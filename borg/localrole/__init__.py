# -*- coding: utf-8 -*-
from AccessControl.Permissions import add_user_folders
from borg.localrole import workspace
from Products.PluggableAuthService import registerMultiPlugin


registerMultiPlugin(workspace.WorkspaceLocalRoleManager.meta_type)


def initialize(context):
    # Register PAS plug-in

    context.registerClass(
        workspace.WorkspaceLocalRoleManager,
        permission=add_user_folders,
        constructors=(
            workspace.manage_addWorkspaceLocalRoleManagerForm,
            workspace.manage_addWorkspaceLocalRoleManager,
        ),
        visibility=None
    )
