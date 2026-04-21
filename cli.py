#!/usr/bin/env python3

import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from bot.orders import OrderManager
from bot.validators import ValidationError, validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import logger
from binance.exceptions import BinanceAPIException

console = Console()


def create_parser():
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(description='Binance Futures Testnet Trading Bot')
    
    parser.add_argument('--symbol', required=True, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', required=True, choices=['BUY', 'SELL'], help='Order side: BUY or SELL')
    parser.add_argument('--type', required=True, choices=['MARKET', 'LIMIT'], dest='order_type', help='Order type: MARKET or LIMIT')
    parser.add_argument('--quantity', required=True, type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Order price (required for LIMIT orders)')
    
    return parser


def main():
    """Main CLI function."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Validate all inputs
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
        
        # Create order manager and place order
        order_manager = OrderManager()
        
        # Print order summary
        order_manager.print_order_summary(symbol, side, order_type, quantity, price)
        
        # Show placing message
        console.print(Panel("Placing order...", style="bold blue"))
        
        # Place the order
        response = order_manager.place_order(symbol, side, order_type, quantity, price)
        
        # Print formatted response
        order_manager.print_order_response(response)
        
    except ValidationError as e:
        logger.error(f"VALIDATION ERROR: {str(e)}")
        console.print(Panel(f"Validation Error: {str(e)}", style="bold red"))
        sys.exit(1)
    except BinanceAPIException as e:
        logger.error(f"BINANCE API ERROR [{e.code}]: {e.message}")
        console.print(Panel(f"Binance API Error [{e.code}]: {e.message}", style="bold red"))
        sys.exit(1)
    except Exception as e:
        logger.error(f"UNEXPECTED ERROR: {str(e)}")
        console.print(Panel(f"Error: {str(e)}", style="bold red"))
        sys.exit(1)


if __name__ == '__main__':
    main()
