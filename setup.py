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
    version='0.0.0a0',
    description=(
        'Patches up the environment and runs a tool from the local virtualenv'
    ),
    long_description=readme + '\n\n' + changes,
    author='Bert JW Regeer',
    author_email='bertjw@regeer.org',
    url='https://github.com/bertjwregeer/vrun',
    license='MIT',
    packages=find_packages('src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    extras_require={
        'docs': docs_require,
        'testing': tests_require,
    },
    entry_points={"console_scripts": ["vrun = vrun.cli:main"]},
    zip_safe=False,
    keywords='virtualenv',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
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
