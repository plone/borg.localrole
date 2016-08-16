from setuptools import setup, find_packages

name = 'borg.localrole'
version = '3.1.2'

readme = open('README.txt').read()
history = open('CHANGES.txt').read()

setup(
    name=name,
    version=version,
    description='A PAS plugin which can manage local roles via an '
                'adapter lookup on the current context',
    long_description=readme + '\n' + history,
    keywords='Plone PAS local roles',
    author='Borg Collective',
    author_email='borg@plone.org',
    url='https://pypi.python.org/pypi/borg.localrole',
    license='LGPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['borg'],
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    extras_require=dict(
      test=[
          'Products.ATContentTypes',
          'plone.app.testing',
      ]
    ),
    install_requires=[
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.deferredimport',
        'zope.interface',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Products.PlonePAS',
        'Products.PluggableAuthService',
        'plone.memoize',
        'Acquisition',
        'Zope2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',  # noqa
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
