# -*- coding: utf-8 -*-
from Acquisition import Implicit
from borg.localrole.testing import BORGLOCALROLE_ZOPE_FIXTURE
from plone.testing import layered
from zope.interface import implementer

import borg.localrole
import doctest
import unittest


@implementer(borg.localrole.interfaces.ILocalRoleProvider)
class SimpleLocalRoleProvider(object):

    def __init__(self, context):
        self.context = context

    def getRoles(self, user):
        """Grant everyone the 'Foo' role"""
        return ('Foo', )

    def getAllRoles(self):
        """In the real world we would enumerate all users and
        grant the 'Foo' role to each, but we won't"""
        yield ('bogus_user', ('Foo', ))


class DummyUser(object):

    def __init__(self, uid, group_ids=()):
        self.id = uid
        self._groups = group_ids

    def getId(self):
        return self.id

    def _check_context(self, obj):
        return True

    def getGroups(self):
        return self._groups

    def getRoles(self):
        return ()


class DummyObject(Implicit):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<DummyObject {0}>'.format(self.name)


optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
optionflags = optionflags | doctest.REPORT_ONLY_FIRST_FAILURE

TESTFILES = [
    ('workspace.rst', BORGLOCALROLE_ZOPE_FIXTURE),
    ('default_adapter.rst', BORGLOCALROLE_ZOPE_FIXTURE),
    ('factory_adapter.rst', BORGLOCALROLE_ZOPE_FIXTURE),
]


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                docfile,
                globs={
                    'DummyObject': DummyObject,
                    'DummyUser': DummyUser,
                    'SimpleLocalRoleProvider': SimpleLocalRoleProvider,
                },
                optionflags=optionflags,
            ),
            layer=layer,
        ) for docfile, layer in TESTFILES
    ])
    return suite
