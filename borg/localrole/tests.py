import unittest
import doctest

from zope.interface import implements
import zope.testing.doctest

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import borg.localrole
from borg.localrole import factory_adapter
from borg.localrole import default_adapter


class SimpleLocalRoleProvider(object):
    implements(borg.localrole.interfaces.ILocalRoleProvider)
    def __init__(self, context):
        self.context = context

    def getRoles(self, user):
        """Grant everyone the 'Foo' role"""
        return ('Foo',)

    def getAllRoles(self):
        """In the real world we would enumerate all users and
        grant the 'Foo' role to each, but we won't"""
        yield ('bogus_user', ('Foo',))


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

@onsetup
def setup_package():
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', borg.localrole)
    fiveconfigure.debug_mode = False

    ztc.installPackage('borg.localrole')


setup_package()
ptc.setupPloneSite(extension_profiles=(
    'borg.localrole:default',
))

def test_suite():
    suite = []

    suite.extend([
        ztc.ZopeDocFileSuite(
                    'README.txt', package='borg.localrole',
                    test_class=ptc.FunctionalTestCase,
                    optionflags=(doctest.ELLIPSIS |
                                 doctest.NORMALIZE_WHITESPACE)),
        ztc.ZopeDocFileSuite(
                    'bbb.txt', package='borg.localrole.bbb',
                    test_class=ptc.FunctionalTestCase,
                    optionflags=(doctest.ELLIPSIS |
                                 doctest.NORMALIZE_WHITESPACE)),
        ])

    # Add the tests that register adapters at the end

    suite.extend([
        zope.testing.doctest.DocTestSuite(borg.localrole.workspace,
            setUp=ztc.placeless.setUp(),
            tearDown=ztc.placeless.tearDown(),
            optionflags=zope.testing.doctest.ELLIPSIS |
                        zope.testing.doctest.NORMALIZE_WHITESPACE),

        zope.testing.doctest.DocTestSuite(factory_adapter),
        zope.testing.doctest.DocTestSuite(default_adapter),
        ])


    return unittest.TestSuite(suite)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
