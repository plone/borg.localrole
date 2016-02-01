# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Acquisition import aq_get
from Acquisition import aq_inner
from Acquisition import aq_parent
from App.class_init import InitializeClass
from borg.localrole.bbb.interfaces import IGroupAwareWorkspace  # BBB
from borg.localrole.bbb.interfaces import IWorkspace  # BBB
from borg.localrole.interfaces import ILocalRoleProvider
from plone.memoize.volatile import cache
from plone.memoize.volatile import DontCache
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PlonePAS.interfaces.plugins import ILocalRolesPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from zope.annotation.interfaces import IAnnotations
from zope.component import getAdapters
from zope.deprecation import deprecate
from zope.interface import implementer

import warnings


manage_addWorkspaceLocalRoleManagerForm = PageTemplateFile(
    'zmi/WorkspaceLocalRoleManagerForm.pt',
    globals(),
    __name__='manage_addWorkspaceRoleManagerForm'
)


def manage_addWorkspaceLocalRoleManager(
    dispatcher,
    id,
    title=None,
    REQUEST=None
):
    """Add a WorkspaceLocalRoleManager to a Pluggable Authentication Services.
    """
    wlrm = WorkspaceLocalRoleManager(id, title)
    dispatcher._setObject(wlrm.getId(), wlrm)

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(
            '{0}/manage_workspace?manage_tabs_message='
            'WorkspaceLocalRoleManager+added.'.format(
                dispatcher.absolute_url()
            )
        )


# memoize support for `checkLocalRolesAllowed`
def clra_cache_key(method, self, user, obj, object_roles):
    """ The cache key needs to include all arguments when caching allowed
        local roles, but the key function also needs to decide whether
        `volatile.cache` can cache or not by checking if it's possible to
        get a request instance from the object.
    """
    request = aq_get(obj, 'REQUEST', None)
    if IAnnotations(request, None) is None:
        raise DontCache
    try:
        oid = obj.getPhysicalPath()
    except AttributeError:
        oid = id(obj)
    return (user.getId(), oid, tuple(object_roles))


def store_on_request(method, self, user, obj, object_roles):
    """ helper for caching local roles on the request """
    return IAnnotations(aq_get(obj, 'REQUEST'))


