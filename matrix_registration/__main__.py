# Standard library imports...
import argparse
import sys
import logging

# Local imports...
from . import config
from . import tokens
from .api import app

parser = argparse.ArgumentParser(
    description='a token based Matrix-registration api',
    prog='python -m matrix_registration')
parser.add_argument('-c', '--config', type=str, default='config.yaml',
                    metavar='<path>', help='the path to your config file')
parser.add_argument('mode', choices=['api', 'token'],
                    help='start as api server or generate new token')
parser.add_argument('-o', '--one-time', type=bool, default=False,
                    help='one time use token')
parser.add_argument('-e', '--expire', type=str, default=None,
                    help='expiration date for token')
parser.add_argument('-d', '--disable', type=str, default=None,
                    help='disable token')
args = parser.parse_args()

config.config = config.Config(args.config)
tokens.tokens = tokens.Tokens()

if args.mode == 'api':
    app.run(host='0.0.0.0', port=config.config.PORT)
elif args.mode == 'token':
    if args.disable:
        disabled = tokens.tokens.disable(args.disable)
        if disabled:
            print("token has been disabled")
        else:
            print("token was already disabled")
    else:
        token = tokens.tokens.new(expire=args.expire, one_time=args.one_time)
        print(token.name)
