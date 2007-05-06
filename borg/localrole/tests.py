import unittest
import doctest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

import borg.localrole

ptc.setupPloneSite()

class LocalRoleTestCase(ptc.FunctionalTestCase):

    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml', borg.localrole)
            fiveconfigure.debug_mode = False

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.txt', package='borg.localrole',
            test_class=LocalRoleTestCase,
            optionflags=(doctest.ELLIPSIS | 
                         doctest.NORMALIZE_WHITESPACE |
                         doctest.REPORT_ONLY_FIRST_FAILURE)),
        
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
