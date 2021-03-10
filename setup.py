import setuptools
import os
from sys import exit


dirs = ["cache"]
cwd = os.getcwd()
for dir in dirs:
    abs_dir = os.path.join(cwd, dir)
    if not os.path.exists(abs_dir):
        os.mkdir(abs_dir)


install_requires = [
    'requests',
    'urllib3',
    ]

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
