from setuptools import setup, find_packages

import sys, os.path
## Ensure that ``./autogen.sh`` is run prior to using ``setup.py``
if "%%short-version%%".startswith("%%"):
    import os, subprocess
    if not os.path.exists('./autogen.sh'):
        sys.stderr.write(
            "This source repository was not configured.\n"
            "Please ensure ``./autogen.sh`` exists and that you are running "
            "``setup.py`` from the project root directory.\n")
        sys.exit(1)
    os.system('./autogen.sh')
    cmdline = sys.argv[:]
    if cmdline[1] == "install":
        ## XXXvlab: for some reason, this is needed when launched from pip
        if cmdline[0] == "-c":
            cmdline[0] = "setup.py"
        sys.exit(subprocess.call(["python", ] + cmdline))

description_files = [
    'README.rst',
    'CHANGELOG.rst',
    'TODO.rst',
]

long_description = '\n\n'.join(open(f).read() 
                               for f in description_files 
                               if os.path.exists(f))

## XXXvlab: Hacking distutils, not very elegant, but the only way I found
## to get 'rgb.txt' to get copied next to the colour.py file...
## Any suggestions are welcome.
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

setup(
    name='colour',
    version='%%version%%',
    description='converts and manipulates various color representation '
    '(HSL, RVB, web, X11, ...)',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development",
        "Topic :: Software Development :: Version Control",
        "Programming Language :: Python :: 2.5",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='color convertion',
    author='Valentin Lab',
    author_email='valentin.lab@kalysto.org',
    url='http://github.com/vaab/colour',
    license='GPL License',
    py_modules=['colour'],
    data_files=['rgb.txt'],
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
    ],
    entry_points="",
)
