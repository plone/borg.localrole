from setuptools import setup, find_packages
from os.path import join

name = 'borg.localrole'
version = '2.0.1'

path = join(*name.split('.'))
readme = open(join(path, 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read().replace(name + ' - ', '')

setup(name = name,
      version = version,
      description = 'A PAS plugin which can manage local roles via an '
                    'adapter lookup on the current context',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'Plone PAS local roles',
      author = 'Borg Collective',
      author_email = 'borg@plone.org',
      url = 'http://pypi.python.org/pypi/borg.localrole',
      license = 'LGPL',
      packages = find_packages(exclude=['ez_setup']),
      namespace_packages = ['borg'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      install_requires=[
        'setuptools',
        'plone.memoize',
      ],
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Intended Audience :: Other Audience',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
)
