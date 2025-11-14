# Automated TradingView watchlists

| Source | Status |
| --- | --- |
| Binance | ![Binance](https://github.com/oktrader/tradingview-watchlists/workflows/Binance/badge.svg) |
| Bitfinex | ![Bitfinex](https://github.com/oktrader/tradingview-watchlists/workflows/Bitfinex/badge.svg) |
| Bybit | ![Bybit](https://github.com/oktrader/tradingview-watchlists/workflows/Bybit/badge.svg) |
| Forex | ![Forex](https://github.com/oktrader/tradingview-watchlists/workflows/FX/badge.svg) |
| Huobi | ![Huobi](https://github.com/oktrader/tradingview-watchlists/workflows/Huobi/badge.svg) |
| Stocks | ![Stocks](https://github.com/oktrader/tradingview-watchlists/workflows/Stocks/badge.svg) |

## Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt
```

### Running Scripts
```bash
# Binance spot
python binance/pairs.py -q USDT > binance/binance_USDT_pairs.txt

# Binance futures
python binance/pairs.py -f > binance/binance_futures.txt

# Bybit
python bybit/pairs.py -q USD > bybit/bybit_USD_futures.txt

# Other exchanges follow the same pattern
python bitfinex/pairs.py
python huobi/pairs.py
python kucoin/pairs.py
python forex/oanda.py
python stocks/nasdaqtrader.py
```

## Troubleshooting

### HTTP 451 / Geolocation Blocks

If workflows fail with `451 Client Error` (Unavailable For Legal Reasons), the exchange API is blocking the GitHub runner's IP region.

**Workaround:** Use an HTTP proxy via environment variables:
```bash
# For GitHub Actions, set these secrets in your repo settings, then reference in workflows:
export HTTP_PROXY=http://your-proxy:port
export HTTPS_PROXY=http://your-proxy:port
python binance/pairs.py > output.txt
```

**Alternative:** Override the API endpoint:
```bash
export BINANCE_API=https://alternative-binance-endpoint.com/api/v1/exchangeInfo
python binance/pairs.py > output.txt
```

Available environment variable overrides:
- `BINANCE_API` – Spot API URL (default: `https://api.binance.com/api/v1/exchangeInfo`)
- `BINANCE_FUTURES_API` – Futures API URL (default: `https://fapi.binance.com/fapi/v1/exchangeInfo`)
- `BYBIT_API` – Bybit API URL
- `HUOBI_API` – Huobi API URL
- `KUCOIN_API` – KuCoin API URL
- `OANDA_API` – Oanda API URL
- `HTTP_PROXY` / `HTTPS_PROXY` – Proxy servers for all requests