@implementer(ILocalRolesPlugin)
class WorkspaceLocalRoleManager(BasePlugin):
    """This is the actual plug-in. It takes care of looking up
    ILocalRolesProvider adapters (when available) and granting local roles
    appropriately.
    """
    meta_type = 'Workspace Roles Manager'
    security = ClassSecurityInfo()

    def __init__(self, id, title=''):
        self.id = id
        self.title = title

    def _get_userfolder(user, obj):
        """Gets the unwrapped user folder for the user, because we may
        need to rewrap"""
        context = user
        while context is not None:
            try:
                if context.getId() == 'acl_users':
                    break
            except AttributeError:
                context = aq_parent(aq_inner(context))
        else:
            return None
        return aq_inner(context)
    #
    # ILocalRolesPlugin implementation
    #

    def _getAdapters(self, obj):
        adapters = getAdapters((obj, ), ILocalRoleProvider)
        # this is sequence of tuples of the form (name, adapter),
        # we don't really care about the names
        return (a[1] for a in adapters)

    def _parent_chain(self, obj):
        """Iterate over the containment chain, stopping if we hit a
        local role blocker"""
        while obj is not None:
            yield obj
            if getattr(obj, '__ac_local_roles_block__', None):
                raise StopIteration
            new = aq_parent(aq_inner(obj))
            # if the obj is a method we get the class
            obj = getattr(obj, 'im_self', new)

    def _get_principal_ids(self, user):
        """Returns a list of the ids of all involved security
        principals: the user and all groups that they belong
        to."""
        principal_ids = list(user.getGroups())
        principal_ids.insert(0, user.getId())
        return principal_ids

    @security.private
    def getRolesInContext(self, user, object):
        # we combine the permission of the user with those of the
        # groups she belongs to
        uf = self._get_userfolder(user)
        if uf is not None:
            # rewrap user with an unwrapped user folder, so
            # _check_context works appropriately
            user = aq_inner(user)
            user = user.__of__(uf)
        principal_ids = self._get_principal_ids(user)
        roles = set()
        for obj in self._parent_chain(object):
            if user._check_context(obj):
                count = -1
                for count, a in enumerate(self._getAdapters(obj)):
                    for pid in principal_ids:
                        roles.update(a.getRoles(pid))
                # XXX: BBB code, kicks in only if there's no proper adapter
                if count == -1:
                    warnings.warn(
                        'Fallback to old IGroupAwareWorkspace/IWorkspace, '
                        'will be removed in Plone 6.0',
                        DeprecationWarning
                    )
                    workspace = IGroupAwareWorkspace(
                        obj, IWorkspace(obj, None))
                    if workspace is not None:
                        roles.update(workspace.getLocalRolesForPrincipal(user))
                        for group in self._groups(obj, user, workspace):
                            roles.update(
                                workspace.getLocalRolesForPrincipal(group))
        return list(roles)

    @security.private
    @cache(get_key=clra_cache_key, get_cache=store_on_request)
    def checkLocalRolesAllowed(self, user, object, object_roles):
        """Checks if the user has one of the specified roles in the
        given context, short circuits when the first provider granting
        one of the roles is found."""
        uf = self._get_userfolder(user)
        if uf is not None:
            # rewrap user with an unwrapped user folder, so
            # _check_context works appropriately
            user = aq_inner(user)
            user = user.__of__(uf)
        check_roles = set(object_roles)
        principal_ids = self._get_principal_ids(user)
        for obj in self._parent_chain(object):
            count = -1
            for count, a in enumerate(self._getAdapters(obj)):
                for pid in principal_ids:
                    roles = a.getRoles(pid)
                    if check_roles.intersection(roles):
                        if user._check_context(obj):
                            return 1
                        else:
                            return 0
            # XXX: BBB code, kicks in only if there's no proper adapter
            if count == -1:
                warnings.warn(
                    'Fallback to old IGroupAwareWorkspace/IWorkspace, '
                    'will be removed in Plone 6.0',
                    DeprecationWarning
                )
                workspace = IGroupAwareWorkspace(obj, IWorkspace(obj, None))
                if workspace is not None:
                    roles = workspace.getLocalRolesForPrincipal(user)
                    if check_roles.intersection(roles):
                        if user._check_context(obj):
                            return 1
                        else:
                            return 0
                    for group in self._groups(obj, user, workspace):
                        roles = workspace.getLocalRolesForPrincipal(group)
                        if check_roles.intersection(roles):
                            if user._check_context(obj):
                                return 1
                            else:
                                return 0

        return None

    @security.private
    def getAllLocalRolesInContext(self, object):
        rolemap = {}
        for obj in self._parent_chain(object):
            for a in self._getAdapters(obj):
                iter_roles = a.getAllRoles()
                for principal, roles in iter_roles:
                    rolemap.setdefault(principal, set()).update(roles)
            else:  # XXX: BBB code, kicks in only if there's no proper ddapter
                warnings.warn(
                    'Fallback to old IGroupAwareWorkspace/IWorkspace, '
                    'will be removed in Plone 6.0',
                    DeprecationWarning
                )
                workspace = IGroupAwareWorkspace(obj, IWorkspace(obj, None))
                if workspace is not None:
                    rolemap.update(workspace.getLocalRoles())

        return rolemap

    @security.private
    @deprecate(
        'Fallback to old IGroupAwareWorkspace/IWorkspacewill be removed in '
        'Plone 6.0'
    )
    def _groups(self, obj, user, workspace):
        """If workspace provides IGroupAwareWorkspace and the user has
        a getGroups() method, yield each group_id returned by that method.
        """
        if IGroupAwareWorkspace.providedBy(workspace):
            getGroups = getattr(user, 'getGroups', None)
            if getGroups is not None:
                acl_users = aq_parent(aq_inner(self))
                for group_id in getGroups():
                    yield acl_users.getGroupById(group_id)

InitializeClass(WorkspaceLocalRoleManager)
