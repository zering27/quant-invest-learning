"""
技术指标计算模块
"""

import pandas as pd
import numpy as np


class Indicators:
    """技术指标计算"""

    @staticmethod
    def calculate_ma(df, periods=None):
        """
        计算移动平均线

        Args:
            df: 包含close列的DataFrame
            periods: 周期列表，如 [5, 10, 20, 60]

        Returns:
            DataFrame: 添加了ma5, ma10, ma20, ma60列
        """
        if periods is None:
            periods = [5, 10, 20, 60]

        for period in periods:
            df[f'ma{period}'] = df['close'].rolling(window=period).mean()
        return df

    @staticmethod
    def calculate_ema(df, periods=None):
        """计算指数移动平均线"""
        if periods is None:
            periods = [12, 26]

        for period in periods:
            df[f'ema{period}'] = df['close'].ewm(span=period, adjust=False).mean()
        return df

    @staticmethod
    def calculate_rsi(df, period=14):
        """
        计算RSI相对强弱指标

        Args:
            df: 包含close列的DataFrame
            period: RSI周期，默认14

        Returns:
            DataFrame: 添加了rsi列
        """
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        return df

    @staticmethod
    def calculate_bollinger_bands(df, period=20, std_dev=2):
        """
        计算布林带

        Args:
            df: 包含close列的DataFrame
            period: 周期，默认20
            std_dev: 标准差倍数，默认2

        Returns:
            DataFrame: 添加了bb_upper, bb_middle, bb_lower列
        """
        df['bb_middle'] = df['close'].rolling(window=period).mean()
        df['bb_std'] = df['close'].rolling(window=period).std()
        df['bb_upper'] = df['bb_middle'] + (df['bb_std'] * std_dev)
        df['bb_lower'] = df['bb_middle'] - (df['bb_std'] * std_dev)
        return df

    @staticmethod
    def calculate_macd(df, fast=12, slow=26, signal=9):
        """
        计算MACD指标

        Args:
            df: 包含close列的DataFrame
            fast: 快线周期，默认12
            slow: 慢线周期，默认26
            signal: 信号线周期，默认9

        Returns:
            DataFrame: 添加了macd, macd_signal, macd_hist列
        """
        df['ema_fast'] = df['close'].ewm(span=fast, adjust=False).mean()
        df['ema_slow'] = df['close'].ewm(span=slow, adjust=False).mean()
        df['macd'] = df['ema_fast'] - df['ema_slow']
        df['macd_signal'] = df['macd'].ewm(span=signal, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']
        return df

    @staticmethod
    def calculate_kdj(df, n=9, m1=3, m2=3):
        """
        计算KDJ指标

        Args:
            df: 包含high, low, close列的DataFrame
            n: RSV周期，默认9
            m1: K周期，默认3
            m2: D周期，默认3

        Returns:
            DataFrame: 添加了kdj_k, kdj_d, kdj_j列
        """
        low_n = df['low'].rolling(window=n, min_periods=1).min()
        high_n = df['high'].rolling(window=n, min_periods=1).max()
        rsv = (df['close'] - low_n) / (high_n - low_n) * 100

        df['kdj_k'] = rsv.ewm(com=m1 - 1, adjust=False).mean()
        df['kdj_d'] = df['kdj_k'].ewm(com=m2 - 1, adjust=False).mean()
        df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
        return df

    @staticmethod
    def calculate_atr(df, period=14):
        """
        计算ATR平均真实波幅

        Args:
            df: 包含high, low, close列的DataFrame
            period: 周期，默认14

        Returns:
            DataFrame: 添加了atr列
        """
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())

        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['atr'] = tr.rolling(window=period).mean()
        return df

    @staticmethod
    def calculate_volume_ratio(df, period=5):
        """
        计算量比

        Args:
            df: 包含volume列的DataFrame
            period: 周期，默认5

        Returns:
            DataFrame: 添加了volume_ratio列
        """
        df['vol_ma'] = df['volume'].rolling(window=period, min_periods=1).mean()
        df['volume_ratio'] = df['volume'] / df['vol_ma']
        return df
