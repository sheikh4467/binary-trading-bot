"""
Configuration Loader
"""

import json
import logging
from typing import Dict
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage configuration"""
    
    @staticmethod
    def load(config_path: str = "config.json") -> Dict:
        """Load configuration from JSON file"""
        try:
            if not Path(config_path).exists():
                logger.warning(f"Config file {config_path} not found, using defaults")
                return ConfigLoader._get_defaults()
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            logger.info(f"✅ Loaded config from {config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return ConfigLoader._get_defaults()
    
    @staticmethod
    def _get_defaults() -> Dict:
        """Get default configuration"""
        return {
            "trading": {
                "enabled": True,
                "pairs": ["EURUSD", "GBPUSD"],
                "timeframes": ["5m", "1h"],
                "confidence_threshold": 70
            },
            "indicators": {
                "ema_fast": 20,
                "ema_slow": 50,
                "rsi_period": 14
            }
        }
    
    @staticmethod
    def save(config: Dict, config_path: str = "config.json"):
        """Save configuration to JSON file"""
        try:
            Path(config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info(f"✅ Saved config to {config_path}")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
