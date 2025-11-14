
# Copilot / AI-Agent Quick Guide — tradingview-watchlists

Purpose
- Short, actionable notes so an AI code agent is immediately productive in this repo.

Quick orientation
- This repo publishes automated TradingView watchlist files by exchange (folders such as `binance/`, `bitfinex/`, `bybit/`, `forex/`, `huobi/`, `kucoin/`, `stocks/`).
- Each exchange folder typically contains a small CLI script (`pairs.py` or similarly named) which queries a public API, formats symbols (e.g. `BINANCE:BTCUSDT`, `BYBIT:...PERP`), and prints comma/newline-separated output into text files in the same folder.

Developer workflows (how it actually runs)
- GitHub Actions (see `.github/workflows/*.yaml`) run scheduled jobs that invoke these scripts and write files. Example (Binance):
	- `python3 binance/pairs.py > binance/binance_all_pairs.txt`
	- CI commits changed files with `git commit -a && git push`.
- On Windows use the repo-root PowerShell prompt and run `python` (or `python3` if available) from the root, e.g.:
	- `python binance/pairs.py -q USDT > binance/binance_USDT_pairs.txt`

Important file patterns & conventions
- Exchange folders: `X/pairs.py` (or `nasdaqtrader.py` for stocks, `oanda.py` for forex). These accept simple CLI flags:
	- Common flags: `-m` or `--margin`, `-f` or `--futures`, `-q`/`--quote-asset` (see `binance/pairs.py`).
	- Outputs are plain text files (CSV-like with one symbol per line or comma/newline separated) named `exchange_*_pairs.txt`, `exchange_all_pairs.txt`, or similar.
- Output format: scripts prefix symbols with exchange identifiers (e.g. `BINANCE:`) so files are ready for import into TradingView or other tooling.
- CI behavior: workflows run scheduled updates and commit the generated files back to the repository; avoid changing those generated files manually unless updating the generator logic.

Cross-component integration points
- Scripts call public REST endpoints (see `requests` usage in `*.py` files). There is no authenticated API usage in these scripts—so no secrets in the repo.
- Generated `.txt` files are the main product — other tooling or manual steps consume them (TradingView imports, external syncs).

Local dev suggestions for edits
- When editing a `pairs.py` script, add or update unitable bits near the CLI parsing block (top of file) and keep output formatting consistent (one symbol per line or comma+newline as existing files).
- Run the same command the CI uses locally to validate output before pushing; e.g. replicate a workflow step from `.github/workflows/binance.yaml`.

Why things are structured this way
- Small, focused scripts per exchange keep API differences isolated. The CI runs them on a schedule and commits only the artifact files — this separates data generation from consumer tooling.

Files to inspect when working here (examples)
- `binance/pairs.py` — shows `-m`, `-f`, `-q` flags and output formatting.
- `stocks/nasdaqtrader.py` — shows how stock exchanges are handled (flags `-nyse`, `--nasdaq`, `-arca`).
- `.github/workflows/*.yaml` — shows exact CI commands and schedules. Copy those locally to reproduce.

Do not assume
- There are no test suites or build steps in the repo — CI simply runs the Python scripts and commits outputs. Do not add heavy build tooling without justification.

If something is unclear or you need more details
- Tell me what area you want expanded (examples: adding local dev commands, adding tests, documenting one script's behavior in greater detail). I can iterate the file.

— End of AI-agent brief —
