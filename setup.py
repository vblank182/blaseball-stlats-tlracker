import setuptools

install_requires = [
    'requests',
    'urllib3',
    ]

setuptools.setup(
    name='blaseball_stlats_tlracker',
    version='0.1',
    description='Blaseball Stlats Tlracker',
    url='https://github.com/vblank182/blaseball-stlats-tlracker',
    author='Jesse Williams',
    author_email='',
    license='GNU GPLv3',
    packages=setuptools.find_packages(),
    install_requires=install_requires
)
