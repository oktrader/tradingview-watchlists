import argparse
import requests

parser = argparse.ArgumentParser(description='Oanda tickers')
parser.add_argument('-t', '--type', action='store',
                    nargs='*', default=['currency', 'cfd', 'metal'])


if __name__ == "__main__":
    args = parser.parse_args()

    for inst_type in args.type:
        symbols = requests.post(
            'https://dashboard.acuitytrading.com/OandaPriceApi/GetPrices?apikey=4b12e6bb-7ecd-49f7-9bbc-2e03644ce41f&lang=en-GB',
            data={'lang': 'en-GB', 'region': 'OEL', 'instrumentType': inst_type}).json()
        symbols = map(lambda x: 'OANDA:{}'.format(
            x['Instrument'].replace('_', '')), symbols)
        print(',\n'.join(sorted(symbols)))
