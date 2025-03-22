from setuptools import setup, find_packages

setup(
    name='lipseek',
    version='0.1',
    packages=find_packages(where='machine_learning'),
    package_dir={'': 'machine_learning'},
)
