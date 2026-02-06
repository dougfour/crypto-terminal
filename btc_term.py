#!/usr/bin/env python3
"""
₿ BTC-TERM - 80s Terminal Crypto Dashboard

Live prices from Coinbase with 80s hacker aesthetic.
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import Dict

import httpx
import select

# ANSI codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
CLEAR = "\033[2J"
HOME = "\033[H"
HIDE = "\033[?25l"
SHOW = "\033[?25h"

BOX_H = "─"
BOX_V = "│"
BOX_TL = "┌"
BOX_TR = "┐"
BOX_BL = "└"
BOX_BR = "┘"
BOX_ML = "├"
BOX_MR = "┤"

# All pairs to display
PAIRS = {
    "BTC-USD": {"emoji": "₿", "name": "BITCOIN"},
    "ETH-USD": {"emoji": "♦", "name": "ETHEREUM"},
    "SOL-USD": {"emoji": "◎", "name": "SOLANA"},
    "SUI-USD": {"emoji": "◈", "name": "SUI"},
}


async def get_all_prices() -> Dict[str, dict]:
    """Get prices for all pairs."""
    results = {}
    
    async with httpx.AsyncClient() as client:
        for pair in PAIRS:
            try:
                # Get current price
                r1 = await client.get(f"https://api.exchange.coinbase.com/products/{pair}/ticker", timeout=3)
                if r1.status_code == 200:
                    ticker = r1.json()
                    price = float(ticker.get("price", 0))
                    
                    # Get 24h stats
                    r2 = await client.get(f"https://api.exchange.coinbase.com/products/{pair}/stats", timeout=3)
                    if r2.status_code == 200:
                        stats = r2.json()
                        high = float(stats.get("high")) if stats.get("high") else price
                        low = float(stats.get("low")) if stats.get("low") else price
                    else:
                        high = low = price
                    
                    results[pair] = {"price": price, "high": high, "low": low}
                else:
                    results[pair] = {"price": 0, "high": 0, "low": 0}
            except:
                results[pair] = {"price": 0, "high": 0, "low": 0}
    
    return results


def draw_header():
    """Draw terminal header."""
    now = datetime.now().strftime("%H:%M:%S")
    print(f"{GREEN}{BOX_TL}{BOX_H * 8} ₿ITCOIN DASHBOARD {BOX_H * 8}{BOX_TR}{RESET}")
    print(f"{GREEN}{BOX_V}{RESET} {CYAN}{BOLD}BTC-TERM v1.0{RESET} " + " " * 30 + f"{GREEN}{BOX_V}{RESET}")
    print(f"{GREEN}{BOX_V}{RESET} {GREEN}● LIVE{RESET} | {now}" + " " * 30 + f"{GREEN}{BOX_V}{RESET}")
    print(f"{GREEN}{BOX_ML}{BOX_H * 46}{BOX_MR}{RESET}")


def draw_row(pair: str, data: dict, is_last: bool = False):
    """Draw a single coin row."""
    info = PAIRS.get(pair, {"emoji": "?", "name": pair})
    emoji = info["emoji"]
    name = info["name"]
    
    price = data.get("price", 0)
    high = data.get("high", 0)
    low = data.get("low", 0)
    
    # Calculate 24h change
    if high > low and price > 0:
        change = ((price - low) / low) * 100
        change_str = f"+{change:.2f}%"
    else:
        change_str = "0.00%"
    
    if change_str.startswith("+"):
        color = GREEN
        arrow = "▲"
    else:
        color = RED
        arrow = "▼"
    
    # Format price based on value
    if price >= 1000:
        price_str = f"${price:,.2f}"
    elif price >= 1:
        price_str = f"${price:,.4f}"
    else:
        price_str = f"${price:,.6f}"
    
    # Format high/low
    high_str = f"${high:,.2f}" if high >= 1 else f"${high:,.4f}"
    low_str = f"${low:,.2f}" if low >= 1 else f"${low:,.4f}"
    
    box_bottom = BOX_BR if is_last else BOX_MR
    
    print(f"{GREEN}{BOX_V}{RESET}  {BOLD}{emoji} {name:<10}{RESET}")
    print(f"{GREEN}{BOX_V}{RESET}")
    print(f"{GREEN}{BOX_V}{RESET}  {BOLD}{price_str:<14}{RESET}  {color}{arrow} {change_str}{RESET}")
    print(f"{GREEN}{BOX_V}{RESET}")
    print(f"{GREEN}{BOX_V}{RESET}  HIGH: {high_str:<12}  LOW: {low_str}")
    print(f"{GREEN}{box_bottom}{BOX_H * 46}{BOX_BR if is_last else BOX_MR}{RESET}")


def draw_footer():
    """Draw footer."""
    print(f"{GREEN}{BOX_V}{RESET}  {BOLD}CONTROLS:{RESET} [R] Refresh  [Q] Quit         ")
    print(f"{GREEN}{BOX_BL}{BOX_H * 46}{BOX_BR}{RESET}")
    print(f"{CYAN}{BOLD}▓▒░ LIVE FROM COINBASE ░▒▓{RESET}")


async def render_loop():
    """Main render loop."""
    # Check if stdin is a TTY
    has_tty = sys.stdin.isatty()
    
    if has_tty:
        import tty
        import termios
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
    
    try:
        while True:
            # Fetch all prices
            prices = await get_all_prices()
            
            # Draw dashboard
            print(CLEAR + HOME, end="")
            draw_header()
            
            pairs_list = list(PAIRS.keys())
            for i, pair in enumerate(pairs_list):
                data = prices.get(pair, {"price": 0, "high": 0, "low": 0})
                draw_row(pair, data, is_last=(i == len(pairs_list) - 1))
            
            draw_footer()
            
            if has_tty:
                # Check for keypress (non-blocking)
                dr, dw, de = select.select([sys.stdin], [], [], 0.5)
                if dr:
                    key = sys.stdin.read(1)
                    if key.lower() == 'q':
                        print(f"\n{GREEN}👋 Bye!{RESET}\n")
                        break
                    elif key.lower() == 'r':
                        # Refresh - just continue loop
                        pass
            else:
                await asyncio.sleep(2)
            
            await asyncio.sleep(2)  # Refresh every 2 seconds
    
    finally:
        if has_tty:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def main():
    print(f"""
{GREEN}
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║    ██████╗ ███████╗ █████╗  ██████╗██╗  ██╗              ║
║   ██╔══██╗██╔════╝██╔══██╗██╔════╝██║  ██║              ║
║   ██████╔╝█████╗  ███████║██║     ███████║              ║
║   ██╔══██╗██╔══╝  ██╔══██║██║     ██╔══██║              ║
║   ██║  ██║███████╗██║  ██║╚██████╗██║  ██║              ║
║   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝              ║
║                                                           ║
║    {CYAN}▓▒░ 80s HACKER TERMINAL AESTHETIC ░▒▓{GREEN}           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
{RESET}
    """)
    
    print(f"{YELLOW}Press [R] to refresh | [Q] to quit{RESET}\n")
    
    try:
        asyncio.run(render_loop())
    except KeyboardInterrupt:
        print(f"\n{GREEN}👋 Bye!{RESET}\n")


if __name__ == "__main__":
    main()
