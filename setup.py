from setuptools import setup, find_packages

setup(
    name='lip-read',
    version='0.1',
    packages=find_packages(where='machine_learning'),
    package_dir={'': 'machine_learning'},
)
