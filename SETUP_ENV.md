# 🔧 Environment Setup Guide

## Quick Start

### 1. Copy Environment Template

```bash
cp .env.example .env
```

### 2. Edit `.env` with Your Credentials

```bash
# Windows
notepad .env

# macOS/Linux
nano .env
# or
vim .env
```

### 3. Get API Keys

#### Alpaca (Required for Trading)
1. Go to: https://alpaca.markets/
2. Sign up for free paper trading account
3. Navigate to: Account → API Keys
4. Generate new API key
5. Copy `API Key ID` → `ALPACA_API_KEY`
6. Copy `Secret Key` → `ALPACA_SECRET_KEY`

#### Polygon (Optional - for real-time data)
1. Go to: https://polygon.io/
2. Sign up for free tier
3. Get API key from dashboard
4. Copy to `POLYGON_API_KEY`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Verify Setup

```python
# test_config.py
from dotenv import load_dotenv
import os

load_dotenv()

print("✓ ALPACA_API_KEY:", "✓" if os.getenv("ALPACA_API_KEY") else "✗ Missing")
print("✓ ALPACA_SECRET_KEY:", "✓" if os.getenv("ALPACA_SECRET_KEY") else "✗ Missing")
print("✓ MODE:", os.getenv("MODE", "backtest"))
```

Run:
```bash
python test_config.py
```

## Configuration Options

### Trading Modes

```bash
# Backtesting (safe, no real money)
MODE=backtest

# Paper Trading (simulated, no real money)
MODE=paper

# Live Trading (REAL MONEY - be careful!)
MODE=live
```

### Risk Management

```bash
# Risk 2% per trade
RISK_PER_TRADE=0.02

# Maximum 10 open positions
MAX_POSITIONS=10

# Stop loss at 5%
STOP_LOSS_PCT=0.05

# Take profit at 10%
TAKE_PROFIT_PCT=0.10
```

### Notifications

#### Slack Notifications
1. Create Slack webhook: https://api.slack.com/messaging/webhooks
2. Add to `.env`:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

#### Email Notifications
```bash
EMAIL_NOTIFICATIONS=true
EMAIL_TO=your-email@example.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Security Best Practices

### ✅ DO:
- Keep `.env` file private
- Use paper trading for testing
- Rotate API keys regularly
- Use strong passwords
- Enable 2FA on broker accounts

### ❌ DON'T:
- Commit `.env` to git
- Share API keys
- Use live mode without testing
- Store secrets in code
- Use same keys for multiple bots

## Troubleshooting

### Issue: "ALPACA_API_KEY not found"
**Solution**: Make sure `.env` file exists and contains the key

### Issue: "Invalid API credentials"
**Solution**: 
1. Verify keys are correct
2. Check if using paper trading URL for paper keys
3. Regenerate keys if needed

### Issue: "Module 'dotenv' not found"
**Solution**: 
```bash
pip install python-dotenv
```

### Issue: "Permission denied"
**Solution**: 
```bash
chmod 600 .env  # Make file readable only by you
```

## Example `.env` File

```bash
# Alpaca Paper Trading
ALPACA_API_KEY=PK1234567890ABCDEF
ALPACA_SECRET_KEY=abcdefghijklmnopqrstuvwxyz1234567890
ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Mode
MODE=paper

# Strategy
SYMBOLS=SPY,QQQ
INITIAL_CASH=100000

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00/B00/XXXX
```

## Next Steps

1. ✅ Setup environment variables
2. ✅ Test configuration
3. ✅ Run backtest
4. ✅ Verify results
5. ✅ Deploy to paper trading
6. ⚠️ Only then consider live trading

## Resources

- [Lumibot Documentation](https://lumibot.lumiwealth.com/)
- [Alpaca API Docs](https://alpaca.markets/docs/)
- [Python-dotenv Guide](https://pypi.org/project/python-dotenv/)
