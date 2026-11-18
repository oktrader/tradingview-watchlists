import argparse
import requests
from typing import List
from datetime import datetime

def get_bybit_symbols(quote_asset: str = None) -> List[str]:
    """Fetch and format Bybit trading symbols."""
    # Using the production API instead of testnet
    url = 'https://api.bybit.com/v5/market/tickers'
    params = {'category': 'spot'}  # You can modify category as needed: spot, linear, inverse
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    symbols = [item['symbol'] for item in response.json()['result']['list']]

    if quote_asset:
        symbols = [s for s in symbols if s.endswith(quote_asset.upper())]
    
    formatted_symbols = [
        f"BYBIT:{s.upper().replace(':', '')}"
        for s in symbols
    ]
    
    return sorted(formatted_symbols)

def save_to_file(symbols: List[str], quote_asset: str = None):
    """Save symbols to a file with specified format."""
    current_date = datetime.now().strftime('%d-%b-%y').lower()
    asset_name = quote_asset.upper() if quote_asset else 'ALL'
    filename = f"bybit_{asset_name}_pairs_{current_date}.txt"
    
    with open(filename, 'w') as f:
        f.write(',\n'.join(symbols))
    
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Bybit tickers formatter')
    parser.add_argument('-q', '--quote-asset', help='Filter by quote asset (e.g., USDT)')
    
    args = parser.parse_args()
    
    try:
        symbols = get_bybit_symbols(args.quote_asset)
        print(',\n'.join(symbols))
        save_to_file(symbols, args.quote_asset)
    except requests.RequestException as e:
        print(f"Error fetching data from Bybit API: {e}")
        exit(1)

if __name__ == "__main__":
    main()
