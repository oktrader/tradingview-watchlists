#!/usr/bin/env python3
"""Test if requests is available and try a simple API call."""
import sys

try:
    import requests
    print(f"✓ requests module found: {requests.__version__}")
except ImportError as e:
    print(f"✗ requests module NOT found: {e}")
    print(f"\nTrying to install requests...")
    import subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "install", "requests"], 
                          capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr)
        sys.exit(1)
    import requests
    print(f"✓ requests installed: {requests.__version__}")

# Try a simple Binance API call
print("\n--- Testing Binance API ---")
try:
    response = requests.get('https://api.binance.com/api/v1/exchangeInfo', timeout=5)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"✓ API call successful, got {len(data.get('symbols', []))} symbols")
    else:
        print(f"✗ API returned status {response.status_code}: {response.text[:200]}")
except Exception as e:
    print(f"✗ API call failed: {e}")

# Try running the binance script
print("\n--- Running binance/pairs.py ---")
try:
    result = subprocess.run([sys.executable, "binance/pairs.py", "-q", "BTC"], 
                          capture_output=True, text=True, timeout=30)
    print("STDOUT:", result.stdout[:500])
    if result.stderr:
        print("STDERR:", result.stderr[:500])
    print(f"Exit code: {result.returncode}")
except Exception as e:
    print(f"✗ Script execution failed: {e}")
