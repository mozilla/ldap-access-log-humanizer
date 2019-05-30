# ldap-access-log-humanizer
A script to help make OpenLDAP access logs more readable for humans and machines

## Example
_____
This will convert LDAP access logs in this format:
```
Oct 26 03:30:53 ldap.example.com slapd[11086]: conn=6832973 fd=24 ACCEPT from IP=192.168.1.1:43050 (IP=0.0.0.0:389)
Oct 26 03:30:53 ldap.example.com slapd[11086]: conn=6832973 op=0 EXT oid=1.3.6.1.4.1.1466.20037 
Oct 26 03:30:53 ldap.example.com slapd[11086]: conn=6832973 op=0 STARTTLS 
Oct 26 03:30:53 ldap.example.com slapd[11086]: conn=6832973 op=0 RESULT oid= err=0 text=  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 fd=24 TLS established tls_ssf=256 ssf=256  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=1 BIND n="uid=bind-generateusers,ou=logins,dc=example" method=128  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=1 BIND dn="uid=bind-generateusers,ou=logins,dc=example" mech=SIMPLE ssf=0  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=1 RESULT tag=97 err=0 text=  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=2 SRCH base="ou=groups,dc=example" scope=2 deref=0 filter="(cn=group_name)"  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=2 SRCH attr=memberUid  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=2 SEARCH RESULT tag=101 err=0 nentries=1 text=  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=3 SRCH base="o=net,dc=example" scope=2 deref=0 filter="(objectClass=posixAccount)"  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=3 SRCH attr=sshPublicKey loginShell homeDirectory mail uidNumber uid  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=3 SEARCH RESULT tag=101 err=0 nentries=1626 text=  
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 op=4 UNBIND 
Oct 26 03:30:54 ldap.example.com slapd[11086]: conn=6832973 fd=24 closed  
```
to something that looks like this:

```
{'conn_id': '6832973', 'time': 'Oct 26 03:30:53', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': False, 'fd_id': 24, 'verb': 'ACCEPT', 'details': 'from IP=192.168.1.1:43050 (IP=0.0.0.0:389)'}
{'conn_id': '6832973', 'time': 'Oct 26 03:30:53', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': False, 'op_id': 0, 'requests': [{'verb': 'EXT', 'details': ['oid=1.3.6.1.4.1.1466.20037']}, {'verb': 'STARTTLS', 'details': []}], 'response': {'verb': 'RESULT', 'details': ['err=0', 'oid=', 'text='], 'error': 'LDAP_SUCCESS'}}
{'conn_id': '6832973', 'time': 'Oct 26 03:30:54', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': True, 'fd_id': 24, 'verb': 'TLS', 'details': 'established tls_ssf=256 ssf=256'}
{'conn_id': '6832973', 'time': 'Oct 26 03:30:54', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': True, 'op_id': 1, 'requests': [{'verb': 'BIND', 'details': ['dn="uid=bind-generateusers,ou=logins,dc=example"', 'method=128']}, {'verb': 'BIND', 'details': ['dn="uid=bind-generateusers,ou=logins,dc=example"', 'mech=SIMPLE', 'ssf=0']}], 'response': {'verb': 'RESULT', 'details': ['err=0', 'tag=97', 'text='], 'error': 'LDAP_SUCCESS'}}
{'conn_id': '6832973', 'time': 'Oct 26 03:30:54', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': True, 'op_id': 2, 'requests': [{'verb': 'SRCH', 'details': ['base="ou=groups,dc=example"', 'scope=2', 'deref=0', 'filter="(cn=group_name)"']}, {'verb': 'SRCH', 'details': ['attr=memberUid']}], 'response': {'verb': 'SEARCH RESULT', 'details': ['err=0', 'nentries=1', 'tag=101', 'text='], 'error': 'LDAP_SUCCESS'}}
{'conn_id': '6832973', 'time': 'Oct 26 03:30:54', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': True, 'op_id': 3, 'requests': [{'verb': 'SRCH', 'details': ['base="o=net,dc=example"', 'scope=2', 'deref=0', 'filter="(objectClass=posixAccount)"']}, {'verb': 'SRCH', 'details': ['attr=sshPublicKey', 'loginShell', 'homeDirectory', 'mail', 'uidNumber', 'uid']}], 'response': {'verb': 'SEARCH RESULT', 'details': ['err=0', 'nentries=1626', 'tag=101', 'text='], 'error': 'LDAP_SUCCESS'}}
{'conn_id': '6832973', 'time': 'Oct 26 03:30:54', 'client': '192.168.1.1', 'server': 'ldap.example.com', 'tls': True, 'fd_id': 24, 'verb': 'closed', 'details': ''}
```

which is more readable by humans and machines. The benefit to this format is that every operation gets its own line of log output, with all of the relevant metadata included on that line, such as connection number, whether TLS is used for this operation, the client IP, the request and the response.

## Usage
____
For testing purposes, use just the command line utility like this:
```
python run.py --noconfig --input_file_name /var/log/ldap/ldap.log --output_stdout
```
This will read the specified OpenLDAP log file and dump the humanized output to stdout

To start a syslog daemon:
```
python run.py --noconfig --input_type syslog --daemonize --host 0.0.0.0 --port 1514 --output_file /var/log/humanizer.log
```
This will open a listener on 0.0.0.0:1514 (udp) and accept syslog messages and write the humanized logs to the specified log file.

Quick and dirty:
```
cat /var/log/ldap/ldap.log | python run.py --noconfig --output_stdout
```

For production usage, use the humanizer_settings.json file to pass the configuration and use systemd or other tool to start the listener
## Supported inputs and outputs
___________________________
The humanizer can read logs via stdin, a specified file or from syslog over UDP.

The humanizer can output humanized logs to stdout, stderr, a specified file, forward to your MozDef server's events collector or forward to another syslog server. It can do any combination of output types, so you can have one instance write a local file, dump to stdout, stderr and forward the logs to syslog and MozDef, or any combination of these.
