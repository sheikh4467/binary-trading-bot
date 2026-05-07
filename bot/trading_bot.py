"""
Professional Binary Trading Bot
Elite-level candlestick analysis with real-time data
"""

import logging
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class Signal(Enum):
    """Trading signals"""
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class OHLC:
    """OHLC candlestick data"""
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass
class TradingAnalysis:
    """Trading analysis result"""
    pair: str
    timeframe: str
    signal: Signal
    confidence: float  # 0-100
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    reasoning: List[str]
    analysis_time: datetime


class TechnicalIndicators:
    """Calculate technical indicators"""
    
    @staticmethod
    def sma(data: List[float], period: int) -> List[float]:
        """Simple Moving Average"""
        return np.convolve(data, np.ones(period)/period, mode='valid').tolist()
    
    @staticmethod
    def ema(data: List[float], period: int) -> List[float]:
        """Exponential Moving Average"""
        ema_vals = []
        multiplier = 2 / (period + 1)
        ema = data[0]
        ema_vals.append(ema)
        
        for price in data[1:]:
            ema = (price - ema) * multiplier + ema
            ema_vals.append(ema)
        
        return ema_vals
    
    @staticmethod
    def rsi(data: List[float], period: int = 14) -> List[float]:
        """Relative Strength Index"""
        deltas = np.diff(data)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.convolve(gains, np.ones(period)/period, mode='valid')
        avg_loss = np.convolve(losses, np.ones(period)/period, mode='valid')
        
        rs = avg_gain / (avg_loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.tolist()
    
    @staticmethod
    def macd(data: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple:
        """MACD indicator"""
        ema_fast = TechnicalIndicators.ema(data, fast)
        ema_slow = TechnicalIndicators.ema(data, slow)
        
        # Align lengths
        min_len = min(len(ema_fast), len(ema_slow))
        macd_line = np.array(ema_fast[-min_len:]) - np.array(ema_slow[-min_len:])
        signal_line = TechnicalIndicators.ema(macd_line.tolist(), signal)
        
        return macd_line.tolist(), signal_line
    
    @staticmethod
    def bollinger_bands(data: List[float], period: int = 20, std_dev: int = 2) -> Tuple:
        """Bollinger Bands"""
        sma = TechnicalIndicators.sma(data, period)
        variance = np.convolve(data, np.ones(period), mode='valid') / period
        std = np.std(np.array(data).reshape(-1, period), axis=1)
        
        upper = sma + (std * std_dev)
        lower = sma - (std * std_dev)
        
        return sma, upper.tolist(), lower.tolist()
    
    @staticmethod
    def atr(high: List[float], low: List[float], close: List[float], period: int = 14) -> List[float]:
        """Average True Range"""
        tr_vals = []
        
        for i in range(len(high)):
            tr1 = high[i] - low[i]
            tr2 = abs(high[i] - close[i-1]) if i > 0 else 0
            tr3 = abs(low[i] - close[i-1]) if i > 0 else 0
            tr = max(tr1, tr2, tr3)
            tr_vals.append(tr)
        
        atr = TechnicalIndicators.sma(tr_vals, period)
        return atr


class CandlePatternRecognition:
    """Recognize candlestick patterns"""
    
    @staticmethod
    def is_bullish_engulfing(candles: List[OHLC], idx: int) -> bool:
        """Bullish engulfing pattern"""
        if idx < 1:
            return False
        prev = candles[idx - 1]
        curr = candles[idx]
        
        # Previous is bearish, current is bullish and engulfs
        return (prev.close < prev.open and 
                curr.close > curr.open and
                curr.open < prev.close and
                curr.close > prev.open)
    
    @staticmethod
    def is_bearish_engulfing(candles: List[OHLC], idx: int) -> bool:
        """Bearish engulfing pattern"""
        if idx < 1:
            return False
        prev = candles[idx - 1]
        curr = candles[idx]
        
        return (prev.close > prev.open and
                curr.close < curr.open and
                curr.open > prev.close and
                curr.close < prev.open)
    
    @staticmethod
    def is_pin_bar(candles: List[OHLC], idx: int, threshold: float = 0.3) -> Tuple[bool, str]:
        """Pin bar pattern (hammer or shooting star)"""
        if idx < 0:
            return False, ""
        
        candle = candles[idx]
        body = abs(candle.close - candle.open)
        total_range = candle.high - candle.low
        
        if total_range == 0:
            return False, ""
        
        body_ratio = body / total_range
        
        if body_ratio > threshold:
            return False, ""
        
        upper_wick = candle.high - max(candle.open, candle.close)
        lower_wick = min(candle.open, candle.close) - candle.low
        
        # Hammer: lower wick > upper wick
        if lower_wick > upper_wick * 2:
            return True, "HAMMER"
        
        # Shooting star: upper wick > lower wick
        if upper_wick > lower_wick * 2:
            return True, "SHOOTING_STAR"
        
        return False, ""
    
    @staticmethod
    def is_inside_bar(candles: List[OHLC], idx: int) -> bool:
        """Inside bar pattern (consolidation)"""
        if idx < 1:
            return False
        prev = candles[idx - 1]
        curr = candles[idx]
        
        return (curr.high < prev.high and curr.low > prev.low)
    
    @staticmethod
    def is_breakout(candles: List[OHLC], idx: int, lookback: int = 20) -> Tuple[bool, str]:
        """Breakout pattern detection"""
        if idx < lookback:
            return False, ""
        
        recent = candles[idx - lookback:idx + 1]
        highs = [c.high for c in recent]
        lows = [c.low for c in recent]
        
        resistance = max(highs[:-1])
        support = min(lows[:-1])
        current = recent[-1]
        
        if current.close > resistance and current.close > current.open:
            return True, "BREAKOUT_UP"
        elif current.close < support and current.close < current.open:
            return True, "BREAKOUT_DOWN"
        
        return False, ""


class SupportResistance:
    """Calculate support and resistance levels"""
    
    @staticmethod
    def find_levels(candles: List[OHLC], lookback: int = 20) -> Tuple[float, float]:
        """Find support and resistance levels"""
        if len(candles) < lookback:
            candles_window = candles
        else:
            candles_window = candles[-lookback:]
        
        highs = [c.high for c in candles_window]
        lows = [c.low for c in candles_window]
        
        resistance = max(highs)
        support = min(lows)
        
        return support, resistance


class TradingBot:
    """Main trading bot with elite-level analysis"""
    
    def __init__(self, risk_percent: float = 2.0):
        self.risk_percent = risk_percent
        self.indicators = TechnicalIndicators()
        self.patterns = CandlePatternRecognition()
        self.sr = SupportResistance()
    
    def analyze(self, candles: List[OHLC], pair: str, timeframe: str) -> TradingAnalysis:
        """Perform elite-level trading analysis"""
        
        if len(candles) < 50:
            logger.warning(f"Not enough candles for {pair} {timeframe}")
            return TradingAnalysis(
                pair=pair, timeframe=timeframe, signal=Signal.HOLD,
                confidence=0, entry_price=0, stop_loss=0, take_profit=0,
                risk_reward_ratio=0, reasoning=["Insufficient data"], 
                analysis_time=datetime.now()
            )
        
        closes = [c.close for c in candles]
        highs = [c.high for c in candles]
        lows = [c.low for c in candles]
        volumes = [c.volume for c in candles]
        
        # Calculate indicators
        ema_20 = self.indicators.ema(closes, 20)
        ema_50 = self.indicators.ema(closes, 50)
        rsi = self.indicators.rsi(closes, 14)
        macd_line, macd_signal = self.indicators.macd(closes)
        atr = self.indicators.atr(highs, lows, closes, 14)
        
        # Get latest values
        current_close = closes[-1]
        current_ema_20 = ema_20[-1] if ema_20 else current_close
        current_ema_50 = ema_50[-1] if ema_50 else current_close
        current_rsi = rsi[-1] if rsi else 50
        current_atr = atr[-1] if atr else 0
        support, resistance = self.sr.find_levels(candles)
        
        # Score calculation (0-100)
        score_components = {
            "candle_pattern": 0,
            "trend": 0,
            "momentum": 0,
            "support_resistance": 0
        }
        
        reasoning = []
        
        # 1. Candle Pattern Analysis (40% weight)
        bullish_engulf = self.patterns.is_bullish_engulfing(candles, len(candles) - 1)
        bearish_engulf = self.patterns.is_bearish_engulfing(candles, len(candles) - 1)
        pin_bar, pin_type = self.patterns.is_pin_bar(candles, len(candles) - 1)
        inside_bar = self.patterns.is_inside_bar(candles, len(candles) - 1)
        breakout, breakout_type = self.patterns.is_breakout(candles, len(candles) - 1)
        
        signal_type = Signal.HOLD
        
        if bullish_engulf:
            score_components["candle_pattern"] = 40
            reasoning.append("✅ Bullish engulfing pattern")
            signal_type = Signal.BUY
        elif bearish_engulf:
            score_components["candle_pattern"] = -40
            reasoning.append("✅ Bearish engulfing pattern")
            signal_type = Signal.SELL
        elif pin_bar and pin_type == "HAMMER":
            score_components["candle_pattern"] = 30
            reasoning.append("✅ Hammer pattern (reversal)")
            signal_type = Signal.BUY
        elif pin_bar and pin_type == "SHOOTING_STAR":
            score_components["candle_pattern"] = -30
            reasoning.append("✅ Shooting star pattern (reversal)")
            signal_type = Signal.SELL
        elif breakout and "UP" in breakout_type:
            score_components["candle_pattern"] = 35
            reasoning.append("✅ Upside breakout detected")
            signal_type = Signal.BUY
        elif breakout and "DOWN" in breakout_type:
            score_components["candle_pattern"] = -35
            reasoning.append("✅ Downside breakout detected")
            signal_type = Signal.SELL
        
        # 2. Trend Analysis (30% weight)
        if current_ema_20 > current_ema_50:
            score_components["trend"] = 30
            reasoning.append("📈 EMA(20) above EMA(50) - Uptrend")
            if signal_type == Signal.HOLD:
                signal_type = Signal.BUY
        elif current_ema_20 < current_ema_50:
            score_components["trend"] = -30
            reasoning.append("📉 EMA(20) below EMA(50) - Downtrend")
            if signal_type == Signal.HOLD:
                signal_type = Signal.SELL
        else:
            reasoning.append("➡️ Sideways trend (no clear direction)")
        
        # 3. Momentum Analysis (20% weight)
        if current_rsi < 30:
            score_components["momentum"] = 20
            reasoning.append("🔴 RSI oversold (<30) - Reversal potential")
            if signal_type == Signal.HOLD:
                signal_type = Signal.BUY
        elif current_rsi > 70:
            score_components["momentum"] = -20
            reasoning.append("🔵 RSI overbought (>70) - Reversal potential")
            if signal_type == Signal.HOLD:
                signal_type = Signal.SELL
        else:
            reasoning.append(f"🟢 RSI neutral ({current_rsi:.1f})")
        
        # 4. Support/Resistance (10% weight)
        distance_to_resistance = ((resistance - current_close) / current_close) * 100
        distance_to_support = ((current_close - support) / current_close) * 100
        
        if current_close < support + (current_atr * 0.5):
            score_components["support_resistance"] = 10
            reasoning.append(f"💪 Price near support ({support:.5f})")
            if signal_type == Signal.HOLD:
                signal_type = Signal.BUY
        elif current_close > resistance - (current_atr * 0.5):
            score_components["support_resistance"] = -10
            reasoning.append(f"⚠️ Price near resistance ({resistance:.5f})")
            if signal_type == Signal.HOLD:
                signal_type = Signal.SELL
        
        # Calculate final confidence
        if signal_type == Signal.BUY:
            total_score = sum(v for v in score_components.values() if v > 0)
            max_score = sum(abs(v) for v in score_components.values() if v > 0)
        elif signal_type == Signal.SELL:
            total_score = sum(abs(v) for v in score_components.values() if v < 0)
            max_score = sum(abs(v) for v in score_components.values() if v < 0)
        else:
            total_score = 0
            max_score = 100
        
        confidence = (total_score / max_score * 100) if max_score > 0 else 0
        confidence = min(100, max(0, confidence))
        
        # Calculate entry, stop loss, take profit
        if signal_type == Signal.BUY:
            entry_price = current_close
            stop_loss = support if support > 0 else (current_close - current_atr * 2)
            take_profit = resistance if resistance > 0 else (current_close + current_atr * 2)
        elif signal_type == Signal.SELL:
            entry_price = current_close
            stop_loss = resistance if resistance > 0 else (current_close + current_atr * 2)
            take_profit = support if support > 0 else (current_close - current_atr * 2)
        else:
            entry_price = current_close
            stop_loss = current_close
            take_profit = current_close
        
        # Risk/Reward ratio
        risk = abs(entry_price - stop_loss)
        reward = abs(take_profit - entry_price)
        risk_reward_ratio = (reward / risk) if risk > 0 else 0
        
        return TradingAnalysis(
            pair=pair,
            timeframe=timeframe,
            signal=signal_type,
            confidence=confidence,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward_ratio=risk_reward_ratio,
            reasoning=reasoning,
            analysis_time=datetime.now()
        )
    
    def format_analysis(self, analysis: TradingAnalysis) -> str:
        """Format analysis for display"""
        confidence_level = "🔴 WEAK" if analysis.confidence < 50 else "🟡 MODERATE" if analysis.confidence < 70 else "🟢 STRONG"
        
        output = f"""
╔════════════════════════════════════════════════════════════╗
║              BINARY TRADING ANALYSIS REPORT                ║
╚════════════════════════════════════════════════════════════╝

📊 Market: {analysis.pair} ({analysis.timeframe})
🎯 Signal: {analysis.signal.value}
💪 Confidence: {analysis.confidence:.1f}% {confidence_level}
⏰ Analysis Time: {analysis.analysis_time.strftime('%Y-%m-%d %H:%M:%S')}

📈 PRICING
├─ Entry Price: {analysis.entry_price:.5f}
├─ Stop Loss: {analysis.stop_loss:.5f}
├─ Take Profit: {analysis.take_profit:.5f}
└─ Risk/Reward: {analysis.risk_reward_ratio:.2f}:1

📋 ANALYSIS REASONING
"""
        for reason in analysis.reasoning:
            output += f"   {reason}\n"
        
        output += """
╚════════════════════════════════════════════════════════════╝
"""
        return output
