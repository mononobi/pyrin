# -*- coding: utf-8 -*-
"""
pyrin setup module.
"""

import io
import re

from setuptools import find_namespace_packages
from setuptools import setup


with io.open('README.md', 'rt', encoding='utf8') as readme_file:
    README = readme_file.read()

with io.open('src/pyrin/__init__.py', 'rt', encoding='utf8') as version_file:
    VERSION = re.search(r"__version__ = '(.*?)'", version_file.read()).group(1)

PACKAGES = [
    'aniso8601>=9.0.1',
    'bcrypt>=3.1.7',
    'pytz>=2021.1',
    'Flask>=1.1.1',
    'PyJWT>=2.0.1',
    'SQLAlchemy>=1.4',
    'colorama>=0.4.3',
    'python-dotenv>=0.16.0',
    'cryptography>=3.4.7',
    'flask-babel>=2.0.0',
    'babel>=2.9.0',
    'alembic>=1.5.8',
    'fire>=0.4.0',
    'sqlparse>=0.4.1',
    'titlecase>=2.0.0',
]

TEST_PACKAGES = PACKAGES + [
    'pytest',
    'pytest-cov',
    'pygments',
]

DOC_PACKAGES = [
    'sphinx',
    'sphinxcontrib-log-cabinet',
    'sphinx-issues',
]

MEMCACHED_PACKAGES = [
    'pymemcache>=3.4.1',
]

SENTRY_PACKAGES = [
    'sentry-sdk>=1.0.0',
    'blinker>=1.4',
]

CELERY_PACKAGES = [
    'celery>=5.0.5',
]

REDIS_PACKAGES = [
    'redis>=3.5.3',
]

setup(
    name='pyrin',
    version=VERSION,
    url='https://github.com/mononobi/pyrin',
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
    description='A rich platform-independent application framework '
                'to build apps using Flask on top of it.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords=('flask python sqlalchemy pyrin core alembic multi-database '
              'application-framework rest-api dependency-injection ioc'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    packages=find_namespace_packages('src', exclude=('tests', 'tests.*')),
    package_dir={'': 'src'},
    package_data={'': ['*']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=PACKAGES,
    extras_require={
        'tests': TEST_PACKAGES,
        'docs': DOC_PACKAGES,
        'memcached': MEMCACHED_PACKAGES,
        'sentry': SENTRY_PACKAGES,
        'celery': CELERY_PACKAGES,
        'redis': REDIS_PACKAGES,
    },
    entry_points={"console_scripts": ["pyrin = pyrin.cli.core.command:main"]},
)
