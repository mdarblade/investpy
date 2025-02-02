#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.


class Data(object):
    """
    This class is used to store the historical data of avery financial product retrieved from Investing.com either as
    a :obj:`json` or as a :obj:`dict`.

    Args:
        date_ (:obj:`str`): date in dd/mm/yyyy format.
        open_ (:obj:`float`): open value of the market on the introduced date.
        high_ (:obj:`float`): highest value of the market on the introduced date.
        low_ (:obj:`float`): lowest value of the market on the introduced date.
        close_ (:obj:`float`): close value of the market on the introduced date.
        volume_ (:obj:`long`): number of shares traded on the introduced date.
        currency_ (:obj:`str`): currency in which the data is displayed.

    Attributes:
        date_ (:obj:`str`): date in dd/mm/yyyy format.
        open_ (:obj:`float`): open value of the market on the introduced date.
        high_ (:obj:`float`): highest value of the market on the introduced date.
        low_ (:obj:`float`): lowest value of the market on the introduced date.
        close_ (:obj:`float`): close value of the market on the introduced date.
        volume_ (:obj:`long`): number of shares traded on the introduced date.
        currency_ (:obj:`str`): currency in which the data is displayed.
    
    """

    def __init__(self, date_, open_, high_, low_, close_, volume_, currency_):
        self.date = date_
        self.open = open_
        self.high = high_
        self.low = low_
        self.close = close_
        self.volume = volume_
        self.currency = currency_

    def stock_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
            'Currency': self.currency,
        }

    def stock_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'currency': self.currency,
        }

    def fund_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Currency': self.currency,
        }

    def fund_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'currency': self.currency,
        }

    def etf_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Currency': self.currency,
        }

    def etf_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'currency': self.currency,
        }

    def index_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Volume': self.volume,
            'Currency': self.currency,
        }

    def index_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
            'currency': self.currency,
        }

    def currency_cross_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'Currency': self.currency,
        }

    def currency_cross_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Currency': self.currency,
        }

    def bond_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
        }

    def bond_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }

    def commodity_to_dict(self):
        return {
            'Date': self.date,
            'Open': self.open,
            'High': self.high,
            'Low': self.low,
            'Close': self.close,
            'Currency': self.currency
        }

    def commodity_as_json(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'currency': self.currency
        }

    def unknown_to_dict(self):
        if self.volume is None:
            return {
                'Date': self.date,
                'Open': self.open,
                'High': self.high,
                'Low': self.low,
                'Close': self.close,
            }
        else:
            return {
                'Date': self.date,
                'Open': self.open,
                'High': self.high,
                'Low': self.low,
                'Close': self.close,
                'Volume': self.volume
            }

    def unknown_as_json(self):
        if self.volume is None:
            return {
                'date': self.date.strftime('%d/%m/%Y'),
                'open': self.open,
                'high': self.high,
                'low': self.low,
                'close': self.close,
            }
        else:
            return {
                'date': self.date.strftime('%d/%m/%Y'),
                'open': self.open,
                'high': self.high,
                'low': self.low,
                'close': self.close,
                'volume': self.volume
            }