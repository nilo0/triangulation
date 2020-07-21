from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='triangulation',
    version='0.0',
    description='',
    long_description=read('README.md'),
    url='https://github.com/nilo0/triangulation',
    keywords=['Triangulation', 'Delaunay'],
    author='Niloofar Rahmati',
    author_email='nilo0far@zedat.fu-berlin.de',
    license='GPLv3',
    packages=['triangulation'],
    install_requires=[
        'numpy',
        'scipy',
        'plotly',
        'requests',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    zip_safe=False
)
