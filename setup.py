# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


name = 'borg.localrole'
version = '3.1.6'

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
    url='https://pypi.python.org/pypi/borg.localrole',
    license='LGPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['borg'],
    include_package_data=True,
    platforms='Any',
    zip_safe=False,
    extras_require=dict(
        test=[
            'plone.app.testing',
        ],
    ),
    install_requires=[
        'setuptools',
        'six',
        'zope.annotation',
        'zope.component',
        'zope.deferredimport',
        'zope.interface',
        'Products.CMFCore',
        'Products.GenericSetup',
        'Products.PlonePAS >= 5.0.1',
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
        'Framework :: Plone :: 5.2',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',  # noqa
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
