from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='deepl',
    version='0.2',
    description='Library and CLI for DeepL translator',
    long_description=long_description,
    author='Adrian Freund',
    author_email='mail@freundtech.com',
    url='https://github.com/freundTech/deepl-cli',
    license='MIT',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
    ],
    keywords='translation deepl cli',
    packages=find_packages(include=['deepl']),
    install_requires=["requests"],
    python_requires='>=3',
    entry_points={
        "console_scripts": ["deepl=deepl.__main__:main"]
    },
    test_suite="test"
)
