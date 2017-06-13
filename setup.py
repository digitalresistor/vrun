from setuptools import setup, find_packages

def readfile(name):
    with open(name) as f:
        return f.read()

readme = readfile('README.rst')
changes = readfile('CHANGES.rst')

docs_require = [
    'Sphinx',
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(
    name='vrun',
    version='0.3',
    description=(
        "Adds Python's bin/Scripts directory to PATH before executing a command. "
        "Primarily used with Python virtual environments."
    ),
    long_description=readme + '\n\n' + changes,
    author='Bert JW Regeer',
    author_email='bertjw@regeer.org',
    url='https://github.com/bertjwregeer/vrun',
    license='ISC',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    extras_require={
        'docs': docs_require,
        'testing': tests_require,
    },
    entry_points={
        "console_scripts": [
            "vrun = vrun.cli:main",
            "vexec = vrun.cli:main",
        ]
    },
    zip_safe=False,
    keywords='virtualenv vexec vrun venv bin Scripts',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
)
