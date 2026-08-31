import argparse
import requests
from typing import List
from datetime import datetime

def get_bitfinex_symbols(margin: bool = False, quote_asset: str = None) -> List[str]:
    """Fetch and format Bitfinex trading symbols."""
    base_url = 'https://api-pub.bitfinex.com/v2/conf/pub:list:pair:'
    url = f"{base_url}{'margin' if margin else 'exchange'}"
    
    response = requests.get(url)
    response.raise_for_status()
    symbols = response.json()[0]
    
    if quote_asset:
        symbols = [s for s in symbols if s.endswith(quote_asset.upper())]
    
    formatted_symbols = [
        f"BITFINEX:{s.upper().replace(':', '')}"
        for s in symbols
    ]
    
    return sorted(formatted_symbols)

def save_to_file(symbols: List[str], market_type: str, quote_asset: str = None):
    """Save symbols to a file with specified format."""
    if not symbols:
        print(f"No trading pairs found for {market_type.upper()}" + 
              (f" with {quote_asset}" if quote_asset else ""))
        return
        
    current_date = datetime.now().strftime('%d-%b-%y').lower()
    asset_name = quote_asset if quote_asset else 'ALL'
    filename = f"bitfinex_{market_type}_{asset_name}_pairs_{current_date}.txt"
    
    with open(filename, 'w') as f:
        f.write(',\n'.join(symbols))
    
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Bitfinex tickers formatter')
    parser.add_argument('-q', '--quote-asset', help='Filter by quote asset (e.g., USD)')
    parser.add_argument('-m', '--margin', action='store_true', help='Show margin pairs only')
    
    args = parser.parse_args()
    
    try:
        symbols = get_bitfinex_symbols(args.margin, args.quote_asset)
        market_type = 'margin' if args.margin else 'spot'
        save_to_file(symbols, market_type, args.quote_asset)
        print(',\n'.join(symbols))
        
    except requests.RequestException as e:
        print(f"Error fetching data from Bitfinex API: {e}")
        exit(1)

if __name__ == "__main__":
    main()
