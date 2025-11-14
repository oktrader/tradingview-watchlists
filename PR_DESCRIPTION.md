# CI/CD Improvements & Resilience Enhancements

## Summary
This PR consolidates significant CI/CD improvements to make the watchlist generation pipeline more reliable, maintainable, and resilient to transient API failures and geolocation blocks.

## Changes

### 1. **Centralized Dependency Management**
- ✅ Added `requirements.txt` with pinned `requests==2.31.0`
- Eliminates scattered `pip install` commands across workflows
- Single source of truth for Python dependencies

### 2. **Reusable Composite Action**
- ✅ Created `.github/actions/setup-python-deps/action.yml`
- DRY principle: replaces duplicated setup steps across 7 workflows
- Supports configurable Python version and requirements file
- Easy to maintain and upgrade in one place

### 3. **Enhanced Exchange Scripts with Retry Logic**
- ✅ Added exponential backoff retry (2s, 4s, 8s delays; max 3 attempts)
- ✅ Added 10s timeout per request
- ✅ Added API response validation before processing
- ✅ Added comprehensive error logging to stderr
- ✅ Graceful exit(1) on fatal errors
- **Affected files:**
  - `binance/pairs.py`
  - `bybit/pairs.py` (also migrated v2 → v5 API endpoint)
  - `bitfinex/pairs.py`
  - `huobi/pairs.py`
  - `kucoin/pairs.py`
  - `forex/oanda.py`
  - `stocks/nasdaqtrader.py`

### 4. **Proxy & Environment Variable Support**
- ✅ Added HTTP proxy support via `HTTP_PROXY` / `HTTPS_PROXY` env vars
- ✅ Added API endpoint override env vars:
  - `BINANCE_API`, `BINANCE_FUTURES_API`
  - `BYBIT_API`, `HUOBI_API`, `KUCOIN_API`, `OANDA_API`
- Allows circumventing geolocation blocks and API migrations without code changes

### 5. **Updated Workflows**
- ✅ All 7 exchange workflows now use composite action
- ✅ Added `workflow_dispatch` trigger for manual testing
- **Workflows:** `binance.yaml`, `bybit.yaml`, `bitfinex.yaml`, `huobi.yaml`, `kucoin.yaml`, `forex.yaml`, `stocks.yaml`

### 6. **API Endpoint Migration**
- ✅ **Bybit:** Migrated from deprecated v2 endpoint (`/v2/public/symbols`) to v5 (`/v5/market/tickers?category=spot`)
- Updated response parsing for v5 structure

### 7. **Documentation**
- ✅ Created `.github/copilot-instructions.md` for AI agent guidance
- ✅ Updated `README.md` with:
  - "Local Development" section (setup & examples)
  - "Troubleshooting" section (geolocation blocks, proxy setup, env var reference)

## Known Issues & Limitations

### Geolocation Blocks
- **Binance & Bybit** may return HTTP 451 (Unavailable For Legal Reasons) depending on GitHub runner location
- **Workaround:** Set `HTTP_PROXY` / `HTTPS_PROXY` env vars in GitHub Actions secrets to route requests through a proxy
- **Alternative:** Use environment variable overrides (`BINANCE_API`, `BYBIT_API`) to point to mirrored/alternative endpoints

### Stocks (NASDAQ Trader)
- Uses FTP protocol; not tested in CI yet
- Likely works due to new retry/error handling, but consider manual validation

## Testing

### Local Testing (Verified ✅)
- Binance (spot & futures): 200+ BTC pairs
- Huobi: Working
- KuCoin: Working
- Bitfinex: Working
- Bybit (after v5 migration): 100+ USDT pairs
- Forex: Working

### CI/CD Testing
- Individual workflows can be manually triggered via `workflow_dispatch` button in GitHub Actions
- Monitor logs for any geolocation or API response issues

## How to Use

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run individual scripts
python3 binance/pairs.py
python3 huobi/pairs.py -q USDT
python3 kucoin/pairs.py

# Test with proxy (if behind corporate firewall or geolocation block)
export HTTP_PROXY=http://proxy.example.com:8080
python3 binance/pairs.py
```

### CI/CD with Custom Endpoints
```bash
# In GitHub Actions secrets, set:
# BINANCE_API = http://custom-mirror.example.com/api/v3/exchangeInfo
# BYBIT_API = http://custom-mirror.example.com/v5/market/tickers?category=spot

# Workflows will use these instead of default endpoints
```

## Contributors Welcome!

### Help Needed With:
1. **Proxy Configuration:** If you have access to a working proxy, help us configure it for CI/CD
2. **Geolocation Bypass:** Alternative API endpoints or mirror services for Binance/Bybit
3. **NASDAQ FTP:** Validate `stocks/nasdaqtrader.py` in CI environment
4. **Additional Exchanges:** Follow the pattern to add more exchange scripts

## Breaking Changes
None — all changes are backwards compatible. Existing workflows continue to work as before.

## Related Issues
- Resolves workflow failures due to missing `requests` dependency
- Fixes Bybit API endpoint deprecation (v2 → v5)
- Improves resilience against transient API failures

---

**PR Status:** Open for review & feedback. Ready to merge pending geolocation bypass strategy for Binance/Bybit.
