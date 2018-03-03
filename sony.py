import argparse
import json

T = 600  # [us]
FREQ = 40  # [kHz]


def compose_ir_signal(product, function, repeat):
    data = [4, 1]  # leader
    for i in range(7):
        data.extend([1 << ((function >> i) & 1), 1])
    if not (product >> 5):
        product_bits = 5
    elif not (product >> 8):
        product_bits = 8
    else:
        product_bits = 13
    for i in range(product_bits):
        data.extend([1 << ((product >> i) & 1), 1])
    data[-1] += 75 - sum(data)
    data = [d * T for d in data]
    data = data * repeat
    return json.dumps({'format': 'us',
                       'freq': FREQ,
                       'data': data})


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='compose IR signal for SONY remote controller')
    parser.add_argument('function', help='function code')
    parser.add_argument('-p', '--product', default='0x0001',
                        help='product code')
    parser.add_argument('-r', '--repeat', type=int, default=4)
    args = parser.parse_args()
    print(compose_ir_signal(product=int(args.product, 16),
                            function=int(args.function, 16),
                            repeat=args.repeat))
