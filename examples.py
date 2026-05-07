"""
Example usage of Binary Trading Bot
Demonstrates all major features
"""

import asyncio
import sys
from bot.trading_bot import TradingBot, OHLC, Signal
from integrations.binance import BinanceREST
from integrations.finnhub import FinnhubClient
from config.loader import ConfigLoader
from utils.backtest import Backtester


async def example_1_analyze_crypto():
    """Example 1: Analyze cryptocurrency with real Binance data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Cryptocurrency Analysis (Binance)")
    print("="*60 + "\n")
    
    bot = TradingBot()
    
    # Get real data from Binance
    candles = await BinanceREST.get_klines("BTC/USDT", "5m", limit=100)
    
    if candles:
        # Convert to OHLC
        ohlc_data = [
            OHLC(
                timestamp=c['timestamp'],
                open=c['open'],
                high=c['high'],
                low=c['low'],
                close=c['close'],
                volume=c['volume']
            )
            for c in candles
        ]
        
        # Analyze
        analysis = bot.analyze(ohlc_data, "BTC/USDT", "5m")
        
        # Print formatted analysis
        print(bot.format_analysis(analysis))


async def example_2_analyze_forex():
    """Example 2: Analyze Forex pair with real Finnhub data"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Forex Analysis (Finnhub)")
    print("="*60 + "\n")
    
    bot = TradingBot()
    client = FinnhubClient(api_key="demo")  # Use your API key
    
    # Get real data from Finnhub
    candles = await client.get_candles("OANDA:EURUSD", "5", limit=100)
    
    if candles:
        # Convert to OHLC
        ohlc_data = [
            OHLC(
                timestamp=c['timestamp'],
                open=c['open'],
                high=c['high'],
                low=c['low'],
                close=c['close'],
                volume=c.get('volume', 0)
            )
            for c in candles
        ]
        
        # Analyze
        analysis = bot.analyze(ohlc_data, "EURUSD", "5m")
        
        # Print formatted analysis
        print(bot.format_analysis(analysis))


async def example_3_multi_pair_scan():
    """Example 3: Scan multiple cryptocurrency pairs"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Multi-Pair Scan")
    print("="*60 + "\n")
    
    bot = TradingBot()
    
    pairs = ["BTC/USDT", "ETH/USDT", "BNB/USDT"]
    results = []
    
    for pair in pairs:
        print(f"\n🔍 Analyzing {pair}...")
        candles = await BinanceREST.get_klines(pair, "5m", limit=100)
        
        if candles:
            ohlc_data = [
                OHLC(
                    timestamp=c['timestamp'],
                    open=c['open'],
                    high=c['high'],
                    low=c['low'],
                    close=c['close'],
                    volume=c['volume']
                )
                for c in candles
            ]
            
            analysis = bot.analyze(ohlc_data, pair, "5m")
            results.append(analysis)
    
    # Print summary
    print("\n" + "="*60)
    print("SCAN SUMMARY")
    print("="*60)
    
    buy_signals = sum(1 for r in results if r.signal == Signal.BUY and r.confidence >= 70)
    sell_signals = sum(1 for r in results if r.signal == Signal.SELL and r.confidence >= 70)
    hold_signals = sum(1 for r in results if r.signal == Signal.HOLD)
    
    print(f"\n✅ BUY Signals (confidence ≥70): {buy_signals}")
    print(f"❌ SELL Signals (confidence ≥70): {sell_signals}")
    print(f"➡️  HOLD Signals: {hold_signals}")
    
    print("\nDetailed Results:")
    for result in results:
        if result.signal != Signal.HOLD:
            confidence_str = "🟢 STRONG" if result.confidence >= 70 else "🟡 MODERATE" if result.confidence >= 50 else "🔴 WEAK"
            print(f"  {result.pair}: {result.signal.value} ({result.confidence:.1f}%) {confidence_str}")


async def example_4_backtest():
    """Example 4: Backtest strategy on historical data"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Strategy Backtesting")
    print("="*60 + "\n")
    
    bot = TradingBot()
    
    # Get historical data
    print("📊 Fetching historical data...")
    candles = await BinanceREST.get_klines("BTC/USDT", "1h", limit=500)
    
    if candles:
        # Convert to OHLC
        ohlc_data = [
            OHLC(
                timestamp=c['timestamp'],
                open=c['open'],
                high=c['high'],
                low=c['low'],
                close=c['close'],
                volume=c['volume']
            )
            for c in candles
        ]
        
        # Backtest
        backtester = Backtester(initial_balance=1000)
        result = backtester.test_strategy(
            ohlc_data,
            lambda candles: bot.analyze(candles, "BTC/USDT", "1h"),
            risk_percent=2
        )
        
        print("\n✅ Backtest Complete!")
        print(f"Initial Balance: $1000.00")
        print(f"Final Balance: ${1000 + result.net_profit:.2f}")


