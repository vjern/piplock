from setuptools import setup, find_packages


setup(
    name = 'piplock',
    description = 'A minimal command-line tool to lock python requirements files',
    author = 'vjern',
    version = '0.1.0',
    # packages = find_packages(),
    py_modules = 'piplock',
    python_requires = '>=3.6',
    keywords = 'pip, dependency-locking',
    long_description = open('README.md').read(),
    long_description_content_type = 'text/markdown',
    license = 'MIT',
    url = 'https://github.com/vjern/piplock',
    entry_points = {
        'console_scripts': ['piplock=piplock.__main__:cli']
    }
)
