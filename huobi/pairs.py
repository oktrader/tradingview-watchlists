import argparse
import requests

parser = argparse.ArgumentParser(description='Huobi tickers')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()

    symbols = requests.get('https://api.huobi.pro/v1/common/symbols').json()['data']
   
    if args.quote_asset:
        symbols = filter(lambda x: x['quote-currency'] == args.quote_asset.lower(), symbols)

    symbols = map(lambda x: 'HUOBI:{}'.format(x['symbol'].upper()), symbols)

    print(',\n'.join(sorted(symbols)))
