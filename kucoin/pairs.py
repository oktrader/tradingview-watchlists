import argparse
import requests

parser = argparse.ArgumentParser(description='Kucoin tickers')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()

    symbols = requests.get('https://api.kucoin.com/api/v1/symbols').json()['data']


    if args.quote_asset:
        symbols = filter(lambda x: x['quoteCurrency'] == args.quote_asset.upper(), symbols)
    symbols = map(lambda x: 'KUCOIN:{}'.format(x['name'].upper().replace('-', '').replace('/', '')), symbols)

    print(',\n'.join(sorted(symbols)))
