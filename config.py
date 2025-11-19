"""
Configuration Management for Lumibot Trading Bot
Loads settings from environment variables for security
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Alpaca Configuration
ALPACA_CONFIG = {
    "API_KEY": os.getenv("ALPACA_API_KEY"),
    "API_SECRET": os.getenv("ALPACA_SECRET_KEY"),
    "PAPER": os.getenv("ALPACA_PAPER", "True").lower() == "true",
    "BASE_URL": os.getenv(
        "ALPACA_BASE_URL",
        "https://paper-api.alpaca.markets" if os.getenv("ALPACA_PAPER", "True").lower() == "true"
        else "https://api.alpaca.markets"
    )
}

# Validate required configuration
if not ALPACA_CONFIG["API_KEY"]:
    raise EnvironmentError(
        "ALPACA_API_KEY not set in environment.\n"
        "Please copy .env.example to .env and fill in your API keys.\n"
        "Get keys from: https://alpaca.markets/"
    )

if not ALPACA_CONFIG["API_SECRET"]:
    raise EnvironmentError(
        "ALPACA_SECRET_KEY not set in environment.\n"
        "Please copy .env.example to .env and fill in your API keys."
    )

# Trading Mode
MODE = os.getenv("MODE", "backtest")  # Options: backtest, paper, live
if MODE not in ["backtest", "paper", "live"]:
    raise ValueError(f"Invalid MODE: {MODE}. Must be 'backtest', 'paper', or 'live'")

# Trading Configuration
INITIAL_CASH = float(os.getenv("INITIAL_CASH", "100000"))
RISK_PER_TRADE = float(os.getenv("RISK_PER_TRADE", "0.02"))
MAX_POSITIONS = int(os.getenv("MAX_POSITIONS", "10"))
STOP_LOSS_PCT = float(os.getenv("STOP_LOSS_PCT", "0.05"))
TAKE_PROFIT_PCT = float(os.getenv("TAKE_PROFIT_PCT", "0.10"))

# Strategy Configuration
STRATEGY_NAME = os.getenv("STRATEGY_NAME", "MyStrategy")
SYMBOLS = os.getenv("SYMBOLS", "SPY,QQQ,IWM").split(",")
TIMEFRAME = os.getenv("TIMEFRAME", "1Day")

# Data Sources
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
USE_YAHOO_FINANCE = os.getenv("YAHOO_FINANCE", "true").lower() == "true"

# Notifications
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
EMAIL_NOTIFICATIONS = os.getenv("EMAIL_NOTIFICATIONS", "false").lower() == "true"
EMAIL_TO = os.getenv("EMAIL_TO")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/trading.log")

# Ensure log directory exists
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

# Backtesting Configuration
BACKTEST_START_DATE = os.getenv("BACKTEST_START_DATE", "2020-01-01")
BACKTEST_END_DATE = os.getenv("BACKTEST_END_DATE", "2024-12-31")

# Database (optional)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///trading.db")

# Monitoring (optional)
SENTRY_DSN = os.getenv("SENTRY_DSN")

def print_config():
    """Print current configuration (for debugging)"""
    print("=" * 60)
    print("Lumibot Configuration")
    print("=" * 60)
    print(f"Mode: {MODE}")
    print(f"Alpaca Paper Trading: {ALPACA_CONFIG['PAPER']}")
    print(f"Initial Cash: ${INITIAL_CASH:,.2f}")
    print(f"Risk Per Trade: {RISK_PER_TRADE:.1%}")
    print(f"Max Positions: {MAX_POSITIONS}")
    print(f"Strategy: {STRATEGY_NAME}")
    print(f"Symbols: {', '.join(SYMBOLS)}")
    print(f"Timeframe: {TIMEFRAME}")
    print(f"Notifications: {'Enabled' if SLACK_WEBHOOK_URL or EMAIL_NOTIFICATIONS else 'Disabled'}")
    print("=" * 60)

if __name__ == "__main__":
    # Test configuration
    print_config()
    print("\n✅ Configuration loaded successfully!")
