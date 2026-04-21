from .client import BinanceClient
from .logging_config import logger


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
        raise


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
        raise


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
        print("\n--- Order Summary ---")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {quantity}")
        if price:
            print(f"Price: {price}")
        print("----------------------")
    
    def print_order_response(self, response):
        print("\n--- Order Result ---")
        print(f"Order ID: {response.get('orderId', 'N/A')}")
        print(f"Status: {response.get('status', 'N/A')}")
        print(f"Executed Quantity: {response.get('executedQty', 'N/A')}")
        print(f"Average Price: {response.get('avgPrice', 'N/A')}")
        print("--------------------")
        
        if response.get('status') == 'FILLED':
            print("✓ Order placed successfully!")
        else:
            print(f"Order placed, status: {response.get('status')}")
