from zope.interface import Interface
import zope.deferredimport

zope.deferredimport.deprecated(
    "Please use borg.localrole.interfaces.ILocalRoleProvider instead",
    IWorkspace = 'borg.localrole.bbb.interfaces:IWorkspace'
    )

zope.deferredimport.deprecated(
    "Please use borg.localrole.interfaces.ILocalRoleProvider instead",
    IGroupAwareWorkspace = 'borg.localrole.bbb.interfaces:IGroupAwareWorkspace'
    )

class ILocalRoleProvider(Interface):
    """An interface which allows querying the local roles on an object"""

    def getRoles(principal_id):
        """Returns an iterable of roles granted to the specified user object
        """

    def getAllRoles():
        """Returns an iterable consisting of tuples of the form:
            (principal_id, sequence_of_roles)
        """