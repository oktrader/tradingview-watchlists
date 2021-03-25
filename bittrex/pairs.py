import argparse
import requests

parser = argparse.ArgumentParser(description='Bittrex tickers')
parser.add_argument('-q', '--quote-asset')
parser.add_argument('-s', '--stocks', action='store_true')

if __name__ == "__main__":
    args = parser.parse_args()

    symbols = requests.get('https://api.bittrex.com/v3/markets').json()
    symbols = filter(lambda x: x['status'] == 'ONLINE', symbols)
   
    if args.quote_asset:
        symbols = filter(lambda x: x['quoteCurrencySymbol'] == args.quote_asset.upper(), symbols)
    if args.stocks:
        symbols = filter(lambda x: 'TOKENIZED_SECURITY' in x['tags'], symbols)
    else:
        symbols = filter(lambda x: 'TOKENIZED_SECURITY' not in x['tags'], symbols)

    symbols = map(lambda x: 'BITTREX:{}'.format(x['symbol'].replace('-', '')), symbols)

    print(',\n'.join(symbols))
