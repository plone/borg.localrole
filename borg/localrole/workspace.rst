Test Cache Key
==============

The cache key needs to include all arguments when caching allowed
local roles, but the key function also needs to decide whether
`volatile.cache` can cache or not by checking if it's possible to
get a request instance from the object.

To test we'll nee an adaptable object, a user and the method which
results' we'd like to cache::

    >>> obj = DummyObject('testcachekey')
    >>> john = DummyUser('john')

    >>> from borg.localrole.workspace import WorkspaceLocalRoleManager
    >>> rm = WorkspaceLocalRoleManager('rm', 'A Role Manager')
    >>> fun = rm.__class__.checkLocalRolesAllowed

    The dummy object doesn't have an acquired request, so no caching
    can be done::

    >>> from borg.localrole.workspace import clra_cache_key
    >>> clra_cache_key(fun, 'me', john, obj, ['foo', 'bar'])
    Traceback (most recent call last):
    ...
    DontCache

So let's add one and try again.  Before we also need to mark it as
being annotatable, which normally happens elsewhere::

    >>> from ZPublisher.HTTPRequest import HTTPRequest
    >>> request = HTTPRequest('', dict(HTTP_HOST='nohost:8080'), {})
    >>> from zope.interface import alsoProvides
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> alsoProvides(request, IAttributeAnnotatable)

    >>> obj.REQUEST = request
    >>> clra_cache_key(fun, 'hmm', john, obj, ['foo', 'bar'])
    ('john', ..., ('foo', 'bar'))

If the objects happens to have a `getPhysicalPath` method, that should
be used instead of the hash::

    >>> class DummyObjectWithPath(DummyObject):
    ...     def getPhysicalPath(self):
    ...         return '42!'
    >>> obj = DummyObjectWithPath('path')
    >>> obj.REQUEST = request
    >>> clra_cache_key(fun, 'hmm', john, obj, ['foo', 'bar'])
    ('john', '42!', ('foo', 'bar'))

Now let's check if the results of a call to `checkLocalRolesAllowed`
is indeed cached, i.e. is the request was annotated correctly.  First
try to log the method invocation, though.  As monkey patching in
something between the original method and the already applied cache
decorator is tricky, we abuse `_get_userfolder`, which is called
first thing in `checkLocalRolesAllowed`::

    >>> original = rm._get_userfolder
    >>> def logger(self, *args, **kw):
    ...     print 'checkLocalRolesAllowed called...'
    ...     return original(self, *args, **kw)
    >>> rm._get_userfolder = logger

    >>> print rm.checkLocalRolesAllowed(john, obj, ['foo', 'bar'])
    checkLocalRolesAllowed called...
    None

    >>> from zope.annotation.interfaces import IAnnotations
    >>> IAnnotations(request)
    {"borg.localrole.workspace.checkLocalRolesAllowed:('john', '42!',
    ('foo', 'bar'))": None}

Calling the method a second time should directly return the cached
value, i.e. the logger shouldn't print anything::

    >>> print rm.checkLocalRolesAllowed(john, obj, ['foo', 'bar'])
    None

Test Workspace
==============

This is the actual plug-in. It takes care of looking up
ILocalRolesProvider adapters (when available) and granting local roles
appropriately.

First we need to make and register an adapter to provide some roles::

    >>> from zope.interface import implementer, Interface
    >>> from zope.component import adapts
    >>> from borg.localrole.tests import SimpleLocalRoleProvider
    >>> from borg.localrole.tests import DummyUser
    >>> from zope.component import provideAdapter

    >>> class ITestMarker(Interface):
    ...     pass
    >>> provideAdapter(SimpleLocalRoleProvider, adapts=(ITestMarker,))


We need an object to adapt, we require nothing of this object,
except it must be adaptable (e.g. have an interface)::

    >>> @implementer(ITestMarker)
    ... class DummyMarkedObject(DummyObject):
    ...     pass
    >>> ob = DummyMarkedObject('marked')

And we need some users that we'll check the permissions of::

    >>> user1 = DummyUser('bogus_user')
    >>> user2 = DummyUser('bogus_user2')

Now we're ready to make one of our RoleManagers and try it out.
First we'll verify that our users have the 'Foo' role, then we'll
make sure they can access objects which require that role, but not
others::

    >>> rm = WorkspaceLocalRoleManager('rm', 'A Role Manager')
    >>> rm.getRolesInContext(user1, ob)
    ['Foo']
    >>> rm.checkLocalRolesAllowed(user1, ob, ['Bar', 'Foo', 'Baz'])
    1
    >>> rm.checkLocalRolesAllowed(user1, ob, ['Bar', 'Baz']) is None
    True
    >>> rm.getAllLocalRolesInContext(ob)
    {'bogus_user': set(['Foo'])}


Multiple Role Providers
-----------------------

It is a bit more interesting when we have more than one adapter
registered.  We register it with a name so that it supplements,
rather than conflict with or override the existing adapter::

    >>> class LessSimpleLocalRoleProvider(SimpleLocalRoleProvider):
    ...     userid = 'bogus_user2'
    ...     roles = ('Foo', 'Baz')
    ...     def getRoles(self, userid):
    ...         '''Grant bogus_user2 the 'Foo' and 'Baz' roles'''
    ...         if userid == self.userid:
    ...             return self.roles
    ...         return ()
    ...
    ...     def getAllRoles(self):
    ...         yield (self.userid, self.roles)

    >>> provideAdapter(LessSimpleLocalRoleProvider, adapts=(Interface,),
    ...                name='adapter2')

