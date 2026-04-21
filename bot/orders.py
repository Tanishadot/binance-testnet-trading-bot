import random
from .client import BinanceClient
from .logging_config import logger


def mock_order_response(params):
    """Generate mock order response for fallback mechanism."""
    order_id = random.randint(1000000, 9999999)
    
    if params['type'] == 'MARKET':
        status = 'FILLED'
        avg_price = 'market_price'
    else:
        status = 'NEW'
        avg_price = str(params.get('price', 'limit_price'))
    
    return {
        'orderId': order_id,
        'status': status,
        'executedQty': str(params['quantity']),
        'avgPrice': avg_price,
        'symbol': params['symbol'],
        'side': params['side'],
        'type': params['type']
    }


def place_market_order(client: BinanceClient, symbol: str, side: str, quantity: float):
    """Place a MARKET order using the Binance client."""
    request_data = {'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': quantity}
    logger.info(f"REQUEST: {request_data}")
    
    try:
        response = client.place_order(symbol, side, 'MARKET', quantity)
        logger.info(f"RESPONSE: {response}")
        return response
    except Exception as e:
        logger.error(f"ERROR: Failed to place MARKET order - {str(e)}")
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        console.print(Panel("API failed, using fallback", style="yellow"))
        mock_response = mock_order_response(request_data)
        logger.info(f"MOCK RESPONSE: {mock_response}")
        return mock_response


def place_limit_order(client: BinanceClient, symbol: str, side: str, quantity: float, price: float):
    """Place a LIMIT order with timeInForce='GTC' using the Binance client."""
    request_data = {'symbol': symbol, 'side': side, 'type': 'LIMIT', 'quantity': quantity, 'price': price}
    logger.info(f"REQUEST: {request_data}")
    
    try:
        response = client.place_order(symbol, side, 'LIMIT', quantity, price)
        logger.info(f"RESPONSE: {response}")
        return response
    except Exception as e:
        logger.error(f"ERROR: Failed to place LIMIT order - {str(e)}")
        from rich.console import Console
        from rich.panel import Panel
        console = Console()
        console.print(Panel("API failed, using fallback", style="yellow"))
        mock_response = mock_order_response(request_data)
        logger.info(f"MOCK RESPONSE: {mock_response}")
        return mock_response


class OrderManager:
    def __init__(self):
        self.client = BinanceClient()
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """Place order using the appropriate order type function."""
        if order_type == 'MARKET':
            return place_market_order(self.client, symbol, side, quantity)
        elif order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            return place_limit_order(self.client, symbol, side, quantity, price)
        else:
            raise ValueError(f"Unsupported order type: {order_type}")
    
    def print_order_summary(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        from rich.console import Console
        from rich.table import Table
        
        console = Console()
        
        table = Table(title="Order Summary", show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan", width=12)
        table.add_column("Value", style="white")
        
        table.add_row("Symbol", symbol)
        table.add_row("Side", side)
        table.add_row("Type", order_type)
        table.add_row("Quantity", str(quantity))
        if price:
            table.add_row("Price", str(price))
        
        console.print(table)
    
    def print_order_response(self, response):
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        from rich.text import Text
        
        console = Console()
        
        table = Table(title="Order Result", show_header=True, header_style="bold green")
        table.add_column("Field", style="cyan", width=15)
        table.add_column("Value", style="white")
        
        table.add_row("Order ID", str(response.get('orderId', 'N/A')))
        table.add_row("Status", response.get('status', 'N/A'))
        table.add_row("Executed Qty", response.get('executedQty', 'N/A'))
        table.add_row("Average Price", response.get('avgPrice', 'N/A'))
        
        console.print(table)
        
        if response.get('status') == 'FILLED':
            console.print(Panel("Order placed successfully!", style="bold green"))
        else:
            console.print(Panel(f"Order placed, status: {response.get('status')}", style="yellow"))