async def example_5_config_management():
    """Example 5: Configuration management"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Configuration Management")
    print("="*60 + "\n")
    
    # Load config
    config = ConfigLoader.load("config.json")
    
    print("📋 Current Configuration:")
    print(f"  Risk Percentage: {config.get('trading', {}).get('risk_percent', 2)}%")
    print(f"  Confidence Threshold: {config.get('trading', {}).get('confidence_threshold', 70)}%")
    print(f"  Trading Pairs (Crypto): {len(config.get('trading', {}).get('crypto_pairs', []))} pairs")
    print(f"  Trading Pairs (Forex): {len(config.get('trading', {}).get('forex_pairs', []))} pairs")
    
    # Modify config
    config['trading']['risk_percent'] = 2.5
    ConfigLoader.save(config, "config_custom.json")
    print("\n✅ Custom configuration saved to config_custom.json")


def example_6_signal_strength():
    """Example 6: Understand confidence scoring"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Confidence Scoring Explanation")
    print("="*60 + "\n")
    
    print("""
The bot uses a weighted scoring system:

📊 ANALYSIS COMPONENTS (Total 100 points)
├─ Candlestick Patterns  (40 points) - 40%
│  ✓ Bullish Engulfing: +40
│  ✓ Bearish Engulfing: -40
│  ✓ Hammer: +30
│  ✓ Shooting Star: -30
│  ✓ Breakout Up: +35
│  ✓ Breakout Down: -35
│
├─ Trend Analysis       (30 points) - 30%
│  ✓ EMA(20) > EMA(50): +30 (Uptrend)
│  ✓ EMA(20) < EMA(50): -30 (Downtrend)
│
├─ Momentum             (20 points) - 20%
│  ✓ RSI < 30: +20 (Oversold, BUY)
│  ✓ RSI > 70: -20 (Overbought, SELL)
│
└─ Support/Resistance   (10 points) - 10%
   ✓ Price near support: +10 (BUY)
   ✓ Price near resistance: -10 (SELL)

CONFIDENCE LEVELS:
🔴 WEAK:        0-49%   (Don't trade)
🟡 MODERATE:   50-69%   (Optional, use wider stops)
🟢 STRONG:     70-100%  (High probability signals)

EXAMPLE SIGNAL:
Signal: BUY with Confidence 87%

Reasoning:
  ✅ Bullish engulfing pattern (+40)
  ✅ EMA(20) > EMA(50) - Uptrend (+30)
  ✅ RSI < 30 - Oversold (+20)
  ✅ Price near support (+10)
  ────────────────────────
  Total: 100 points → 87% confidence
    """)


async def main():
    """Run all examples"""
    print("""
╔════════════════════════════════════════════════════════════╗
║          BINARY TRADING BOT - USAGE EXAMPLES               ║
║      Professional Analysis with Real-Time Data             ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    try:
        # Run examples
        await example_1_analyze_crypto()
        await asyncio.sleep(2)
        
        await example_2_analyze_forex()
        await asyncio.sleep(2)
        
        await example_3_multi_pair_scan()
        await asyncio.sleep(2)
        
        await example_4_backtest()
        await asyncio.sleep(2)
        
        await example_5_config_management()
        
        example_6_signal_strength()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
