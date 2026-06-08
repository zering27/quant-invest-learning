"""
回测引擎模块
"""

import pandas as pd
import numpy as np
from datetime import datetime
from .data_fetcher import DataFetcher
from .indicators import Indicators
from .risk_manager import RiskManager
from .portfolio import Portfolio
import config


class Backtester:
    """回测引擎"""

    def __init__(self, params=None):
        """
        初始化回测引擎

        Args:
            params: 回测参数字典，包含:
                - stock_code: 股票代码
                - start_date: 开始日期
                - end_date: 结束日期
                - initial_capital: 初始资金
                - commission_rate: 手续费率
                - strategy: 策略类型
        """
        self.params = params or {}
        self.stock_code = self.params.get('stock_code', '600000')
        self.start_date = self.params.get('start_date', config.BACKTEST_CONFIG['default_start_date'])
        self.end_date = self.params.get('end_date', config.BACKTEST_CONFIG['default_end_date'])
        self.initial_capital = self.params.get('initial_capital', config.BACKTEST_CONFIG['initial_capital'])
        self.commission_rate = self.params.get('commission_rate', config.BACKTEST_CONFIG['commission_rate'])
        self.strategy = self.params.get('strategy', 'ma_cross')

        self.data_fetcher = DataFetcher()
        self.indicators = Indicators()
        self.risk_manager = RiskManager()
        self.portfolio = Portfolio(self.initial_capital)
        self.trades = []
        self.equity_curve = []

    def run(self):
        """
        执行回测

        Returns:
            dict: 回测结果，包含收益率、夏普比率、最大回撤等
        """
        # 获取数据
        df = self.data_fetcher.get_stock_data(self.stock_code, self.start_date, self.end_date)

        if df.empty:
            return {'error': '无法获取数据'}

        # 计算技术指标
        df = self.indicators.calculate_ma(df)
        df = self.indicators.calculate_rsi(df)
        df = self.indicators.calculate_bollinger_bands(df)

        # 生成交易信号
        df = self._generate_signals(df)

        # 执行回测
        self._execute_backtest(df)

        # 计算性能指标
        results = self._calculate_performance()
        results['trades'] = self.trades
        results['equity_curve'] = self.equity_curve

        return results

    def _generate_signals(self, df):
        """根据策略生成交易信号"""
        if self.strategy == 'ma_cross':
            # 均线交叉策略
            df['signal'] = 0
            df.loc[df['ma5'] > df['ma20'], 'signal'] = 1   # 金叉买入
            df.loc[df['ma5'] < df['ma20'], 'signal'] = -1  # 死叉卖出
        elif self.strategy == 'rsi':
            # RSI超买超卖策略
            df['signal'] = 0
            df.loc[df['rsi'] < 30, 'signal'] = 1   # 超卖买入
            df.loc[df['rsi'] > 70, 'signal'] = -1  # 超买卖出
        elif self.strategy == 'bollinger':
            # 布林带策略
            df['signal'] = 0
            df.loc[df['close'] < df['bb_lower'], 'signal'] = 1   # 价格低于下轨买入
            df.loc[df['close'] > df['bb_upper'], 'signal'] = -1   # 价格高于上轨卖出
        else:
            df['signal'] = 0

        return df

    def _execute_backtest(self, df):
        """执行回测逻辑"""
        position = 0
        cash = self.initial_capital
        entry_price = 0

        for i, row in df.iterrows():
            date = row['date']
            price = row['close']
            signal = row['signal']

            # 买入信号且无持仓
            if signal == 1 and position == 0:
                # 计算可买入数量（考虑手续费）
                max_shares = int(cash / (price * (1 + self.commission_rate)))
                position = max_shares
                cost = max_shares * price * (1 + self.commission_rate)
                cash -= cost
                entry_price = price
                self.trades.append({
                    'date': date,
                    'action': 'BUY',
                    'price': price,
                    'shares': max_shares,
                    'cash': cash
                })

            # 卖出信号且有持仓
            elif signal == -1 and position > 0:
                # 检查止损止盈
                should_sell, reason = self.risk_manager.check_risk(
                    entry_price, price, position * entry_price
                )

                if should_sell:
                    revenue = position * price * (1 - self.commission_rate - config.BACKTEST_CONFIG['stamp_tax'])
                    cash += revenue
                    pnl = revenue - (position * entry_price)
                    self.trades.append({
                        'date': date,
                        'action': 'SELL',
                        'price': price,
                        'shares': position,
                        'cash': cash,
                        'pnl': pnl,
                        'reason': reason
                    })
                    position = 0
                    entry_price = 0

            # 记录当日权益
            equity = cash + position * price
            self.equity_curve.append({
                'date': date,
                'equity': equity,
                'position': position,
                'cash': cash
            })

    def _calculate_performance(self):
        """计算回测性能指标"""
        if not self.equity_curve:
            return {}

        equity_df = pd.DataFrame(self.equity_curve)
        equity = equity_df['equity'].values

        # 总收益率
        total_return = (equity[-1] - self.initial_capital) / self.initial_capital

        # 年化收益率
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 0 else 0

        # 最大回撤
        peak = np.maximum.accumulate(equity)
        drawdown = (peak - equity) / peak
        max_drawdown = np.max(drawdown)

        # 夏普比率
        returns = np.diff(equity) / equity[:-1]
        sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0

        # 胜率
        winning_trades = [t for t in self.trades if t.get('action') == 'SELL' and t.get('pnl', 0) > 0]
        win_rate = len(winning_trades) / len([t for t in self.trades if t.get('action') == 'SELL']) if self.trades else 0

        return {
            'initial_capital': self.initial_capital,
            'final_equity': equity[-1],
            'total_return': total_return,
            'annual_return': annual_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'win_rate': win_rate,
            'total_trades': len([t for t in self.trades if t.get('action') == 'SELL']),
            'profit_factor': self._calculate_profit_factor()
        }

    def _calculate_profit_factor(self):
        """计算盈利因子"""
        profits = [t['pnl'] for t in self.trades if t.get('action') == 'SELL' and t.get('pnl', 0) > 0]
        losses = [abs(t['pnl']) for t in self.trades if t.get('action') == 'SELL' and t.get('pnl', 0) < 0]

        total_profit = sum(profits) if profits else 0
        total_loss = sum(losses) if losses else 1

        return total_profit / total_loss if total_loss > 0 else 0
