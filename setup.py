"""pyjpphonecheckerパッケージsetupスクリプト."""

from setuptools import find_packages
from setuptools import setup


setup(
    name='pyjpphonechecker',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'requests',
        'beautifulsoup4',
        'playwright',
    ],
)
