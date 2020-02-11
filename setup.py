# -*- coding: utf-8 -*-
"""
pyrin setup module.
"""

import io
import re

from setuptools import find_packages
from setuptools import setup

with io.open('README.md', 'rt', encoding='utf8') as readme_file:
    readme = readme_file.read()

with io.open('src/pyrin/__init__.py', 'rt', encoding='utf8') as version_file:
    version = re.search(r"__version__ = '(.*?)'", version_file.read()).group(1)

setup(
    name='pyrin',
    version=version,
    # url='',
    project_urls={
        # 'Documentation': '',
        'Code': 'https://github.com/mononobi/pyrin',
        'Issue tracker': 'https://github.com/mononobi/pyrin/issues',
    },
    license='GPL-3.0',
    author='Mohamad Nobakht',
    author_email='mohamadnobakht@gmail.com',
    maintainer='Mohamad Nobakht',
    maintainer_email='mohamadnobakht@gmail.com',
    description='Application framework for developing small to '
                'large scale enterprise applications.',
    long_description=readme,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',

    ],
    packages=find_packages('src', exclude=('tests', 'tests.*')),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'aniso8601>=8.0.0',
        'bcrypt>=3.1.7',
        'cffi>=1.13.2',
        'pytz>=2019.3',
        'Flask>=1.1.1',
        'PyJWT>=1.7.1',
        'SQLAlchemy>=1.3.13',
        'colorama>=0.4.3',
        'python-dotenv>=0.10.5',
        'cryptography>=2.8',
        'flask-babel>=1.0.0',
        'babel>=2.8.0',
        'alembic>=1.4.0',
        'fire>=0.2.1',
        'sqlparse>=0.3.0',
    ],
    extras_require={
        'tests': [
            'pytest',
            'pytest-cov',
            'pygments',
        ],
        'docs': [
            'sphinx',
            'sphinxcontrib-log-cabinet',
            'sphinx-issues',
        ],
    },
    # entry_points={'console_scripts': ['pyrin = pyrin.cli.manager:main']},
)
