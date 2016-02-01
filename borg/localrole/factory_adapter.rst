::
    >>> from zope.component import provideAdapter
    >>> from zope.interface import Interface, implements, alsoProvides
    >>> from borg.localrole.workspace import WorkspaceLocalRoleManager
    >>> from borg.localrole.factory_adapter import FactoryTempFolderProvider
    >>> from borg.localrole.interfaces import IFactoryTempFolder
    >>> rm = WorkspaceLocalRoleManager('rm', 'A Role Manager')
    >>> root = DummyObject('root')


Let's construct a hierarchy similar to the way portal factory is used::

    root --> folder -------|
      |------------> PortalFactory --> TempFolder --> NewObject

And so in code

::

    >>> fold = DummyObject('fold').__of__(root)
    >>> factory = DummyObject('factory').__of__(root)
    >>> wrapped_factory = factory.__of__(fold)
    >>> temp = DummyObject('temp').__of__(wrapped_factory)
    >>> newob = DummyObject('newob').__of__(temp)

    >>> from borg.localrole.tests import SimpleLocalRoleProvider
    >>> from borg.localrole.interfaces import ILocalRoleProvider
    >>> from borg.localrole.tests import DummyUser
    >>> user1 = DummyUser('bogus_user1')


To test our adapter we need an acl_users, and our user needs a
getRolesInContext method::

    >>> class FakeUF(object):
    ...     def getUserById(self, userid, default=None):
    ...         if userid == user1.getId():
    ...             return user1
    ...         return None
    >>> root.acl_users = FakeUF()
    >>> def getRolesInContext(user, context):
    ...     return rm.getRolesInContext(user, context)
    >>> from new import instancemethod
    >>> user1.getRolesInContext = instancemethod(
    ...     getRolesInContext,
    ...     user1,
    ...     DummyUser)


Check for leftovers::

    >>> ILocalRoleProvider(root)
    Traceback (most recent call last):
    ...
    TypeError: ('Could not adapt', <DummyObject root>,
    <InterfaceClass borg.localrole.interfaces.ILocalRoleProvider>)

We add special interface to our Folder which allows us to provide
some local roles, these roles will be inherited by any contained
objects but not by our 'newob' because though the folder is its
acquisition chain it is not contained by it::


    >>> rm.getRolesInContext(user1, fold)
    []

    >>> class ISpecialInterface(Interface):
    ...     pass
    >>> alsoProvides(fold, ISpecialInterface)
    >>> provideAdapter(
    ...     SimpleLocalRoleProvider,
    ...     adapts=(ISpecialInterface,)
    ... )
    >>> rm.getRolesInContext(user1, fold)
    ['Foo']

    >>> contained = DummyObject('contained').__of__(fold)
    >>> rm.getRolesInContext(user1, contained)
    ['Foo']

    >>> rm.getRolesInContext(user1, newob)
    []

The getAllRoles method always returns an empty dict, because it is
only used for thing which are irrelevant for temporary objects (or
the original author was lazy)::

    >>> ftfp = FactoryTempFolderProvider(newob)
    >>> ftfp.getAllRoles()
    {}

