import argparse
import json

T = 425  # [us]
FREQ = 38  # [kHz]


def compose_ir_signal(vendor, command, trailer, repeat):
    data = [8, 4]  # leader
    for j in range(2):
        v = (vendor >> 8 * (1 - j)) & 0xff
        for i in range(8):
            data.extend([1, 1 + 2 * ((v >> i) & 1)])
    for c in command:
        for i in range(8):
            data.extend([1, 1 + 2 * ((c >> i) & 1)])
    data = [d * T for d in data]
    data.extend([T, trailer])
    while data[-1] > 65535:
        remainder = data[-1] - 65535
        data[-1] = 65535
        data.extend([0, remainder])
    data *= repeat
    return json.dumps({'format': 'us',
                       'freq': FREQ,
                       'data': data},
                      separators=(',', ':'))


if __name__ == '__main__':
    'compose IR signal in AEHA format'
    parser = argparse.ArgumentParser(
        description='compose IR signal for SONY remote controller')
    parser.add_argument('-r', '--repeat', type=int, default=2)
    parser.add_argument('-t', '--trailer', type=int, default=75000)
    parser.add_argument('vendor', help='vendor code')
    parser.add_argument('command', nargs='*')
    args = parser.parse_args()
    print(compose_ir_signal(vendor=int(args.vendor, 16),
                            command=[int(c, 16) for c in args.command],
                            trailer=args.trailer,
                            repeat=args.repeat))
