import argparse
import subprocess
import sys

import requests


def send_ir(ip_address, signal_format, rest_args):
    data = subprocess.check_output(
        [sys.executable, '-m', signal_format] + rest_args)
    requests.post('http://{}/messages'.format(ip_address),
                  data=data,
                  headers={'X-Requested-With': 'requests'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='send IR signal to Nature Remo via Local API')
    parser.add_argument('ip_address', help='IP address of Nature Remo')
    parser.add_argument('signal_format', help='IR signal format (aeha|sony)')
    parser.add_argument('args', nargs='*')
    args = parser.parse_args()
    send_ir(ip_address=args.ip_address, signal_format=args.signal_format,
            rest_args=args.args)
