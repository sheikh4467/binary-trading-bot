````markdown name=README.md url=https://github.com/sheikh4467/binary-trading-bot

# 🚀 Professional Binary Trading Bot

**Elite-level candlestick analysis with real-time live data, professional trading signals, and confidence scoring.**

An advanced binary trading bot that analyzes cryptocurrency, forex, commodities, and indices using professional technical analysis. Every signal includes a **0-100% confidence score**, entry/exit prices, stop-loss, take-profit, and risk/reward ratios.

---

## 🎯 Key Features

✅ **Professional Candlestick Analysis**
- 5 advanced pattern recognition systems
- Bullish/Bearish Engulfing, Hammer, Shooting Star, Breakouts
- Real candlestick data (zero mock data)

✅ **6 Technical Indicators**
- EMA (20, 50) for trend confirmation
- RSI (14) for momentum analysis
- MACD for trend changes
- Bollinger Bands for volatility
- ATR for dynamic position sizing
- Support & Resistance levels

✅ **Intelligent Signal Generation**
- BUY/SELL/HOLD signals with weighted confidence
- Automatic stop-loss & take-profit calculation
- Risk/reward ratio optimization
- Detailed reasoning for each signal

✅ **Real-Time Data Sources** (100% FREE, NO MOCK DATA)
- **Binance WebSocket**: Live cryptocurrency data
- **Finnhub API**: Forex, commodities, stocks
- **Quotex Integration**: Binary options platform ready

✅ **Advanced Features**
- Multi-timeframe analysis (1m to 1d)
- Backtesting framework with detailed statistics
- Multi-channel notifications (Telegram, Discord, Email)
- Risk management with position sizing
- Continuous monitoring mode

---

## 📊 What You Can Trade

### Cryptocurrencies
- Bitcoin (BTC), Ethereum (ETH), Binance Coin (BNB)
- Cardano (ADA), Ripple (XRP), Litecoin (LTC)
- Polkadot (DOT), Chainlink (LINK), Polygon (MATIC), Dogecoin (DOGE)

### Forex Pairs
- EURUSD, GBPUSD, USDJPY, AUDUSD, NZDUSD
- EURJPY, EURGBP, AUDJPY, NZDJPY, USDCHF, USDCAD

### Commodities
- Gold (XAUUSD), Silver (XAGUSD), Oil (WTIUSD)

### Indices
- US 30, US 500, EUR/USD Index

---

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/sheikh4467/binary-trading-bot.git
cd binary-trading-bot
pip install -r requirements.txt
```

### 2. Run Single Analysis

```bash
# Analyze EURUSD on 5-minute timeframe
python main.py EURUSD 5m

# Analyze Bitcoin
python main.py BTCUSDT 5m

# Run with backtesting
python main.py ETHUSDT 1h backtest
```

### 3. Run Examples

```bash
# See all examples
python examples.py
```

### 4. Continuous Monitoring

```bash
# Monitor specific pairs continuously
python main.py continuous
```

---

## 📋 Signal Example

```
╔════════════════════════════════════════════════════════════╗
║              BINARY TRADING ANALYSIS REPORT                ║
╚════════════════════════════════════════════════════════════╝

📊 Market: EURUSD (5m)
🎯 Signal: BUY
💪 Confidence: 87% 🟢 STRONG
⏰ Analysis Time: 2026-05-07 10:30:45

📈 PRICING
├─ Entry Price: 1.0875
├─ Stop Loss: 1.0820
├─ Take Profit: 1.0920
└─ Risk/Reward: 0.82:1

📋 ANALYSIS REASONING
   ✅ Bullish engulfing pattern
   📈 EMA(20) above EMA(50) - Uptrend
   🟢 RSI neutral (55.3)
   💪 Price near support (1.0805)

