import streamlit as st
from bot.orders import OrderManager
from bot.validators import ValidationError, validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.logging_config import logger
from binance.exceptions import BinanceAPIException

st.set_page_config(
    page_title="Binance Futures Trading Bot",
    page_icon=":chart_with_upwards_trend:",
    layout="centered"
)

st.title("Binance Futures Trading Bot")
st.markdown("---")

# Order input form
with st.form("order_form"):
    st.subheader("Place Order")
    
    col1, col2 = st.columns(2)
    
    with col1:
        symbol = st.text_input("Symbol*", value="BTCUSDT", help="Trading symbol (e.g., BTCUSDT)")
        side = st.selectbox("Side*", ["BUY", "SELL"], help="Order side: BUY or SELL")
    
    with col2:
        order_type = st.selectbox("Order Type*", ["MARKET", "LIMIT"], help="Order type: MARKET or LIMIT")
        quantity = st.number_input("Quantity*", min_value=0.0, value=0.001, step=0.001, format="%.6f", help="Order quantity")
    
    price = None
    if order_type == "LIMIT":
        price = st.number_input("Price*", min_value=0.0, value=27000.0, step=0.01, format="%.2f", help="Order price (required for LIMIT orders)")
    
    submit_button = st.form_submit_button("Place Order", type="primary")

if submit_button:
    try:
        # Validate inputs
        validated_symbol = validate_symbol(symbol)
        validated_side = validate_side(side)
        validated_order_type = validate_order_type(order_type)
        validated_quantity = validate_quantity(quantity)
        validated_price = validate_price(price, validated_order_type)
        
        # Show order summary
        st.success("Order Summary")
        summary_data = {
            "Symbol": validated_symbol,
            "Side": validated_side,
            "Type": validated_order_type,
            "Quantity": validated_quantity
        }
        if validated_price:
            summary_data["Price"] = validated_price
        
        st.json(summary_data)
        
        # Show placing message
        st.info("Placing order...")
        
        # Place the order
        order_manager = OrderManager()
        response = order_manager.place_order(
            validated_symbol, 
            validated_side, 
            validated_order_type, 
            validated_quantity, 
            validated_price
        )
        
        # Show order result
        st.success("Order Result")
        result_data = {
            "Order ID": response.get('orderId', 'N/A'),
            "Status": response.get('status', 'N/A'),
            "Executed Quantity": response.get('executedQty', 'N/A'),
            "Average Price": response.get('avgPrice', 'N/A')
        }
        st.json(result_data)
        
        # Success message
        if response.get('status') == 'FILLED':
            st.success("Order placed successfully! :white_check_mark:")
        else:
            st.info(f"Order placed, status: {response.get('status')}")
        
    except ValidationError as e:
        logger.error(f"VALIDATION ERROR: {str(e)}")
        st.error(f"Validation Error: {str(e)}")
    except BinanceAPIException as e:
        logger.error(f"BINANCE API ERROR [{e.code}]: {e.message}")
        st.error(f"Binance API Error [{e.code}]: {e.message}")
    except Exception as e:
        logger.error(f"UNEXPECTED ERROR: {str(e)}")
        st.error(f"Error: {str(e)}")

st.markdown("---")
st.markdown("### About")
st.markdown("""
This is a Binance Futures Testnet trading bot with fallback functionality:
- **Primary**: Real Binance API calls
- **Fallback**: Mock responses when API fails
- **Logging**: All requests/responses logged to `bot.log`
""")

st.markdown("### Environment Setup")
st.markdown("""
Ensure `.env` file contains:
```
BINANCE_TESTNET_API_KEY=your_api_key
BINANCE_TESTNET_SECRET_KEY=your_secret_key
```
""")
