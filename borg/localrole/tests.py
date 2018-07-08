# -*- coding: utf-8 -*-
from borg.localrole import default_adapter
from borg.localrole import factory_adapter
from plone.app.testing import PLONE_INTEGRATION_TESTING
from plone.testing import layered
from plone.testing import zca
from zope.interface import implementer

import borg.localrole
import doctest
import re
import six
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


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub("set\(\[(.*?)\]\)", "{\\1}", got)
            want = re.sub(
                'plone.memoize.volatile.DontCache',
                'DontCache', want
            )
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    suite = [
        layered(
            doctest.DocFileSuite(
                'README.txt',
                package='borg.localrole',
                optionflags=(doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
            ),
            layer=PLONE_INTEGRATION_TESTING),
        layered(
            doctest.DocTestSuite(
                borg.localrole.workspace,
                optionflags=(doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE),
                checker=Py23DocChecker(),
            ),
            layer=zca.UNIT_TESTING
        ),
        layered(
            doctest.DocTestSuite(
                factory_adapter,
                optionflags=(doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
            ),
            layer=zca.UNIT_TESTING
        ),
        doctest.DocTestSuite(default_adapter),
    ]
    return unittest.TestSuite(suite)
