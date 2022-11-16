from setuptools import setup, find_packages

from own_package import __version__

extra_athena = [
    'numpy == 1.21.2',
    'matplotlib >= 3.6',
    'scipy == 1.7.1',
    'yt == 3.6.1',
    'cmasher == 1.6.3',
    'lic',
]

extra_data_analysis= [
    *extra_athena,
    'structure-tensor'
]


extra_plot = [
    *extra_athena,
]

extra_pluto= [
    *extra_athena,
]

extra_test= [
    *extra_athena,
    'pytest>=4',
    'pytest-cov>=2',
]

extra_dev = [
    *extra_test,
]

setup(
    name='own_package',
    version=__version__,

    url='https://github.com/HiteshKishoreDas/own_package',
    author='Hitesh Kishore Das',
    author_email='dashiteshkishore@gmail.com',

    py_modules=find_packages(),

    extras_require={
        'athena': extra_athena,
        'data_analysis': extra_data_analysis,
        'dev': extra_dev,
        'plot': extra_plot,
        'pluto': extra_pluto,
        'test': extra_test,

    },
)
