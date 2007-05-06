# Borrowed from teamspace and b-org - written primarily by
# Wichert Akkerman

# This module is releasd under the Zope Public License

from Globals import InitializeClass
from Acquisition import aq_inner, aq_chain, aq_parent
from AccessControl import ClassSecurityInfo
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PlonePAS.interfaces.plugins import ILocalRolesPlugin

from borg.localrole.interfaces import IWorkspace

manage_addWorkspaceLocalRoleManagerForm = PageTemplateFile(
        "zmi/WorkspaceLocalRoleManagerForm.pt", globals(),
        __name__="manage_addWorkspaceRoleManagerForm")

def manage_addWorkspaceLocalRoleManager(dispatcher, id, title=None, REQUEST=None):
    """Add a WorkspaceLocalRoleManager to a Pluggable Authentication Services."""
    wlrm = WorkspaceLocalRoleManager(id, title)
    dispatcher._setObject(wlrm.getId(), wlrm)

    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(
                '%s/manage_workspace?manage_tabs_message=WorkspaceLocalRoleManager+added.'
                % dispatcher.absolute_url())

class WorkspaceLocalRoleManager(BasePlugin):
    meta_type = "Workspace Roles Manager"
    security  = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self.id = id
        self.title = title

    #
    # ILocalRolesPlugin implementation
    #

    security.declarePrivate("getRolesInContext")
    def getRolesInContext(self, user, object):
        roles = []

        obj, workspace = self._findWorkspace(object)
        if workspace is not None:
            if user._check_context(obj):
                roles.extend(workspace.getLocalRolesForPrincipal(user))
                
        return roles

    security.declarePrivate("checkLocalRolesAllowed")
    def checkLocalRolesAllowed(self, user, object, object_roles):
        roles = []
        
        obj, workspace = self._findWorkspace(object)
        if workspace is not None:
            if not user._check_context(obj):
                return 0
            roles = workspace.getLocalRolesForPrincipal(user)
            for role in roles:
                if role in object_roles:
                    return 1
        
        return None

    security.declarePrivate("getAllLocalRolesInContext")
    def getAllLocalRolesInContext(self, object):
        rolemap = {}
        
        obj, workspace = self._findWorkspace(object)
        if workspace is not None:
            localRoleMap = workspace.getLocalRoles()
            for (principal, roles) in localRoleMap.items():
                rolemap.setdefault(principal, set()).update(roles)
                
        return rolemap
        
    # Helper methods
        
    security.declarePrivate("_findWorkspace")
    def _findWorkspace(self, object):
        """Find the first workspace, if any, in the acquistion chain of this
        object. Returns a tuple obj, workspace where workspace is the adapted
        IWorkspace.
        """
        
        for obj in self._chain(object):
            workspace = IWorkspace(obj, None)
            if workspace is not None:
                return obj, workspace
        return None, None
    
    security.declarePrivate("_chain")
    def _chain(self, object):
        """Generator to walk the acquistion chain of object, considering that it 
        could be a function.
        """
        
        # Walk up the acquisition chain of the object, to be able to check
        # each one for IWorkspace.

        # If the thing we are accessing is actually a bound method on an
        # instance, then after we've checked the method itself, get the
        # instance it's bound to using im_self, so that we can continue to 
        # walk up the acquistion chain from it (incidentally, this is why we 
        # can't juse use aq_chain()).

        context = aq_inner(object)
        
        while context is not None:
            yield context
            
            funcObject = getattr(context, 'im_self', None )
            if funcObject is not None:
                context = aq_inner(funcObject)
            else:
                # Don't use aq_inner() since portal_factory (and probably other)
                # things, depends on being able to wrap itself in a fake context.
                context = aq_parent(context)

classImplements(WorkspaceLocalRoleManager, ILocalRolesPlugin)
InitializeClass(WorkspaceLocalRoleManager)
