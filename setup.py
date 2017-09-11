from setuptools import setup

setup(
    name='deepl',
    version='0.1',
    description='Library and CLI for DeepL translator',
    author='Adrian Freund',
    author_email='mail@freundtech.com',
    url='https://github.com/freundTech/deepl-cli',
    license='MIT',
    packages=['deepl'],
    install_requires=["requests"],
    entry_points={
        "console_scripts": ["deepl=deepl.__main__:main"]
    }
)
