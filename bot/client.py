import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

load_dotenv()


class BinanceClient:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_TESTNET_API_KEY')
        self.api_secret = os.getenv('BINANCE_TESTNET_SECRET_KEY')
        
        if not self.api_key or not self.api_secret:
            raise ValueError("BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_SECRET_KEY environment variables must be set")
        
        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=True,
            tld='com'
        )
        self.client.API_URL = 'https://testnet.binancefuture.com'
    
    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        order_params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders")
            order_params['price'] = str(price)
            order_params['timeInForce'] = 'GTC'
        
        return self.client.futures_create_order(**order_params)
