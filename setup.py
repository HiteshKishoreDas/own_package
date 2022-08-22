from setuptools import setup, find_packages

from own_package import __version__

setup(
    name='own_package',
    version=__version__,

    url='https://github.com/HiteshKishoreDas/own_package',
    author='Hitesh Kishore Das',
    author_email='dashiteshkishore@gmail.com',

    py_modules=find_packages(),

    install_requires=[
        'numpy == 1.21.2',
        'matplotlib == 3.3.4',
        'scipy == 1.7.1',
        'yt == 3.6.1',
    ],
)
