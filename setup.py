from setuptools import setup, find_packages

import sys
import os.path

## Ensure that ``./autogen.sh`` is run prior to using ``setup.py``
if "%%short-version%%".startswith("%%"):
    import os
    import subprocess
    if not os.path.exists('./autogen.sh'):
        sys.stderr.write(
            "This source repository was not configured.\n"
            "Please ensure ``./autogen.sh`` exists and that you are running "
            "``setup.py`` from the project root directory.\n")
        sys.exit(1)
    if os.path.exists('.autogen.sh.output'):
        sys.stderr.write(
            "It seems that ``./autogen.sh`` couldn't do its job as expected.\n"
            "Please try to launch ``./autogen.sh`` manualy, and send the "
            "results to the\nmaintainer of this package.\n"
            "Package will not be installed !\n")
        sys.exit(1)
    sys.stderr.write(
        "Missing version information: running './autogen.sh'...\n")
    os.system('./autogen.sh > .autogen.sh.output')
    cmdline = sys.argv[:]
    if cmdline[1] == "install":
        ## XXXvlab: for some reason, this is needed when launched from pip
        if cmdline[0] == "-c":
            cmdline[0] = "setup.py"
        errlvl = subprocess.call(["python", ] + cmdline)
        os.unlink(".autogen.sh.output")
        sys.exit(errlvl)

description_files = [
    'README.rst',
    'CHANGELOG.rst',
    'TODO.rst',
]

long_description = '\n\n'.join(open(f).read()
                               for f in description_files
                               if os.path.exists(f))

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
    license='BSD License',
    py_modules=['colour'],
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
    ],
    entry_points="",
)
