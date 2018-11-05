try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '',
    'author': '',
    'url': '',
    'download_url': '',
    'author_email': 'jdow@mozilla, jclaudius@mozilla.com',
    'version': "0.0.1",
    'install_requires': [],
    'packages': ['humanizer'],
    'scripts': [],
    'name': 'humanizer'
}

setup(**config)
