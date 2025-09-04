try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Exercise 46 Project',
    'author': 'Your Name',
    'url': 'http://example.com',
    'download_url': 'http://example.com/download',
    'author_email': 'you@example.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['ex46module'],  # Change this to whatever your module folder is
    'scripts': [],
    'name': 'ex46'
}

setup(**config)

