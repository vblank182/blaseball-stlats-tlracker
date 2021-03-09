import setuptools
from os import mkdir

dirs = ["./cache"]
for dir in dirs:
    try:
        mkdir(dir)
    except OSError:
        print (f'Creation of the directory `{dir}` failed.')
    else:
        print (f'Successfully created the directory `{dir}`.')

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
