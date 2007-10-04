import unittest
import doctest

from zope.app.testing import placelesssetup
import zope.testing.doctest

from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup, PloneSite

import borg.localrole

@onsetup
def setup_product():
    """Set up the additional products required for this package.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for dependent packages.
    
    fiveconfigure.debug_mode = True
    zcml.load_config('configure.zcml', borg.localrole)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('borg.localrole')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need.Then, we let PloneTestCase set up this 
# product on installation.

setup_product()
ptc.setupPloneSite(products=['borg.localrole'])

def test_suite():
    return unittest.TestSuite([

        ztc.ZopeDocFileSuite(
            'README.txt', package='borg.localrole',
            test_class=ptc.FunctionalTestCase,
            optionflags=(doctest.ELLIPSIS | 
                         doctest.NORMALIZE_WHITESPACE |
                         doctest.REPORT_ONLY_FIRST_FAILURE)),
        
        ztc.ZopeDocFileSuite(
            'bbb.txt', package='borg.localrole.bbb',
            test_class=ptc.FunctionalTestCase,
            optionflags=(doctest.ELLIPSIS | 
                         doctest.NORMALIZE_WHITESPACE |
                         doctest.REPORT_ONLY_FIRST_FAILURE)),
        
        
        zope.testing.doctest.DocTestSuite(borg.localrole.workspace,
            setUp=placelesssetup.setUp(),
            tearDown=placelesssetup.tearDown()),

        
        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
