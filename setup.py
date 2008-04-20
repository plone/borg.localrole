from setuptools import setup, find_packages
import sys, os

version = '2.0.0'

setup(name='borg.localrole',
      version=version,
      description="A PAS plugin which can manage local roles via an adapter lookup on the current context",
      long_description="""\
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone PAS local roles',
      author='Martin Aspeli, Wichert Akkerman, Alec Mitchell',
      author_email='optilude@gmx.net',
      url='http://svn.plone.org/svn/collective/borg/borg.localrole',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['borg'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "setuptools",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
