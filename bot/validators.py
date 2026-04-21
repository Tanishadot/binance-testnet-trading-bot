class ValidationError(Exception):
    pass


def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValidationError("Symbol is required")
    return symbol.upper()


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than 0")
    return quantity


def validate_price(price: float, order_type: str) -> float:
    if order_type == 'LIMIT':
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        if price <= 0:
            raise ValidationError("Price must be greater than 0")
        return price
    return None


def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValidationError("Side must be either BUY or SELL")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValidationError("Order type must be either MARKET or LIMIT")
    return order_type
