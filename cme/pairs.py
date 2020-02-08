import argparse
import requests

parser = argparse.ArgumentParser(description='TV tickers')
parser.add_argument('-e', '--exchange')


if __name__ == "__main__":
    args = parser.parse_args()

    symbols = requests.get(f'https://symbol-search.tradingview.com/symbol_search/?exchange={args.exchange.upper()}&type=&hl=true&lang=en&domain=production').json()
    symbols = map(lambda x: '{}:{}'.format(args.exchange.upper(), x['contracts'][0]['symbol']), symbols)
    print(',\n'.join(symbols))
