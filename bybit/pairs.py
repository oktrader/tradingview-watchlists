import argparse
import requests

parser = argparse.ArgumentParser(description="Bybit tickers")
parser.add_argument("-q", "--quote-asset")

if __name__ == "__main__":
    args = parser.parse_args()

    url = "https://api.bybit.com/v2/public/symbols"
    symbols = map(lambda x: x["name"], requests.get(url).json()["result"])

    if args.quote_asset:
        symbols = filter(lambda x: x.endswith(args.quote_asset.upper()), symbols)

    symbols = map(lambda x: "BYBIT:{}".format(x.upper().replace(":", "")), symbols)

    print(",\n".join(sorted(symbols)))
