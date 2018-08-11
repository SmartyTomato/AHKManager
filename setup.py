from setuptools import setup

readme = open('README.md').read()

setup(
    name='AHKManager',
    version='1.0',
    packages=['AHKManager'],
    url='https://github.com/SmartyTomato/AHKManager',
    license='GNU General Public License v3.0',
    author='Tommy Zhao',
    author_email='smartytomato@hotmail.com',
    description='AutoHotKey manager',
    long_description=readme, install_requires=['PyQt5'],
)
