# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from borg.localrole.interfaces import IFactoryTempFolder
from borg.localrole.interfaces import ILocalRoleProvider
from zope.component import adapter
from zope.interface import implementer


@adapter(IFactoryTempFolder)
@implementer(ILocalRoleProvider)
class FactoryTempFolderProvider(object):
    """A simple local role provider which just gathers the roles from
    the desired context
    """

    def __init__(self, obj):
        self.tempfolder = obj

    def getRoles(self, principal_id):
        lrp = ILocalRoleProvider(aq_parent(aq_parent(self.tempfolder)))
        if lrp:
            return lrp.getRoles(principal_id)
        return tuple()

    def getAllRoles(self):
        # This should not be used in any meaningful way, so we'll make it cheap
        return {}
