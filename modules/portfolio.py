"""
投资组合管理模块
"""

import pandas as pd
from datetime import datetime


class Portfolio:
    """投资组合管理"""

    def __init__(self, initial_capital):
        """
        初始化投资组合

        Args:
            initial_capital: 初始资金
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = {}  # {symbol: {'shares': x, 'avg_cost': y}}
        self.history = []

    @property
    def total_capital(self):
        """总资金（含持仓市值）"""
        return self.cash + self.position_value

    @property
    def position_value(self):
        """持仓市值"""
        total = 0
        for symbol, pos in self.positions.items():
            total += pos['shares'] * pos['avg_cost']
        return total

    def buy(self, symbol, shares, price):
        """
        买入股票

        Args:
            symbol: 股票代码
            shares: 买入股数
            price: 买入价格

        Returns:
            bool: 是否成功
        """
        cost = shares * price
        if cost > self.cash:
            return False

        self.cash -= cost

        if symbol in self.positions:
            # 追加买入
            existing_shares = self.positions[symbol]['shares']
            existing_cost = self.positions[symbol]['avg_cost']
            total_cost = existing_shares * existing_cost + cost
            new_shares = existing_shares + shares
            new_avg_cost = total_cost / new_shares

            self.positions[symbol] = {
                'shares': new_shares,
                'avg_cost': new_avg_cost
            }
        else:
            # 新买入
            self.positions[symbol] = {
                'shares': shares,
                'avg_cost': price
            }

        self._record_trade(symbol, 'BUY', shares, price)
        return True

    def sell(self, symbol, shares, price):
        """
        卖出股票

        Args:
            symbol: 股票代码
            shares: 卖出股数
            price: 卖出价格

        Returns:
            bool: 是否成功
        """
        if symbol not in self.positions:
            return False

        if self.positions[symbol]['shares'] < shares:
            return False

        revenue = shares * price
        self.cash += revenue

        # 更新持仓
        self.positions[symbol]['shares'] -= shares
        if self.positions[symbol]['shares'] == 0:
            del self.positions[symbol]

        self._record_trade(symbol, 'SELL', shares, price)
        return True

    def get_position(self, symbol):
        """
        获取持仓

        Args:
            symbol: 股票代码

        Returns:
            int: 持仓股数
        """
        if symbol in self.positions:
            return self.positions[symbol]['shares']
        return 0

    def get_positions_df(self):
        """
        获取持仓DataFrame

        Returns:
            DataFrame: 持仓数据
        """
        if not self.positions:
            return pd.DataFrame()

        data = []
        for symbol, pos in self.positions.items():
            data.append({
                'symbol': symbol,
                'shares': pos['shares'],
                'avg_cost': pos['avg_cost'],
                'market_value': pos['shares'] * pos['avg_cost']
            })

        df = pd.DataFrame(data)
        df['weight'] = df['market_value'] / self.total_capital
        return df

    def _record_trade(self, symbol, action, shares, price):
        """记录交易"""
        self.history.append({
            'timestamp': datetime.now(),
            'symbol': symbol,
            'action': action,
            'shares': shares,
            'price': price,
            'cash': self.cash,
            'total_capital': self.total_capital
        })

    def get_history_df(self):
        """
        获取交易历史DataFrame

        Returns:
            DataFrame: 交易历史
        """
        if not self.history:
            return pd.DataFrame()

        return pd.DataFrame(self.history)

    def rebalance(self, target_weights, prices):
        """
        重新平衡投资组合

        Args:
            target_weights: 目标权重字典 {symbol: weight}
            prices: 当前价格字典 {symbol: price}

        Returns:
            dict: 交易指令
        """
        trades = {}

        for symbol, target_weight in target_weights.items():
            target_value = self.total_capital * target_weight
            current_shares = self.get_position(symbol)
            current_price = prices.get(symbol, 0)

            if current_price == 0:
                continue

            current_value = current_shares * current_price
            diff_value = target_value - current_value
            diff_shares = int(diff_value / current_price)

            if diff_shares > 0:
                trades[symbol] = {'action': 'BUY', 'shares': diff_shares}
            elif diff_shares < 0:
                trades[symbol] = {'action': 'SELL', 'shares': abs(diff_shares)}

        return trades

    def reset(self):
        """重置投资组合"""
        self.cash = self.initial_capital
        self.positions = {}
        self.history = []
