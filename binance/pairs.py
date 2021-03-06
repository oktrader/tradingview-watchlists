import argparse
import requests

parser = argparse.ArgumentParser(description='Binance tickers')
parser.add_argument('-m', '--margin', action='store_true')
parser.add_argument('-f', '--futures', action='store_true')
parser.add_argument('-q', '--quote-asset')

if __name__ == "__main__":
    args = parser.parse_args()

    if args.futures:
        symbols = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo').json()['symbols']
        symbols = map(lambda x: 'BINANCE:{}PERP'.format(x['symbol']), symbols)
        print(',\n'.join(sorted(symbols)))
    else:
        symbols = filter(lambda x: x['status'] == 'TRADING', requests.get('https://api.binance.com/api/v1/exchangeInfo').json()['symbols'])
        if args.margin:
            symbols = filter(lambda x: x['isMarginTradingAllowed'], symbols)
        if args.quote_asset:
            symbols = filter(lambda x: x['quoteAsset'] == args.quote_asset, symbols)
        symbols = map(lambda x: 'BINANCE:{}'.format(x['symbol']), symbols)
        print(',\n'.join(sorted(symbols)))
