"""task9: the public series the pack ships, pulled once and kept byte for byte under raw/ with a manifest.

    python3 pull.py      # re-pull (network); the build never pulls, it reads raw/ and checks each file's sha256
"""
import datetime as dt
import hashlib
import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else "raw")
FRED = {
    "NASDAQ100": "NASDAQ-100 Index, daily close (Nasdaq, via FRED)",
    "DGS2": "Market yield on U.S. Treasury securities at 2-year constant maturity, daily (Board of Governors H.15, via FRED)",
    "DGS10": "Market yield on U.S. Treasury securities at 10-year constant maturity, daily (Board of Governors H.15, via FRED)",
    "DTB3": "3-month Treasury bill secondary market rate, daily (Board of Governors H.15, via FRED)",
    "DBAA": "Moody's seasoned Baa corporate bond yield, daily (Moody's, via FRED)",
    "DAAA": "Moody's seasoned Aaa corporate bond yield, daily (Moody's, via FRED)",
    "DTWEXBGS": "Nominal broad U.S. dollar index, daily (Board of Governors H.10, via FRED)",
    "DCOILBRENTEU": "Crude oil prices: Brent, Europe, daily (EIA, via FRED)",
    "DEXUSAL": "U.S. dollars to one Australian dollar, noon buying rates (H.10, via FRED)",
    "DEXUSNZ": "U.S. dollars to one New Zealand dollar, noon buying rates (H.10, via FRED)",
    "DEXUSUK": "U.S. dollars to one British pound, noon buying rates (H.10, via FRED)",
    "DEXUSEU": "U.S. dollars to one euro, noon buying rates (H.10, via FRED)",
    "DEXJPUS": "Japanese yen to one U.S. dollar, noon buying rates (H.10, via FRED)",
    "DEXSZUS": "Swiss francs to one U.S. dollar, noon buying rates (H.10, via FRED)",
    "DEXCAUS": "Canadian dollars to one U.S. dollar, noon buying rates (H.10, via FRED)",
    "DEXNOUS": "Norwegian kroner to one U.S. dollar, noon buying rates (H.10, via FRED)",
    "DEXSDUS": "Swedish kronor to one U.S. dollar, noon buying rates (H.10, via FRED)",
    "IR3TIB01AUM156N": "Australia, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01NZM156N": "New Zealand, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01GBM156N": "United Kingdom, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IRSTCI01GBM156N": "United Kingdom, call money/interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01EZM156N": "Euro area, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01DEM156N": "Germany, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01JPM156N": "Japan, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01CHM156N": "Switzerland, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01CAM156N": "Canada, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01NOM156N": "Norway, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01SEM156N": "Sweden, 3-month interbank rate, monthly (OECD MEI, via FRED)",
    "IR3TIB01USM156N": "United States, 3-month interbank rate, monthly (OECD MEI, via FRED)",
}
CBOE = {"SPX": "S&P 500 Index daily closing levels (Cboe index history download)",
        "VIX": "Cboe Volatility Index daily open, high, low and close (Cboe index history download)"}


def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def main():
    os.makedirs(OUT, exist_ok=True)
    pulled = dt.date.today().isoformat()
    files = []
    for sid, what in FRED.items():
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=%s" % sid
        b = get(url)
        name = sid + ".csv"
        open(os.path.join(OUT, name), "wb").write(b)
        lines = b.decode().strip().splitlines()
        files.append(dict(file=name, series=what, url=url, pulled=pulled, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b),
                          rows=len(lines) - 1, header=lines[0], first=lines[1].split(",")[0], last=lines[-1].split(",")[0]))
    for sym, what in CBOE.items():
        url = "https://cdn.cboe.com/api/global/us_indices/daily_prices/%s_History.csv" % sym
        b = get(url)
        name = sym + "_History.csv"
        open(os.path.join(OUT, name), "wb").write(b)
        lines = b.decode().strip().splitlines()
        files.append(dict(file=name, series=what, url=url, pulled=pulled, sha256=hashlib.sha256(b).hexdigest(), bytes=len(b),
                          rows=len(lines) - 1, header=lines[0], first=lines[1].split(",")[0], last=lines[-1].split(",")[0]))
    json.dump({"source": "Federal Reserve Bank of St. Louis (FRED) and Cboe Global Markets index history downloads",
               "pulled": pulled, "note": "Kept byte for byte as downloaded; the build reads every market value from these files.",
               "files": files}, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    print(len(files), "files to", OUT)


if __name__ == "__main__":
    main()
