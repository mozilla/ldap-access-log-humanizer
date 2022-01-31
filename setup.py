''' Packaging setup '''

import os
import subprocess
from setuptools import setup

NAME = 'ldap-access-log-humanizer'
VERSION = '0.0.3'

def git_version():
    ''' Return the git revision as a string '''
    def _minimal_ext_cmd(cmd):
        # construct minimal environment
        env = {}
        for envvar in ['SYSTEMROOT', 'PATH']:
            val = os.environ.get(envvar)
            if val is not None:
                env[envvar] = val
        # LANGUAGE is used on win32
        env['LANGUAGE'] = 'C'
        env['LANG'] = 'C'
        env['LC_ALL'] = 'C'
        out = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                               env=env).communicate()[0]
        return out

    try:
        out = _minimal_ext_cmd(['git', 'rev-parse', 'HEAD'])
        git_revision = out.strip().decode('ascii')
    except OSError:
        git_revision = u"Unknown"

    return git_revision

setup(
    name=NAME,
    packages=[NAME.replace('-','_')],
    version=VERSION,
    author='',
    author_email='secops@mozilla.com',
    description=('Make OpenLDAP access logs more readable for humans and machines\n' +
                 'This package is built upon commit ' + git_version()),
    license='MPL',
    url='https://github.com/mozilla/ldap-access-log-humanizer',
    install_requires=['requests'],
    scripts=['humanizer.py'],
    data_files=[('/etc/humanizer', ['humanizer_settings.json.default']),
        ('/usr/lib/systemd/system', ['humanizer.service']),
        ('/etc/logrotate.d/', ['humanizer-logrotate']),
        ('/etc/rsyslog.d/', ['humanizer-rsyslog.conf'])],
)
