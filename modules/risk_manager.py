"""
风险管理模块
"""

import config


class RiskManager:
    """风险管理器"""

    def __init__(self, risk_config=None):
        """
        初始化风险管理器

        Args:
            risk_config: 风险配置字典
        """
        self.config = risk_config or config.RISK_CONFIG
        self.max_position_size = self.config['max_position_size']
        self.max_total_position = self.config['max_total_position']
        self.stop_loss = self.config['stop_loss']
        self.take_profit = self.config['take_profit']

    def check_position_size(self, total_capital, position_value):
        """
        检查仓位是否超过限制

        Args:
            total_capital: 总资金
            position_value: 持仓市值

        Returns:
            tuple: (是否允许, 建议仓位)
        """
        current_ratio = position_value / total_capital if total_capital > 0 else 0

        if current_ratio >= self.max_total_position:
            return False, 0

        allowed_ratio = self.max_total_position - current_ratio
        suggested_value = total_capital * allowed_ratio

        return True, suggested_value

    def check_risk(self, entry_price, current_price, position_value):
        """
        检查单笔交易风险（止损止盈）

        Args:
            entry_price: 入场价格
            current_price: 当前价格
            position_value: 持仓市值

        Returns:
            tuple: (是否触发风控, 原因)
        """
        if entry_price == 0:
            return False, None

        pnl_ratio = (current_price - entry_price) / entry_price

        # 检查止损
        if pnl_ratio <= -self.stop_loss:
            return True, 'stop_loss'

        # 检查止盈
        if pnl_ratio >= self.take_profit:
            return True, 'take_profit'

        return False, None

    def calculate_position_size(self, capital, price, volatility=None):
        """
        根据风险敞口计算仓位

        Args:
            capital: 可用资金
            price: 股价
            volatility: 波动率（可选）

        Returns:
            int: 可买入股数
        """
        if volatility and volatility > 0:
            # 根据波动率调整仓位
            risk_ratio = min(self.stop_loss / volatility, self.max_position_size)
        else:
            risk_ratio = self.max_position_size

        max_investment = capital * risk_ratio
        shares = int(max_investment / price)
        return shares

    def validate_trade(self, trade_info, portfolio):
        """
        验证交易是否合规

        Args:
            trade_info: 交易信息字典
            portfolio: 投资组合对象

        Returns:
            tuple: (是否允许, 错误信息)
        """
        action = trade_info.get('action')
        symbol = trade_info.get('symbol')
        shares = trade_info.get('shares', 0)
        price = trade_info.get('price', 0)

        if action == 'BUY':
            # 检查仓位限制
            allowed, _ = self.check_position_size(
                portfolio.total_capital,
                portfolio.position_value + (shares * price)
            )
            if not allowed:
                return False, '超出最大仓位限制'

        elif action == 'SELL':
            # 检查持仓是否足够
            current_position = portfolio.get_position(symbol)
            if current_position < shares:
                return False, '持仓不足'

        return True, None

    def get_risk_metrics(self, positions, total_capital):
        """
        计算当前风险指标

        Args:
            positions: 持仓列表
            total_capital: 总资金

        Returns:
            dict: 风险指标
        """
        total_exposure = sum([p['market_value'] for p in positions])
        exposure_ratio = total_exposure / total_capital if total_capital > 0 else 0

        return {
            'total_exposure': total_exposure,
            'exposure_ratio': exposure_ratio,
            'cash_ratio': 1 - exposure_ratio,
            'position_count': len(positions),
            'max_position_size': self.max_position_size,
            'max_total_position': self.max_total_position
        }
