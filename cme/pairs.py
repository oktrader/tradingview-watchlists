import sys
import argparse
from string import ascii_uppercase
import requests


parser = argparse.ArgumentParser(description='TV tickers')
parser.add_argument('-e', '--exchange')


if __name__ == "__main__":
    args = parser.parse_args()

    all_symbols = []
    for c in ascii_uppercase:
        symbols = requests.get(f'https://symbol-search.tradingview.com/symbol_search/', params={
            'exchange': args.exchange.upper(),
            'lang': 'en',
            'domain': 'production',
            'text': c
        }).json()
        symbols = list(map(lambda x: '{}:{}'.format(args.exchange.upper(), x['contracts'][0]['symbol']), symbols))

        if len(symbols) >= 50:
            print(f'{c} has more than 50 symbols', file=sys.stderr) # TODO fix this

        all_symbols.extend(symbols)

    print(',\n'.join(sorted(all_symbols)))
