import argparse
import requests

parser = argparse.ArgumentParser(description='Binance tickers')
parser.add_argument('-m', '--margin', action='store_true')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()

    symbols = requests.get('https://api.binance.com/api/v1/exchangeInfo').json()['symbols']

    if args.margin:
        symbols = filter(lambda x: x['isMarginTradingAllowed'], symbols)
    
    if args.quote_asset:
        symbols = filter(lambda x: x['quoteAsset'] == args.quote_asset, symbols)

    symbols = map(lambda x: 'BINANCE:{}'.format(x['symbol']), symbols)

    print(',\n'.join(symbols))
