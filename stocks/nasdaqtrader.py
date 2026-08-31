from ftplib import FTP
from io import BytesIO, TextIOWrapper
import argparse
from datetime import datetime
from typing import List, Dict

EXCHANGES = {
    'N': 'NYSE',
    'P': 'ARCA'
}

def get_nasdaq_stocks() -> List[str]:
    """Fetch NASDAQ listed stocks."""
    stocks = []
    with BytesIO() as r:
        ftp.retrbinary('RETR /SymbolDirectory/nasdaqlisted.txt', r.write)
        r.seek(0)
        wrapper = TextIOWrapper(r, encoding='utf-8')
        
        for line in wrapper:
            ticker, name, market_cat, is_test, status, lot_size, x, y = line.split('|')
            if is_test == 'N':
                stocks.append(f'NASDAQ:{ticker}')
    return sorted(stocks)

def get_other_stocks(include_etfs: bool) -> Dict[str, List[str]]:
    """Fetch NYSE and ARCA stocks."""
    exchange_stocks = {'NYSE': [], 'ARCA': []}
    
    with BytesIO() as r:
        ftp.retrbinary('RETR /SymbolDirectory/otherlisted.txt', r.write)
        r.seek(0)
        wrapper = TextIOWrapper(r, encoding='utf-8')
        
        for line in wrapper:
            line_split = line.split('|')
            ticker = line_split[0]
            exchange = line_split[2]
            is_etf = line_split[4]
            is_test = line_split[6]
            
            if is_test == 'Y' or '$' in ticker or '.' in ticker:
                continue
                
            if is_etf == 'Y' and not include_etfs:
                continue
                
            if exchange in EXCHANGES:
                exchange_stocks[EXCHANGES[exchange]].append(f'{EXCHANGES[exchange]}:{ticker}')
    
    return {k: sorted(v) for k, v in exchange_stocks.items()}

def save_to_file(symbols: List[str], exchange: str):
    """Save symbols to a file."""
    current_date = datetime.now().strftime('%d-%b-%y').lower()
    filename = f"{exchange.lower()}_stocks_{current_date}.txt"
    
    with open(filename, 'w') as f:
        f.write(',\n'.join(symbols))
    
    print(f"Saved {exchange} stocks to {filename}")

def main():
    parser = argparse.ArgumentParser(description='Nasdaq stocks downloader')
    parser.add_argument('-nq', '--nasdaq', action='store_true', help='Download NASDAQ stocks')
    parser.add_argument('-nyse', '--nyse', action='store_true', help='Download NYSE stocks')
    parser.add_argument('-arca', '--arca', action='store_true', help='Download ARCA stocks')
    parser.add_argument('-etfs', '--etfs', action='store_true', help='Include ETFs')
    
    args = parser.parse_args()
    
    global ftp
    ftp = FTP('ftp.nasdaqtrader.com')
    ftp.login()
    
    try:
        if args.nasdaq:
            nasdaq_stocks = get_nasdaq_stocks()
            save_to_file(nasdaq_stocks, 'NASDAQ')
            print('\n'.join(nasdaq_stocks))
            
        if args.nyse or args.arca:
            other_stocks = get_other_stocks(args.etfs)
            
            if args.nyse:
                save_to_file(other_stocks['NYSE'], 'NYSE')
                print('\n'.join(other_stocks['NYSE']))
                
            if args.arca:
                save_to_file(other_stocks['ARCA'], 'ARCA')
                print('\n'.join(other_stocks['ARCA']))
                
    finally:
        ftp.quit()

if __name__ == "__main__":
    main()
