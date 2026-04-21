# Binance Futures Testnet Trading Bot

A clean and minimal Python trading bot for Binance Futures Testnet.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
```bash
export BINANCE_TESTNET_API_KEY="your_testnet_api_key"
export BINANCE_TESTNET_SECRET_KEY="your_testnet_secret_key"
```

## Usage (CLI)

The CLI is the primary interface with enhanced Rich formatting for better user experience.

### Market Orders

**BUY Market Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

**SELL Market Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type MARKET --quantity 0.001
```

### Limit Orders

**BUY Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 27000.00
```

**SELL Limit Order:**
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 28000.00
```

**CLI Features:**
- Rich table formatting for order summary and results
- Color-coded status panels
- User-friendly error messages
- "Placing order..." progress indicator
- Fallback notifications when API fails

## Optional UI

For a web-based interface, run the Streamlit app:

```bash
streamlit run app.py
```

**UI Features:**
- Interactive form with dropdown inputs
- Real-time order summary display
- JSON-formatted results
- Status indicators and error handling
- Same fallback logic as CLI
- Environment setup guide

**Note:** The CLI remains the primary interface. The UI is an optional enhancement for users who prefer a graphical interface.

## Project Structure

```
trading_bot/
  bot/
    client.py        # Binance client wrapper
    orders.py        # Order placement logic
    validators.py    # Input validation
    logging_config.py # Logging configuration
  cli.py             # CLI entry point
  requirements.txt   # Dependencies
  README.md          # Documentation
```

## Features

- Place BUY/SELL orders on Binance Futures Testnet
- Support MARKET and LIMIT order types
- Input validation for all parameters
- Comprehensive logging to `bot.log`
- Clear order summaries and responses
- Error handling for API and network issues

## Notes

- Uses Binance Futures Testnet (no real money)
- Requires Binance Testnet API keys
- Logs all API requests and responses
- Validates all input parameters before placing orders
