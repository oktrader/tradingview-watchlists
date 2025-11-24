import argparse
import requests
import sys
import time
import os

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def fetch_with_retry(url, method='get', data=None, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
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
            if method == 'post':
                response = requests.post(url, data=data, timeout=10, proxies=proxies)
            else:
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

parser = argparse.ArgumentParser(description='Oanda tickers')
parser.add_argument('-t', '--type', action='store',
                    nargs='*', default=['currency', 'cfd', 'metal'])


if __name__ == "__main__":
    args = parser.parse_args()

    try:
        url = os.getenv('OANDA_API', 
            'https://dashboard.acuitytrading.com/OandaPriceApi/GetPrices?apikey=4b12e6bb-7ecd-49f7-9bbc-2e03644ce41f&lang=en-GB')
        for inst_type in args.type:
            data = fetch_with_retry(
                url,
                method='post',
                data={'lang': 'en-GB', 'region': 'OEL', 'instrumentType': inst_type})
            if not isinstance(data, list):
                raise ValueError(f"Unexpected API response format: {data}")
            symbols = map(lambda x: 'OANDA:{}'.format(
                x['Instrument'].replace('_', '')), data)
            print(',\n'.join(sorted(symbols)))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
