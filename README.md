# ₿ Crypto Terminal

**80s Hacker Aesthetic. Live Crypto Prices. Zero Dependencies.**

A terminal-based cryptocurrency dashboard with maximum retro vibes. Live prices from Coinbase, rendered in glorious 80s terminal style.

```
┌──────── ₿ITCOIN DASHBOARD ────────┐
│ ● LIVE | 19:08:28                 │
├────────────────────────────────────┤
│ ₿ BITCOIN                          │
│                                    │
│ $65,149.63    ▲ +8.58%           │
│                                    │
│ HIGH: $71,840.07    LOW: $60,001.00
├────────────────────────────────────┤
│ ♦ ETHEREUM                         │
│                                    │
│ $1,927.48     ▲ +10.60%          │
│                                    │
│ HIGH: $2,145.77    LOW: $1,742.79
├────────────────────────────────────┤
│ ◎ SOLANA                           │
│                                    │
│ $79.14      ▲ +17.28%            │
│                                    │
│ HIGH: $93.25       LOW: $67.48
├────────────────────────────────────┤
│ ◈ SUI                              │
│                                    │
│ $0.90      ▲ +14.70%             │
│                                    │
│ HIGH: $1.08        LOW: $0.79
└────────────────────────────────────┘
```

## Features

- ⚡ **Live prices** - Real-time data from Coinbase API
- 📊 **Multi-coin** - BTC, ETH, SOL, SUI
- 🎨 **80s aesthetic** - Green text, box drawing, scanlines
- 🔄 **Auto-refresh** - Updates every 2 seconds
- ⌨️ **Keyboard controls** - Press R to refresh, Q to quit

## Installation

```bash
# Clone the repo
git clone https://github.com/dougfour/crypto-terminal.git
cd crypto-terminal

# Install dependencies
pip install httpx

# Run it
python btc_term.py
```

## Requirements

- Python 3.8+
- `httpx` library

## Controls

| Key | Action |
|-----|--------|
| `R` | Refresh prices |
| `Q` | Quit |

## Supported Coins

| Key | Coin |
|-----|------|
| 1 | Bitcoin (BTC) |
| 2 | Ethereum (ETH) |
| 3 | Solana (SOL) |
| 4 | SUI |

## How It Works

1. Fetches live prices from Coinbase Exchange API
2. Calculates 24h high/low from stats endpoint
3. Renders everything in terminal with ANSI escape codes
4. Auto-refreshes every 2 seconds

## Why This Exists

Because checking prices in a browser is for squares. Real hackers use the terminal.

## License

MIT - Fork it, break it, make it yours.

---

**Made with 🐍 and 💜**
