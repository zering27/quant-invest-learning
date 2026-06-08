"""
性能分析模块
"""

import pandas as pd
import numpy as np


class PerformanceAnalyzer:
    """性能分析器"""

    def __init__(self, trades, equity_curve, benchmark=None):
        """
        初始化性能分析器

        Args:
            trades: 交易记录列表
            equity_curve: 权益曲线列表
            benchmark: 基准收益率（可选）
        """
        self.trades = trades
        self.equity_curve = equity_curve
        self.benchmark = benchmark

    def analyze(self):
        """
        全面分析策略性能

        Returns:
            dict: 完整的性能指标
        """
        if not self.equity_curve:
            return {}

        equity_df = pd.DataFrame(self.equity_curve)

        return {
            'total_return': self._total_return(equity_df),
            'annual_return': self._annual_return(equity_df),
            'max_drawdown': self._max_drawdown(equity_df),
            'sharpe_ratio': self._sharpe_ratio(equity_df),
            'sortino_ratio': self._sortino_ratio(equity_df),
            'calmar_ratio': self._calmar_ratio(equity_df),
            'win_rate': self._win_rate(),
            'profit_factor': self._profit_factor(),
            'avg_holding_days': self._avg_holding_days(),
            'trade_stats': self._trade_statistics()
        }

    def _total_return(self, equity_df):
        """计算总收益率"""
        initial = equity_df['equity'].iloc[0]
        final = equity_df['equity'].iloc[-1]
        return (final - initial) / initial if initial > 0 else 0

    def _annual_return(self, equity_df):
        """计算年化收益率"""
        total_return = self._total_return(equity_df)
        days = len(equity_df)
        return (1 + total_return) ** (252 / days) - 1 if days > 252 else total_return

    def _max_drawdown(self, equity_df):
        """计算最大回撤"""
        equity = equity_df['equity'].values
        peak = np.maximum.accumulate(equity)
        drawdown = (peak - equity) / peak
        return np.max(drawdown)

    def _sharpe_ratio(self, equity_df):
        """计算夏普比率"""
        returns = equity_df['equity'].pct_change().dropna()
        if len(returns) == 0 or returns.std() == 0:
            return 0
        return np.mean(returns) / np.std(returns) * np.sqrt(252)

    def _sortino_ratio(self, equity_df):
        """计算索提诺比率"""
        returns = equity_df['equity'].pct_change().dropna()
        downside_returns = returns[returns < 0]
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0
        return np.mean(returns) / downside_returns.std() * np.sqrt(252)

    def _calmar_ratio(self, equity_df):
        """计算卡玛比率"""
        annual_return = self._annual_return(equity_df)
        max_drawdown = self._max_drawdown(equity_df)
        return annual_return / max_drawdown if max_drawdown > 0 else 0

    def _win_rate(self):
        """计算胜率"""
        sell_trades = [t for t in self.trades if t.get('action') == 'SELL']
        if not sell_trades:
            return 0
        winning = len([t for t in sell_trades if t.get('pnl', 0) > 0])
        return winning / len(sell_trades)

    def _profit_factor(self):
        """计算盈利因子"""
        profits = sum([t['pnl'] for t in self.trades if t.get('action') == 'SELL' and t.get('pnl', 0) > 0])
        losses = abs(sum([t['pnl'] for t in self.trades if t.get('action') == 'SELL' and t.get('pnl', 0) < 0]))
        return profits / losses if losses > 0 else 0

    def _avg_holding_days(self):
        """计算平均持仓天数"""
        holding_days = []
        entry_date = None
        entry_shares = 0

        for trade in self.trades:
            if trade['action'] == 'BUY':
                entry_date = pd.to_datetime(trade['date'])
                entry_shares = trade['shares']
            elif trade['action'] == 'SELL' and entry_date:
                exit_date = pd.to_datetime(trade['date'])
                days = (exit_date - entry_date).days
                holding_days.append(days)
                entry_date = None

        return np.mean(holding_days) if holding_days else 0

    def _trade_statistics(self):
        """交易统计"""
        sell_trades = [t for t in self.trades if t.get('action') == 'SELL']
        if not sell_trades:
            return {}

        pnls = [t.get('pnl', 0) for t in sell_trades]
        return {
            'total_trades': len(sell_trades),
            'winning_trades': len([p for p in pnls if p > 0]),
            'losing_trades': len([p for p in pnls if p < 0]),
            'avg_profit': np.mean([p for p in pnls if p > 0]) if [p for p in pnls if p > 0] else 0,
            'avg_loss': np.mean([p for p in pnls if p < 0]) if [p for p in pnls if p < 0] else 0,
            'max_profit': max(pnls) if pnls else 0,
            'max_loss': min(pnls) if pnls else 0
        }

    def generate_report(self):
        """生成性能报告"""
        metrics = self.analyze()

        report = f"""
        ========================================
              量化策略性能报告
        ========================================

        收益指标:
        -----------
        总收益率:     {metrics.get('total_return', 0)*100:.2f}%
        年化收益率:   {metrics.get('annual_return', 0)*100:.2f}%

        风险指标:
        -----------
        最大回撤:     {metrics.get('max_drawdown', 0)*100:.2f}%
        夏普比率:     {metrics.get('sharpe_ratio', 0):.2f}
        索提诺比率:   {metrics.get('sortino_ratio', 0):.2f}
        卡玛比率:     {metrics.get('calmar_ratio', 0):.2f}

        交易统计:
        -----------
        总交易次数:   {metrics.get('trade_stats', {}).get('total_trades', 0)}
        胜率:         {metrics.get('win_rate', 0)*100:.2f}%
        盈利因子:     {metrics.get('profit_factor', 0):.2f}
        平均持仓天数: {metrics.get('avg_holding_days', 0):.1f}

        单笔交易:
        -----------
        最大盈利:     {metrics.get('trade_stats', {}).get('max_profit', 0):.2f}
        最大亏损:     {metrics.get('trade_stats', {}).get('max_loss', 0):.2f}
        平均盈利:     {metrics.get('trade_stats', {}).get('avg_profit', 0):.2f}
        平均亏损:     {metrics.get('trade_stats', {}).get('avg_loss', 0):.2f}

        ========================================
        """

        return report
