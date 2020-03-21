Changelog
=========

.. You should *NOT* be adding new change log entries to this file.
   You should create a file in the news directory instead.
   For helpful instructions, please see:
   https://github.com/plone/plone.releaser/blob/master/ADD-A-NEWS-ITEM.rst

.. towncrier release notes start

3.1.7 (2020-03-21)
------------------

Bug fixes:


- Minor packaging updates. [various] (#1)


3.1.6 (2018-09-23)
------------------

Bug fixes:

- Python 2 / 3 compatibility.
  [ale-rt, pbauer]

- Fix issue StopIteration raising a Runtimeerror in Python 3.7
  See https://www.python.org/dev/peps/pep-0479/
  [pbauer]


3.1.5 (2018-02-02)
------------------

Bug fixes:

- Import ``activatePluginInterfaces`` from the canonical place in ``Products.PlonePAS``.
  [maurits]

- Python 2 / 3 compat with six.
  [jensens]

- Cleanup:

    - No self-contained buildout,
    - utf8-headers,
    - isort,
    - ZCA-decorators
    - formatting/readability/pep8,
    - Security decorators

  [jensens]

- Fix test for Zope 4.
  [pbauer]


3.1.4 (2017-10-17)
------------------

Bug fixes:

- Made test compatible with zope4.  [pbauer]


3.1.3 (2016-11-18)
------------------

Bug fixes:

- Removed ZopeTestCase.  [maurits]


3.1.2 (2016-08-17)
------------------

Fixes:

- Use zope.interface decorator.
  [gforcada]


3.1.1 (2014-10-23)
------------------

- Ported tests to plone.app.testing
  [tomgross]

3.1 (2014-03-01)
----------------

- Moved portal_factory stuff to Products.ATContentTypes for PLIP #13770
  [ale-rt]

3.0.2 - 2010-10-27
------------------

- Close ``<input>`` tags properly (Chameleon compatibility).
  [swampmonkey]

3.0.1 - 2010-07-18
------------------

- Avoid raising deprecation warnings about our own code.
  [hannosch]

- Use the standard libraries doctest module.
  [hannosch]

3.0 - 2010-07-01
----------------

- Update docstring. Nested groups do work properly.
  [esteele]

3.0a1 - 2009-11-17
------------------

- Avoid polluting test environment with extra adapter registrations.
  [davisagli]

- Use `Testing.ZopeTestCase.placeless` instead of `zope.app.testing.placeless`.
  [hannosch]

- Adjusted test setup for Plone 5.
  [hannosch]

- Added the `replace_local_role_manager` method formerly found in CMFPlone.
  [hannosch]

- Standardize package documentation and remove invalid license files.
  [hannosch]

- Declare test dependencies in an extra and fixed deprecation warnings
  for use of Globals.
  [hannosch]

2.0.2 - Unreleased
------------------

- Specify package dependencies.
  [hannosch]

2.0.1 - 2008-07-31
------------------

- Support caching of allowed local roles on the request.
  [witsch]

- Renamed the default adapter to "default" so that people don't
  accidentally override it with an unnamed adapter. Overriding the default
  should be possible, but is a marginal use case. If it's overridden but
  not replicated properly, all sorts of problems can result.
  [optilude]

- Added exportimport.zcml which registers TitleOnlyExportImport for
  WorkspaceLocalRoleManager; this allows local roles plug-in to be
  imported and exported as part of a GenericSetup profile.
  [rafrombrc]

2.0.0 - 2008-04-20
------------------

- Baseline for Plone 3.1
