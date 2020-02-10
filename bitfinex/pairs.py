import argparse
import requests

parser = argparse.ArgumentParser(description='Bitfinex tickers')
parser.add_argument('-q', '--quote-asset')
parser.add_argument('-m', '--margin', action='store_true')

if __name__ == "__main__":
    args = parser.parse_args()

    url = 'https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange'
    if args.margin:
        url = 'https://api-pub.bitfinex.com/v2/conf/pub:list:pair:margin'

    symbols = requests.get(url).json()[0]
   
    if args.quote_asset:
        symbols = filter(lambda x: x.endswith(args.quote_asset.upper()), symbols)

    symbols = map(lambda x: 'BITFINEX:{}'.format(x.upper().replace(':', '')), symbols)

    print(',\n'.join(sorted(symbols)))
