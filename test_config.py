"""
Test Configuration Script
Run this to verify your .env file is set up correctly
"""
import sys
from pathlib import Path

def test_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("\n📝 To fix:")
        print("   1. Copy .env.example to .env")
        print("   2. Edit .env with your API keys")
        print("   3. Run this script again")
        return False
    print("✅ .env file found")
    return True

def test_config_import():
    """Try to import configuration"""
    try:
        from config import (
            ALPACA_CONFIG, MODE, INITIAL_CASH,
            STRATEGY_NAME, SYMBOLS
        )
        print("✅ Configuration imported successfully")
        return True, {
            "alpaca_config": ALPACA_CONFIG,
            "mode": MODE,
            "initial_cash": INITIAL_CASH,
            "strategy": STRATEGY_NAME,
            "symbols": SYMBOLS
        }
    except EnvironmentError as e:
        print(f"❌ Configuration error: {e}")
        return False, None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False, None

def test_alpaca_keys(config):
    """Verify Alpaca API keys are set"""
    alpaca = config["alpaca_config"]
    
    if alpaca["API_KEY"] and len(alpaca["API_KEY"]) > 10:
        print("✅ Alpaca API Key is set")
    else:
        print("❌ Alpaca API Key is missing or invalid")
        return False
    
    if alpaca["API_SECRET"] and len(alpaca["API_SECRET"]) > 10:
        print("✅ Alpaca Secret Key is set")
    else:
        print("❌ Alpaca Secret Key is missing or invalid")
        return False
    
    return True

def test_mode(config):
    """Verify trading mode is valid"""
    mode = config["mode"]
    if mode in ["backtest", "paper", "live"]:
        print(f"✅ Trading mode: {mode}")
        if mode == "live":
            print("   ⚠️  WARNING: Live trading mode - real money at risk!")
        return True
    else:
        print(f"❌ Invalid trading mode: {mode}")
        return False

def test_strategy_config(config):
    """Verify strategy configuration"""
    print(f"✅ Strategy: {config['strategy']}")
    print(f"✅ Symbols: {', '.join(config['symbols'])}")
    print(f"✅ Initial Cash: ${config['initial_cash']:,.2f}")
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Lumibot Configuration Test")
    print("=" * 60)
    print()
    
    # Test 1: Check .env file
    if not test_env_file():
        sys.exit(1)
    
    print()
    
    # Test 2: Import configuration
    success, config = test_config_import()
    if not success:
        sys.exit(1)
    
    print()
    
    # Test 3: Verify Alpaca keys
    if not test_alpaca_keys(config):
        print("\n📝 To fix:")
        print("   1. Go to https://alpaca.markets/")
        print("   2. Sign up for paper trading account")
        print("   3. Get API keys from dashboard")
        print("   4. Add to .env file")
        sys.exit(1)
    
    print()
    
    # Test 4: Verify mode
    if not test_mode(config):
        sys.exit(1)
    
    print()
    
    # Test 5: Verify strategy config
    test_strategy_config(config)
    
    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  1. Run a backtest: python run_backtest.py")
    print("  2. Try paper trading: python run_paper.py")
    print("  3. Read SETUP_ENV.md for more info")
    print()

if __name__ == "__main__":
    main()
