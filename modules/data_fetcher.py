"""
数据获取模块 - 从各种数据源获取股票数据
"""

import baostock as bs
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta


class DataFetcher:
    """数据获取器"""

    def __init__(self, source='baostock'):
        self.source = source
        if source == 'baostock':
            bs.login()

    def __del__(self):
        if self.source == 'baostock':
            bs.logout()

    def get_stock_data(self, code, start_date=None, end_date=None):
        """
        获取股票历史数据

        Args:
            code: 股票代码，如 '600000' (上海) 或 '000001' (深圳)
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'

        Returns:
            DataFrame: 包含日期、开盘价、收盘价、最高价、最低价、成交量等
        """
        if self.source == 'baostock':
            df = self._get_from_baostock(code, start_date, end_date)
            if df is None or df.empty:
                print("baostock获取失败，尝试akshare...")
                return self._get_from_akshare(code, start_date, end_date)
            return df
        else:
            return self._get_from_akshare(code, start_date, end_date)

    def _get_from_baostock(self, code, start_date, end_date):
        """从baostock获取数据"""
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        if code.startswith('6'):
            bs_code = f"sh.{code}"
        else:
            bs_code = f"sz.{code}"

        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency="d"
        )

        data_list = []
        while rs.error_code == '0' and rs.next():
            data_list.append(rs.get_row_data())

        if not data_list:
            print(f"baostock返回空数据: {bs_code}")
            return None

        df = pd.DataFrame(data_list, columns=rs.fields)
        
        try:
            df['open'] = df['open'].astype(float)
            df['high'] = df['high'].astype(float)
            df['low'] = df['low'].astype(float)
            df['close'] = df['close'].astype(float)
            df['volume'] = df['volume'].astype(float)
        except KeyError as e:
            print(f"baostock列名错误: {e}, 可用列: {df.columns.tolist()}")
            return None
        
        return df

    def _get_from_akshare(self, code, start_date, end_date):
        """从akshare获取数据作为备用"""
        try:
            if code.startswith('6'):
                symbol = f"sh{code}"
            else:
                symbol = f"sz{code}"

            df = ak.stock_zh_a_hist(symbol=symbol, start_date=start_date, end_date=end_date)
            df = df.rename(columns={
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount'
            })
            return df
        except Exception as e:
            print(f"akshare获取数据失败: {e}")
            return pd.DataFrame()

    def get_realtime_quote(self, code):
        """获取实时行情"""
        if self.source == 'baostock':
            if code.startswith('6'):
                bs_code = f"sh.{code}"
            else:
                bs_code = f"sz.{code}"
            rs = bs.query_real_time_quotes(bs_code)
            return rs.get_row_data()
        return None