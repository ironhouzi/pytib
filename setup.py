import fileinput

from setuptools import setup
from subprocess import run, CalledProcessError, PIPE, DEVNULL


PACKAGE_NAME = 'pytib'


def _untagged_dev_version():
    try:
        # parameters to get correct info if light weight tags are used
        r = run(('git', 'describe', '--tags', '--abbrev=0'),
                stdout=PIPE, stderr=DEVNULL, check=True)
        _dev_version = r.stdout.decode().strip()
    except CalledProcessError:
        _dev_version = '0.1.0'

    # Used for automatic development versions only!
    r = run(('git', 'rev-parse', 'HEAD'), stdout=PIPE, check=True)

    return f'{_dev_version}+git{r.stdout.decode().strip()}'


try:
    # Releases must be done with git tags
    r = run(('git', 'tag', '-l', '--points-at', 'HEAD'),
            check=True, stdout=PIPE, stderr=DEVNULL)
    _version = r.stdout.decode().strip()

    # If not, create a development version based on git commit
    if _version == '':
        _version = _untagged_dev_version()
except CalledProcessError:
    _version = _untagged_dev_version()

with open(f'{PACKAGE_NAME}/__init__.py', 'a') as f:
    f.write("__version__ = '%s'" % _version)

try:
    setup(
        name='pytib',
        version=_version,
        description='Produce Tibetan unicode from latin script',
        url='https://github.com/ironhouzi/pytib',
        author='Robin Skahjem-Eriksen',
        author_email='robin@skahjem-eriksen.no',
        license='MIT',
        packages=[
            'pytib',
        ],
        scripts=['ptib'],
        install_requires=[
            'click',
        ],
        include_package_data=True,
        zip_safe=False
    )
finally:
    # remove injected __version__ line so version control is unaffected by build
    for line in fileinput.input(f'{PACKAGE_NAME}/__init__.py', inplace=True):
        if line.startswith('__version__'):
            print('', end='')