╚════════════════════════════════════════════════════════════╝
```

---

## ⚙️ Configuration

Edit `config.json` to customize:

```json
{
  "trading": {
    "confidence_threshold": 70,
    "pairs": ["EURUSD", "GBPUSD"],
    "timeframes": ["5m", "1h"]
  },
  "indicators": {
    "ema_fast_period": 20,
    "ema_slow_period": 50,
    "rsi_period": 14
  },
  "notifications": {
    "telegram": { "enabled": false },
    "discord": { "enabled": false }
  }
}
```

---

## 📊 How Confidence Works

The bot analyzes 4 components with weighted scoring:

| Component | Weight | Description |
|-----------|--------|-------------|
| Candlestick Pattern | 40% | Recognizes 5 professional patterns |
| Trend Analysis | 30% | EMA crossover confirmation |
| Momentum | 20% | RSI levels and oscillators |
| Support/Resistance | 10% | Price proximity to key levels |

**Example Calculation:**
```
✅ Bullish engulfing       +40 points (40%)
✅ Uptrend (EMA 20>50)     +30 points (30%)
✅ Oversold RSI            +20 points (20%)
✅ Near support level      +10 points (10%)
─────────────────────────────────────────
Total: 100 points → 87% confidence 🟢 STRONG
```

---

## 🔔 Notifications Setup

### Telegram
1. Create a bot: https://t.me/BotFather
2. Get your chat ID
3. Add to `config.json`:
```json
"telegram": {
  "enabled": true,
  "bot_token": "YOUR_BOT_TOKEN",
  "chat_id": "YOUR_CHAT_ID"
}
```

### Discord
1. Create a webhook in Discord channel settings
2. Add to `config.json`:
```json
"discord": {
  "enabled": true,
  "webhook_url": "YOUR_WEBHOOK_URL"
}
```

---

## 🧪 Backtesting

Test your strategy on historical data:

```bash
python main.py BTCUSDT 1h backtest
```

Generates report with:
- Win rate percentage
- Profit factor
- Sharpe ratio (risk-adjusted returns)
- Max drawdown
- Average win/loss

---

## 📁 Project Structure

```
binary-trading-bot/
├── bot/
│   └── trading_bot.py          # Core analysis engine
├── integrations/
│   ├── binance.py              # Binance WebSocket & REST API
│   ├── finnhub.py              # Forex & commodity data
│   └── quotex.py               # Binary options platform
├── utils/
│   ├── notifications.py        # Alert system
│   └── backtest.py             # Backtesting framework
├── config/
│   └── loader.py               # Config management
├── main.py                     # Bot entry point
├── examples.py                 # Usage examples
├── config.json                 # Configuration
└── README.md                   # This file
```

---

## 🎓 Technical Indicators Explained

### EMA (Exponential Moving Average)
- **Fast (20)**: Tracks recent price action
- **Slow (50)**: Tracks long-term trend
- **Signal**: Buy when EMA20 > EMA50

### RSI (Relative Strength Index)
- **< 30**: Oversold (potential buy)
- **> 70**: Overbought (potential sell)
- **30-70**: Neutral zone

### MACD (Moving Average Convergence Divergence)
- **Positive**: Bullish momentum
- **Negative**: Bearish momentum
- **Crossover**: Trend change signals

### ATR (Average True Range)
- Measures volatility
- Used for dynamic stop-loss sizing
- Larger ATR = Higher volatility

### Bollinger Bands
- **Upper Band**: Resistance level
- **Lower Band**: Support level
- **Breakout**: Price moving beyond bands

---

## 🔐 Risk Management

The bot includes:
- ✅ Automatic stop-loss calculation
- ✅ Risk-reward ratio optimization
- ✅ Position sizing based on risk percentage
- ✅ Max concurrent trades limit
- ✅ Daily trade limit

Configure in `config.json`:
```json
"risk_management": {
  "risk_percent": 2.0,
  "max_trades_per_day": 10,
  "max_concurrent_trades": 3
}
```

---

## 🔍 Pattern Recognition

### 1. Bullish Engulfing
- Previous candle: Bearish
- Current candle: Bullish and fully engulfs previous
- Signal: Strong BUY

### 2. Bearish Engulfing
- Previous candle: Bullish
- Current candle: Bearish and fully engulfs previous
- Signal: Strong SELL

### 3. Hammer
- Small body with long lower wick
- Appears at bottom of downtrend
- Signal: BUY (reversal)

### 4. Shooting Star
- Small body with long upper wick
- Appears at top of uptrend
- Signal: SELL (reversal)

### 5. Breakout
- Price breaks above resistance or below support
- Signal: BUY (above) or SELL (below)

---

## 📝 API Keys Required (All Free)

### Finnhub (Optional, for Forex)
- Get free key: https://finnhub.io
- 60 API calls/minute
- Add to `config.json`

### Binance
- No API key needed for historical data
- Public WebSocket streaming
- Fully free forever

### Telegram (Optional)
- Create bot: https://t.me/BotFather
- Completely free

### Discord (Optional)
- Create webhook in channel settings
- Completely free

---

## 🚨 Important Notes

⚠️ **This bot is for educational purposes and analysis only**
- Past performance ≠ Future results
- Always use proper risk management
- Start with small positions
- Never risk more than you can afford to lose
- This is NOT financial advice

✅ **Best Practices**
- Backtest before live trading
- Monitor bot performance regularly
- Use appropriate timeframes for your strategy
- Adjust confidence threshold based on results
- Keep API keys secure

---

## 📈 Performance Metrics

The bot tracks:
- **Win Rate**: Percentage of winning trades
- **Profit Factor**: Gross profit / Gross loss
- **Sharpe Ratio**: Risk-adjusted returns
- **Max Drawdown**: Largest peak-to-trough decline
- **Average Win/Loss**: Mean profit and loss per trade

---

## 🐛 Troubleshooting

### No data returned
```
❌ Ensure internet connection is active
❌ Check if pair symbol is correct
❌ Verify API rate limits not exceeded
```

### Slow performance
```
✅ Reduce number of pairs analyzed
✅ Use longer timeframes (5m -> 15m)
✅ Reduce analysis frequency
```

### Notification not working
```
✅ Verify API key/token is correct
✅ Check webhook URL is valid
✅ Ensure notifications are enabled in config
```

---

## 📞 Support & Issues

For issues or questions:
1. Check `config.json` settings
2. Review bot logs in `trading_bot.log`
3. Test with examples: `python examples.py`
4. Enable DEBUG logging for detailed info

---

## 📚 Learning Resources

- **Technical Analysis**: [Investopedia](https://www.investopedia.com)
- **Candlestick Patterns**: [TradingView](https://www.tradingview.com)
- **Risk Management**: [BabyPips](https://www.babypips.com)
- **Python Async**: [Python Docs](https://docs.python.org/3/library/asyncio.html)

---

## 📄 License

This project is open source and available under the MIT License.

---

## ⭐ Features Roadmap

- [ ] Machine Learning predictions
- [ ] More pattern recognition (3 candle patterns)
- [ ] Advanced position management
- [ ] Performance analytics dashboard
- [ ] Mobile app integration
- [ ] Cloud deployment guide
- [ ] Strategy optimizer
- [ ] Volume profile analysis

---

## 🎯 Getting Started Checklist

- [ ] Clone repository
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Get API key from Finnhub (optional)
- [ ] Configure `config.json`
- [ ] Run examples: `python examples.py`
- [ ] Backtest strategy: `python main.py EURUSD 1h backtest`
- [ ] Setup notifications (optional)
- [ ] Start live analysis: `python main.py EURUSD 5m`

---

## 💡 Pro Tips

1. **Multi-Timeframe**: Analyze multiple timeframes to confirm signals
2. **Risk Management**: Always use stop-loss, never risk > 2% per trade
3. **Backtesting**: Always backtest before trading live
4. **Notifications**: Setup alerts to never miss opportunities
5. **Logging**: Check logs regularly to understand bot behavior
6. **Diversification**: Trade multiple pairs with different characteristics
7. **Market Hours**: Forex liquid during European/US sessions
8. **Crypto**: Trades 24/7 with consistent volatility

---

**Created with ❤️ for professional traders**

*Last Updated: May 2026*

````
