import setuptools
from sys import exit

install_requires = []  # dependencies satisfied through requirements.txt

setuptools.setup(
    name='blaseball-stlats-tlracker',
    version='0.1',
    description='Blaseball Stlats Tlracker',
    url='https://github.com/vblank182/blaseball-stlats-tlracker',
    author='Jesse Williams',
    author_email='',
    license='GNU GPLv3',
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
