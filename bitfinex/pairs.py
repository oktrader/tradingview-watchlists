import argparse
import requests
import sys
import time

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def fetch_with_retry(url, max_retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Fetch URL with exponential backoff retry on failure."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
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

parser = argparse.ArgumentParser(description='Bitfinex tickers')
parser.add_argument('-q', '--quote-asset')
parser.add_argument('-m', '--margin', action='store_true')

if __name__ == "__main__":
    args = parser.parse_args()

    try:
        url = 'https://api-pub.bitfinex.com/v2/conf/pub:list:pair:exchange'
        if args.margin:
            url = 'https://api-pub.bitfinex.com/v2/conf/pub:list:pair:margin'

        data = fetch_with_retry(url)
        if not isinstance(data, list) or len(data) == 0:
            raise ValueError(f"Unexpected API response format: {data}")
        symbols = data[0]
       
        if args.quote_asset:
            symbols = filter(lambda x: x.endswith(args.quote_asset.upper()), symbols)

        symbols = map(lambda x: 'BITFINEX:{}'.format(x.upper().replace(':', '')), symbols)

        print(',\n'.join(sorted(symbols)))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
