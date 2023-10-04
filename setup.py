from pathlib import Path
from setuptools import find_packages
from setuptools import setup


name = "borg.localrole"
version = "3.1.11.dev0"

long_description = (
    f"{Path('README.rst').read_text()}\n{Path('CHANGES.rst').read_text()}"
)

setup(
    name=name,
    version=version,
    description="A PAS plugin which can manage local roles via an "
    "adapter lookup on the current context",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    keywords="Plone PAS local roles",
    author="Borg Collective",
    author_email="borg@plone.org",
    url="https://pypi.org/project/borg.localrole",
    license="LGPL",
    packages=find_packages(),
    namespace_packages=["borg"],
    include_package_data=True,
    platforms="Any",
    zip_safe=False,
    python_requires=">=3.8",
    extras_require=dict(
        test=[
            "plone.app.testing",
            "plone.testing",
        ],
    ),
    install_requires=[
        "AccessControl",
        "setuptools",
        "zope.annotation",
        "zope.component",
        "zope.deferredimport",
        "zope.interface",
        "Products.CMFCore",
        "Products.GenericSetup",
        "Products.PlonePAS >= 5.0.1",
        "Products.PluggableAuthService",
        "plone.memoize",
        "Acquisition",
        "Zope",
    ],
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0",
        "Framework :: Plone :: 5.1",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Core",
        "Intended Audience :: Other Audience",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
