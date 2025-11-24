import argparse
import requests
import sys
import time
import os

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def fetch_with_retry(url, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Fetch URL with exponential backoff retry on failure."""
    # Optional proxy support via environment variables
    proxies = None
    if os.getenv('HTTP_PROXY') or os.getenv('HTTPS_PROXY'):
        proxies = {
            'http': os.getenv('HTTP_PROXY'),
            'https': os.getenv('HTTPS_PROXY', os.getenv('HTTP_PROXY'))
        }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10, proxies=proxies)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as e:
            if attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}", file=sys.stderr)
                raise

parser = argparse.ArgumentParser(description="Bybit tickers")
parser.add_argument("-q", "--quote-asset")

if __name__ == "__main__":
    args = parser.parse_args()

    try:
        # Bybit v5 API - get spot market tickers
        url = os.getenv('BYBIT_API', "https://api.bybit.com/v5/market/tickers?category=spot")
        data = fetch_with_retry(url)
        
        # v5 API returns: { retCode, retMsg, result: { category, list: [...] }, ... }
        if 'result' not in data or 'list' not in data['result']:
            raise KeyError(f"Unexpected API response structure: {list(data.keys())}")
        
        symbols = [item['symbol'] for item in data['result']['list']]

        if args.quote_asset:
            symbols = [s for s in symbols if s.endswith(args.quote_asset.upper())]

        symbols_list = [f"BYBIT:{s.upper()}" for s in symbols]

        print(",\n".join(sorted(symbols_list)))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
