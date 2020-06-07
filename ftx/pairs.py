import argparse
import requests

parser = argparse.ArgumentParser(description='FTX tickers')
parser.add_argument('-q', '--quote-asset')
parser.add_argument('-f', '--futures', action='store_true')
parser.add_argument('-s', '--spot', action='store_true')
parser.add_argument('-p', '--perps', action='store_true')


if __name__ == "__main__":
    args = parser.parse_args()

    symbols = requests.get('https://ftx.com/api/markets').json()['result']

    if args.futures:
        symbols = filter(lambda x: x['type'] == 'future', symbols)
    if args.spot:
        symbols = filter(lambda x: x['type'] == 'spot', symbols)
    if args.perps:
        symbols = filter(lambda x: x['type'] =='future' and x['name'].endswith('PERP'), symbols)

    symbols = map(lambda x: 'FTX:{}'.format(x['name'].upper().replace('-', '').replace('/', '')), symbols)

    print(',\n'.join(sorted(symbols)))
