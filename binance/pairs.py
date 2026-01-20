import argparse
import requests
from typing import List
from datetime import datetime
import sys

def get_futures_symbols() -> List[str]:
    """Fetch Binance futures trading symbols."""
    response = requests.get('https://fapi.binance.com/fapi/v1/exchangeInfo')
    response.raise_for_status()
    symbols = response.json()['symbols']
    return [f'BINANCE:{s["symbol"]}PERP' for s in symbols]

def get_spot_symbols(margin: bool = False, quote_asset: str = None) -> List[str]:
    """Fetch Binance spot trading symbols."""
    response = requests.get('https://api.binance.com/api/v1/exchangeInfo')
    response.raise_for_status()
    symbols = [s for s in response.json()['symbols'] if s['status'] == 'TRADING']
    
    if margin:
        symbols = [s for s in symbols if s['isMarginTradingAllowed']]
    if quote_asset:
        symbols = [s for s in symbols if s['quoteAsset'] == quote_asset]
    
    return [f'BINANCE:{s["symbol"]}' for s in symbols]

def save_to_file(symbols: List[str], market_type: str, quote_asset: str = None):
    """Save symbols to a file."""
    if not symbols:
        print(f"No trading pairs found for {market_type.upper()}" + 
              (f" with {quote_asset}" if quote_asset else ""))
        sys.exit(1)
        
    current_date = datetime.now().strftime('%d-%b-%y').lower()
    asset_name = quote_asset if quote_asset else 'ALL'
    filename = f"binance_{market_type}_{asset_name}_pairs_{current_date}.txt"
    
    with open(filename, 'w') as f:
        f.write(',\n'.join(sorted(symbols)))
    
    print(f"Results saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Binance tickers formatter')
    parser.add_argument('-m', '--margin', action='store_true', help='Show margin pairs only')
    parser.add_argument('-f', '--futures', action='store_true', help='Show futures pairs')
    parser.add_argument('-q', '--quote-asset', help='Filter by quote asset (e.g., USDT)')
    
    args = parser.parse_args()
    
    try:
        if args.futures:
            symbols = get_futures_symbols()
            save_to_file(symbols, 'futures')
        else:
            symbols = get_spot_symbols(args.margin, args.quote_asset)
            market_type = 'margin' if args.margin else 'spot'
            save_to_file(symbols, market_type, args.quote_asset)
        
        print(',\n'.join(sorted(symbols)))
        
    except requests.RequestException as e:
        print(f"Error fetching data from Binance API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
