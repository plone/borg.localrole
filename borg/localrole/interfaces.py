from zope.interface import Interface

class IWorkspace(Interface):
    """A workspace in which custom local roles are needed
    
    A workspace gives information to the Pluggable Authentication Service 
    about local roles. The context will be adapted to this interface to 
    find out which additional local roles should apply.
    """
    
    def getLocalRolesForPrincipal(principal):
        """Return a sequence of all local roles for a principal.
        """

    def getLocalRoles():
        """Return a dictonary mapping principals to their roles within
        a workspace.
        """
