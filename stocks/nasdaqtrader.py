
from ftplib import FTP, all_errors
from io import BytesIO, TextIOWrapper
import argparse
import sys
import time

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def ftp_with_retry(host, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Connect to FTP with retry on failure."""
    for attempt in range(max_retries):
        try:
            ftp = FTP(host, timeout=10)
            ftp.login()
            return ftp
        except all_errors as e:
            if attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}", file=sys.stderr)
                raise

parser = argparse.ArgumentParser(description='Nasdaq stocks')
parser.add_argument('-nq', '--nasdaq', action='store_true')
parser.add_argument('-nyse', '--nyse', action='store_true')
parser.add_argument('-arca', '--arca', action='store_true')
parser.add_argument('-etfs', '--etfs', action='store_true')

exchanges = {
    'N': 'NYSE',
    'P': 'ARCA'
}

if __name__ == "__main__":
    args = parser.parse_args()

    try:
        ftp = ftp_with_retry('ftp.nasdaqtrader.com')
        
        if args.nasdaq:
            r = BytesIO()
            ftp.retrbinary('RETR /SymbolDirectory/nasdaqlisted.txt', r.write)
            r.seek(0)
            wrapper = TextIOWrapper(r, encoding='utf-8')

            for line in wrapper:
                ticker, name, market_cat, is_test, status, lot_size, x, y = line.split('|')
                if is_test == 'N':
                    print('NASDAQ:{}'.format(ticker))

        if args.nyse or args.arca:
            r = BytesIO()
            ftp.retrbinary('RETR /SymbolDirectory/otherlisted.txt', r.write)
            r.seek(0)
            wrapper = TextIOWrapper(r, encoding='utf-8')

            for line in wrapper:
                line_split = line.split('|')
                
                ticker = line_split[0]
                exchange = line_split[2]
                is_etf = line_split[4]
                is_test = line_split[6]

                if is_test == 'Y':
                    continue

                if is_etf == 'Y' and not args.etfs:
                    continue

                if '$' in ticker or '.' in ticker:
                    continue

                if exchange in exchanges:
                    print('{}:{}'.format(exchanges[exchange], ticker))
        
        ftp.quit()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)