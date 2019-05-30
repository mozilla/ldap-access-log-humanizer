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
    'packages': ['ldap-access-log-humanizer'],
    'scripts': ['humanizer.py'],
    'data_files': [('etc/humanizer', ['humanizer_settings.json.default'])],
    'name': 'humanizer'
}

setup(**config)
