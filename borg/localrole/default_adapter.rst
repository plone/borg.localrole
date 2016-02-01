Looks at ``__ac_local_roles__`` to find local roles stored persistently on an object::

    >>> from borg.localrole.default_adapter import DefaultLocalRoleAdapter
    >>> obj = DummyObject('dummy')
    >>> roles = DefaultLocalRoleAdapter(obj)


Let's make sure the behavior is sane for objects with no local role awareness::

    >>> roles.getRoles('dummy')
    []
    >>> tuple(roles.getAllRoles())
    ()

Same goes if the RoleManager role map is set to None::

    >>> obj.__ac_local_roles__ = None
    >>> roles.getRoles('dummy')
    []
    >>> tuple(roles.getAllRoles())
    ()

And if we have some roles assigned, we get the expected behavior::

    >>> obj.__ac_local_roles__ = {'dummy': ['Role1', 'Role2']}
    >>> roles.getRoles('dummy')
    ['Role1', 'Role2']
    >>> roles.getRoles('dummy2')
    []
    >>> tuple(roles.getAllRoles())
    (('dummy', ['Role1', 'Role2']),)

The __ac__local_roles__ attribute may be a callable::

    >>> obj.__ac_local_roles__ = lambda: {'dummy2': ['Role1']}
    >>> roles.getRoles('dummy')
    []
    >>> roles.getRoles('dummy2')
    ['Role1']
    >>> tuple(roles.getAllRoles())
    (('dummy2', ['Role1']),)
