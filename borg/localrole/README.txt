=========================
 Local roles PAS plug-in
=========================

This PAS plug-in can be used to assign local roles in a particular context,
by adapter.

First, we must install it

    >>> from borg.localrole.utils import setup_localrole_plugin
    >>> print setup_localrole_plugin(self.portal)
    - Activating: local_roles
    borg_localroles activated.

    
It should be safe to install it more than once - if it's already installed,
calling setup_localrole_plugin() will just do nothing.

    >>> print setup_localrole_plugin(self.portal)
    borg_localroles already installed
    
Let us create some users.

    >>> from Products.PloneTestCase.PloneTestCase import default_user
    >>> from Products.CMFCore.utils import getToolByName

    >>> acl_users = getToolByName(self.portal, 'acl_users')
    >>> user = acl_users.getUserById(default_user)

By default, a user does not have any special local roles in a particular 
folder.

    >>> user.getRolesInContext(self.folder)
    ['Member', 'Owner', 'Authenticated']

We will now register a local role adapter, to enable a particular roles
policy.

    >>> from Products.ATContentTypes.interface import IATFolder
    >>> IATFolder.providedBy(self.folder)
    True
    
    >>> from zope.interface import implements
    >>> from zope.component import adapts
    >>> from borg.localrole.interfaces import IWorkspace

    >>> class LocalRoles(object):
    ...     implements(IWorkspace)
    ...     adapts(IATFolder)
    ...     
    ...     def __init__(self, context):
    ...         self.context=context
    ...     
    ...     def getLocalRoles(self):
    ...         return {default_user : ('Manager',)}
    ...     
    ...     def getLocalRolesForPrincipal(self, principal):
    ...         principal_id = principal.getId()
    ...         r = self.getLocalRoles()
    ...         return r.get(principal_id, ())

    >>> from zope.component import provideAdapter
    >>> provideAdapter(LocalRoles)

Now, these roles are appended in the folder:

    >>> sorted(user.getRolesInContext(self.folder))
    ['Authenticated', 'Manager', 'Member', 'Owner']
    
Of course, they do not apply in other places, for which the adapter is not
registered.

    >>> sorted(user.getRolesInContext(self.portal))
    ['Authenticated', 'Member']

It is also possible to assign local roles based on groups. Let us add 
a group.

    >>> groups = getToolByName(self.portal, 'portal_groups')
    >>> _ = groups.addGroup('group1')

For this, we need to use the more specific interface IGroupAwareWorkspace.
This has no additional methods, but we need to make sure the getLocalRoles()
and getLocalRolesForPrincipal() methods can deal with group principals.

    >>> from borg.localrole.interfaces import IGroupAwareWorkspace
    >>> from zope.interface import implementsOnly

    >>> class GroupLocalRoles(LocalRoles):
    ...     implementsOnly(IGroupAwareWorkspace)
    ...     adapts(IATFolder)
    ...     
    ...     def getLocalRoles(self):
    ...         return {default_user : ('Manager',),
    ...                 'group1'     : ('Reviewer',),}

    >>> provideAdapter(GroupLocalRoles)

Until we add the user to the group, this has no effect.

    >>> user.getRolesInContext(self.folder)
    ['Member', 'Owner', 'Manager', 'Authenticated']

But then...

    >>> _ = groups.addPrincipalToGroup(default_user, 'group1')
    >>> user = acl_users.getUserById(default_user) # need this to get updated groups list
    >>> sorted(user.getRolesInContext(self.folder))
    ['Authenticated', 'Manager', 'Member', 'Owner', 'Reviewer']
