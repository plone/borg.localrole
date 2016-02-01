# -*- coding: utf-8 -*-
from borg.localrole.interfaces import ILocalRoleProvider
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ILocalRoleProvider)
@adapter(Interface)
class DefaultLocalRoleAdapter(object):
    """Looks at __ac_local_roles__ to find local roles stored
    persistently on an object
    """

    def __init__(self, context):
        self.context = context

    @property
    def _rolemap(self):
        rolemap = getattr(self.context, '__ac_local_roles__', {})
        # None is the default value from AccessControl.Role.RoleMananger
        if rolemap is None:
            return {}
        if callable(rolemap):
            rolemap = rolemap()
        return rolemap

    def getRoles(self, principal_id):
        """Returns the roles for the given principal in context"""
        return self._rolemap.get(principal_id, [])

    def getAllRoles(self):
        """Returns all the local roles assigned in this context:
        (principal_id, [role1, role2])"""
        return self._rolemap.iteritems()
