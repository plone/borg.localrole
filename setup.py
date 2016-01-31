# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


name = 'borg.localrole'
version = '3.1.2.dev0'

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

setup(
    name=name,
    version=version,
    description='A PAS plugin which can manage local roles via an '
                'adapter lookup on the current context',
    long_description=readme + '\n' + history,
    keywords='Plone PAS local roles',
    author='Borg Collective',
    author_email='borg@plone.org',
    url='http://pypi.python.org/pypi/borg.localrole',
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
        'Acquisition',
        'plone.memoize',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Products.PlonePAS',
        'Products.PluggableAuthService',
        'setuptools',
        'zope.annotation',
        'zope.component',
        'zope.deferredimport',
        'zope.interface',
        'Zope2',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
