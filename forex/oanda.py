import argparse
import requests
from typing import List
from datetime import datetime

def get_and_save_oanda_symbols(instrument_type: str):
    """Fetch, format and save Oanda trading symbols for a specific instrument type."""
    symbols = requests.post(
        'https://dashboard.acuitytrading.com/OandaPriceApi/GetPrices?apikey=4b12e6bb-7ecd-49f7-9bbc-2e03644ce41f&lang=en-GB',
        data={'lang': 'en-GB', 'region': 'OEL', 'instrumentType': instrument_type}
    ).json()
    
    formatted_symbols = [
        f"OANDA:{x['Instrument'].replace('_', '')}"
        for x in symbols
    ]
    
    # Save to file
    current_date = datetime.now().strftime('%d-%b-%y').lower()
    filename = f"oanda_{instrument_type}_pairs_{current_date}.txt"
    
    with open(filename, 'w') as f:
        f.write(',\n'.join(sorted(formatted_symbols)))
    
    print(f"Saved {instrument_type} pairs to {filename}")
    return sorted(formatted_symbols)

def main():
    parser = argparse.ArgumentParser(description='Oanda tickers formatter')
    parser.add_argument('-t', '--type', 
                       nargs='*', 
                       default=['currency', 'cfd', 'metal'],
                       help='Instrument types to fetch')
    
    args = parser.parse_args()
    
    for inst_type in args.type:
        symbols = get_and_save_oanda_symbols(inst_type)
        print(f"\n{inst_type.upper()} Pairs:")
        print(',\n'.join(symbols))
        print("\n")

if __name__ == "__main__":
    main()
