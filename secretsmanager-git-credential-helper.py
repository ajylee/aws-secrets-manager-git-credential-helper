#!/usr/bin/env python
"""
See description of argument parser
"""

import argparse
import json

import boto3

import subprocess as sbp

parser = argparse.ArgumentParser(description='''
Get git creds from secrets manager

Please configure git like in the following example, replacing "example.com", "us-east-1", and "accounts/github" as appropriate.
~~~
git config --global credential.https://example.com.helper "! $(realpath secretsmanager-git-credential-helper.py) https://example.com"

# custom config vars
git config --global aws-secrets-manager.https://example.com.region-name "us-east-1"
git config --global aws-secrets-manager.https://example.com.secret-id "accounts/github"
~~~

Store the git credentials in a JSON object with keys "username" and "password".
''')

parser.add_argument('url', action='store', help='URL of git repo, e.g. https://example.com')
subparsers = parser.add_subparsers(help='commands', dest='command')

parser_of_get = subparsers.add_parser('get')
parser_of_store = subparsers.add_parser('store')  # not applicable
parser_of_erase = subparsers.add_parser('erase')  # not applicable

args, unknown_args = parser.parse_known_args()


def get_credentials_key(key):
    return sbp.Popen(['git', 'config', '--get-urlmatch', f'aws-secrets-manager.{key}', args.url], stdout=sbp.PIPE).communicate()[0].decode().strip()


region_name = get_credentials_key('region-name')
secret_id = get_credentials_key('secret-id')

account = json.loads(
    boto3.Session(region_name=region_name).client('secretsmanager').get_secret_value(
        SecretId=secret_id,
    )['SecretString']
)

if args.command == 'get':
    print(f"""username={account['username']}""")
    print(f"""password={account['password']}""")
