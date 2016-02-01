# -*- coding: utf-8 -*-
from Acquisition import aq_base
from borg.localrole.config import LOCALROLE_PLUGIN_NAME
from borg.localrole.workspace import manage_addWorkspaceLocalRoleManager
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.PlonePAS.plugins.local_role import LocalRolesManager
from StringIO import StringIO


def setup_localrole_plugin(portal):
    """Install and prioritize the local-role PAS plug-in
    """
    out = StringIO()
    uf = getToolByName(portal, 'acl_users')
    existing = uf.objectIds()

    if LOCALROLE_PLUGIN_NAME not in existing:
        manage_addWorkspaceLocalRoleManager(uf, LOCALROLE_PLUGIN_NAME)
        activatePluginInterfaces(portal, LOCALROLE_PLUGIN_NAME, out)
    else:
        out.write('{0} already installed'.format(LOCALROLE_PLUGIN_NAME))
    return out.getvalue()


def replace_local_role_manager(portal):
    """Installs the borg local role manager in place of the standard one from
    PlonePAS"""
    uf = getToolByName(portal, 'acl_users', None)
    # Make sure we have a PAS user folder
    if uf is not None and 'plugins' in aq_base(uf):
        # Remove the original plugin if it's there
        if 'local_roles' in uf.objectIds():
            orig_lr = getattr(uf, 'local_roles')
            if isinstance(orig_lr, LocalRolesManager):
                uf.plugins.removePluginById('local_roles')
        # Install the borg.localrole plugin if it's not already there
        setup_localrole_plugin(portal)
