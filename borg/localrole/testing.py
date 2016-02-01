# -*- coding: utf-8 -*-
from plone.testing import Layer
from plone.testing import z2
from Products.CMFCore.interfaces import ISiteRoot
from Products.PlonePAS.setuphandlers import migrate_root_uf
from zope.component import provideUtility


class BorgLocalroleZopeLayer(Layer):
    """testlayer for borg.localrole - Zope + PAS + PlonePAS only
    """

    defaultBases = (
        z2.INTEGRATION_TESTING,
    )

    # Products that will be installed, plus options
    products = (
        ('zope.component', {'loadZCML': True}, ),
        ('zope.annotation', {'loadZCML': True}, ),
        ('Products.GenericSetup', {'loadZCML': True}, ),
        ('Products.CMFCore', {'loadZCML': True}, ),
        ('Products.PluggableAuthService', {'loadZCML': True}, ),
        ('Products.PluginRegistry', {'loadZCML': True}, ),
        ('Products.PlonePAS', {'loadZCML': True}, ),
    )

    def setUp(self):
        self.setUpZCML()

    def testSetUp(self):
        self.setUpProducts()
        provideUtility(self['app'], provides=ISiteRoot)
        migrate_root_uf(self['app'])

    def setUpZCML(self):
        """Stack a new global registry and load ZCML configuration of Plone
        and the core set of add-on products into it.
        """

        # Load dependent products's ZCML
        from zope.configuration import xmlconfig
        from zope.dottedname.resolve import resolve

        def loadAll(filename):
            for p, config in self.products:
                if not config['loadZCML']:
                    continue
                try:
                    package = resolve(p)
                except ImportError:
                    continue
                try:
                    xmlconfig.file(
                        filename,
                        package,
                        context=self['configurationContext']
                    )
                except IOError:
                    pass

        loadAll('meta.zcml')
        loadAll('configure.zcml')
        loadAll('overrides.zcml')

    def setUpProducts(self):
        """Install all old-style products listed in the the ``products`` tuple
        of this class.
        """
        for prd, config in self.products:
            z2.installProduct(self['app'], prd)


BORGLOCALROLE_ZOPE_FIXTURE = BorgLocalroleZopeLayer()

BORGLOCALROLE_ZOPE_INTEGRATION_TESTING = z2.IntegrationTesting(
    bases=(BORGLOCALROLE_ZOPE_FIXTURE,),
    name='BorgLocalroleZopeLayer:Integration'
)
