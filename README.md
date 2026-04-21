# Binance Futures Testnet Trading Bot

A professional CLI-based trading bot for Binance Futures Testnet with Rich formatting, input validation, and robust fallback mechanisms.

## Features

- **CLI-based order execution** with Rich table formatting
- **Input validation** for symbol, quantity, and price requirements
- **Structured logging** with REQUEST/RESPONSE/MOCK RESPONSE tracking
- **Fallback mechanism** for API failures with mock responses
- **Optional Streamlit UI** for web-based interaction

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Binance Testnet API credentials
```

## Usage (CLI)

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 70000
```

**CLI Features:**
- Rich table formatting for order summaries and results
- Color-coded status panels and progress indicators
- Comprehensive error handling with clear messages
- Professional output with no raw JSON dumps

## Optional UI

Launch the web interface:
```bash
streamlit run app.py
```

**UI Features:**
- Interactive form with dropdown selections
- Real-time order summary and response display
- Same validation and fallback logic as CLI
- Professional JSON-formatted results

## Fallback Mechanism

Due to Binance Testnet access restrictions, the bot includes a robust fallback system:

- **Primary**: Attempts real Binance API calls
- **Fallback**: Generates mock responses when API fails
- **Logging**: Clearly distinguishes between `RESPONSE:` and `MOCK RESPONSE:` in logs
- **User Experience**: Seamless execution with clear status indicators

## Project Structure

```
binance-testnet-trading-bot/
  bot/
    client.py        # Binance client wrapper
    orders.py        # Order placement logic
    validators.py    # Input validation
    logging_config.py # Logging configuration
  cli.py             # CLI entry point
  app.py             # Streamlit UI (optional)
  requirements.txt   # Dependencies
  .env.example      # Environment variables template
  README.md          # Documentation
```

## Requirements

- Python 3.7+
- Binance Testnet API credentials
- Dependencies listed in `requirements.txt`

## Logging

All API requests, responses, and errors are logged to `bot.log` with timestamps for complete audit trails.