This should have no effect on our first user::

    >>> rm.getRolesInContext(user1, ob)
    ['Foo']
    >>> rm.checkLocalRolesAllowed(user1, ob, ['Bar', 'Foo', 'Baz'])
    1
    >>> rm.checkLocalRolesAllowed(user1, ob, ['Bar', 'Baz']) is None
    True
    >>> rm.getAllLocalRolesInContext(ob)
    {'bogus_user2': set(['Foo', 'Baz']), 'bogus_user': set(['Foo'])}

But our second user notices the change, note that even though two
of our local role providers grant the role 'Foo', it is not duplicated::

    >>> rm.getRolesInContext(user2, ob)
    ['Foo', 'Baz']
    >>> rm.checkLocalRolesAllowed(user2, ob, ['Bar', 'Foo', 'Baz'])
    1
    >>> rm.checkLocalRolesAllowed(user2, ob, ['Bar', 'Baz'])
    1
    >>> rm.checkLocalRolesAllowed(user2, ob, ['Bar']) is None
    True


Role Acquisition and Blocking
-----------------------------

This plugin will acquire role definitions from parent objects,
unless explicitly blocked.  To test this, we need some objects
which support acquisition::

    >>> from Acquisition import Implicit
    >>> class DummyImplicit(DummyMarkedObject, Implicit):
    ...     def stupid_method(self):
    ...         return 1
    >>> root = DummyImplicit('root')
    >>> next = DummyImplicit('next').__of__(root)
    >>> last = DummyImplicit('last').__of__(next)
    >>> other = DummyImplicit('other').__of__(root)

So we now have /root/next/last and /root/other, we'll create and
register special adapters for our next and other objects.

    >>> class ISpecial1(Interface):
    ...     pass
    >>> class ISpecial2(Interface):
    ...     pass
    >>> from zope.interface import directlyProvides
    >>> directlyProvides(next, ISpecial1)
    >>> directlyProvides(other, ISpecial2)
    >>> class Adapter1(LessSimpleLocalRoleProvider):
    ...     adapts(ISpecial1)
    ...     userid = 'bogus_user'
    ...     roles = ('Bar',)
    >>> class Adapter2(LessSimpleLocalRoleProvider):
    ...     adapts(ISpecial2)
    ...     userid = 'bogus_user3'
    ...     roles = ('Foobar',)
    >>> user3 = DummyUser('bogus_user3')

We'll register these to override the existing unnamed adapter:

    >>> provideAdapter(Adapter1)
    >>> provideAdapter(Adapter2)

Now we can show how acquisition of roles works, first we look at the
'last' item, which should have roles provided by
SimpleLocalRoleProvider, and LessSimpleLocalRoleProvider, as well
as acquired from Adapter1 on 'next':

    >>> rm.getRolesInContext(user1, last)
    ['Foo', 'Bar']

    >>> rm.getRolesInContext(user2, last)
    ['Foo', 'Baz']

If we look at the parent, we get the same results, because the
SimpleLocalRoleProvider adapter also applies to the 'root'
object. However, if we enable local role blocking on 'next' we
won't see the roles from the 'root'::

    >>> rm.getRolesInContext(user1, next)
    ['Foo', 'Bar']
    >>> next.__ac_local_roles_block__ = True
    >>> rm.getRolesInContext(user1, next)
    ['Bar']

The checkLocalRolesAllowed and getAllLocalRolesInContext methods
take acquisition and blocking into account as well::

    >>> rm.checkLocalRolesAllowed(user1, last,  ['Bar'])
    1
    >>> rm.checkLocalRolesAllowed(user1, next,  ['Foo', 'Baz']) is None
    True
    >>> rm.getAllLocalRolesInContext(last)
    {'bogus_user2': set(['Foo', 'Baz']), 'bogus_user': set(['Foo', 'Bar'])}

It's important to note, that roles are acquired only by
containment.  Additional wrapping cannot change the security on an
object.  For example if we were to wrap 'last' in the context of
other, which provides a special role for 'user3', we should see no
effect::

    >>> rm.getRolesInContext(user3, last)
    ['Foo']
    >>> rm.getRolesInContext(user3, other)
    ['Foobar', 'Foo']
    >>> rm.getRolesInContext(user3, last.__of__(other))
    ['Foo']

It's also important that methods of objects yield the same local
roles as the objects would

    >>> rm.getRolesInContext(user3, other.stupid_method)
    ['Foobar', 'Foo']

Group Support
-------------

This plugin also handles roles granted to user groups, calling up
the adapters to get roles for any groups the user might belong
to::

    >>> user4 = DummyUser('bogus_user4', ('Group1', 'Group2'))
    >>> user4.getGroups()
    ('Group1', 'Group2')
    >>> rm.getRolesInContext(user4, last)
    ['Foo']
    >>> class Adapter3(LessSimpleLocalRoleProvider):
    ...     userid = 'Group2'
    ...     roles = ('Foobar',)

    >>> provideAdapter(Adapter3, adapts=(Interface,), name='group_adapter')
    >>> rm.getRolesInContext(user4, last)
    ['Foobar', 'Foo']


Wrong User Folder
-----------------

Finally, to ensure full test coverage, we provide a user object
which pretends to be wrapped in such a way that the user folder
does not recognize it.  We check that it always gets an empty set
of roles and a special 0 value when checking access::

    >>> class BadUser(DummyUser):
    ...     def _check_context(self, obj):
    ...         return False
    >>> bad_user = BadUser('bad_user')
    >>> rm.getRolesInContext(bad_user, ob)
    []
    >>> rm.checkLocalRolesAllowed(bad_user, ob, ['Bar', 'Foo', 'Baz'])
    0

