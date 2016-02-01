Changelog
=========

3.1.2 (unreleased)
------------------

- PEP8, UTF8 headers, sorted imports, security decorators, and other cleanup.
  [jensens]


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
