#!/usr/bin/python3

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import unidecode
import json

import pandas as pd
import pkg_resources


def stocks_as_df(country=None):
    """
    This function retrieves all the stock data stored in `stocks.csv` file, which previously was
    retrieved from Investing.com. Since the resulting object is a matrix of data, the stock data is properly
    structured in rows and columns, where columns are the stock data attribute names. Additionally, country
    filtering can be specified, which will make this function return not all the stored stock data, but just
    the stock data of the stocks from the introduced country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`pandas.DataFrame` - stocks_df:
            The resulting :obj:`pandas.DataFrame` contains all the stock data from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            So on, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | full name | isin | currency | symbol
                --------|------|-----------|------|----------|--------
                xxxxxxx | xxxx | xxxxxxxxx | xxxx | xxxxxxxx | xxxxxx

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if stocks file was not found.
        IOError: raised when stocks file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks list not found or unable to retrieve.")

    stocks.drop(columns=['tag', 'id'], inplace=True)

    if country is None:
        stocks.reset_index(drop=True, inplace=True)
        return stocks
    elif unidecode.unidecode(country.lower()) in stock_countries_as_list():
        stocks = stocks[stocks['country'] == unidecode.unidecode(country.lower())]
        stocks.reset_index(drop=True, inplace=True)
        return stocks


def stocks_as_list(country=None):
    """
    This function retrieves all the stock symbols stored in `stocks.csv` file, which contains all the
    data from the stocks as previously retrieved from Investing.com. So on, this function will just return
    the stock symbols which will be one of the input parameters when it comes to stock data retrieval functions
    from investpy. Additionally, note that the country filtering can be applied, which is really useful since
    this function just returns the symbols and in stock data retrieval functions both the symbol and the country
    must be specified and they must match.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.

    Returns:
        :obj:`list` - stocks_list:
            The resulting :obj:`list` contains the all the stock symbols from the introduced country if specified,
            or from every country if None was specified, as indexed in Investing.com from the information previously
            retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of stock symbols will look like::

                stocks_list = ['TS', 'APBR', 'GGAL', 'TXAR', 'PAMP', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if stocks file was not found.
        IOError: raised when stocks file is missing or empty.
    
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks list not found or unable to retrieve.")

    stocks.drop(columns=['tag', 'id'], inplace=True)

    if country is None:
        return stocks['symbol'].tolist()
    elif unidecode.unidecode(country.lower()) in stock_countries_as_list():
        return stocks[stocks['country'] == unidecode.unidecode(country.lower())]['symbol'].tolist()


def stocks_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the stock information stored in the `stocks.csv` file and formats it as a
    Python dictionary which contains the same information as the file, but every row is a :obj:`dict` and
    all of them are contained in a :obj:`list`. Note that the dictionary structure is the same one as the
    JSON structure. Some optional paramaters can be specified such as the country, columns or as_json, which
    are a filtering by country so not to return all the stocks but just the ones from the introduced country,
    the column names that want to be retrieved in case of needing just some columns to avoid unnecessary information
    load, and whether the information wants to be returned as a JSON object or as a dictionary; respectively.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available stocks from.
        columns (:obj:`list`, optional):column names of the stock data to retrieve, can be: <country, name, full_name, isin, currency, symbol>
        as_json (:obj:`bool`, optional): if True the returned data will be a :obj:`json` object, if False, a :obj:`list` of :obj:`dict`.

    Returns:
        :obj:`list` of :obj:`dict` OR :obj:`json` - stocks_dict:
            The resulting :obj:`list` of :obj:`dict` contains the retrieved data from every stock as indexed in Investing.com from
            the information previously retrieved by investpy and stored on a csv file.

            In case the information was successfully retrieved, the :obj:`list` of :obj:`dict` will look like::

                stocks_dict = {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'tag': tag,
                    'isin': isin,
                    'id': id,
                    'currency': currency,
                    'symbol': symbol,
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
        FileNotFoundError: raised if stocks file was not found.
        IOError: raised when stocks file is missing or empty.

    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stocks.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        stocks = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0056: stocks file not found or errored.")

    if stocks is None:
        raise IOError("ERR#0001: stocks list not found or unable to retrieve.")

    stocks.drop(columns=['tag', 'id'], inplace=True)

    if columns is None:
        columns = stocks.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in stocks.columns.tolist() for column in columns):
        raise ValueError("ERR#0021: specified columns does not exist, available columns are "
                         "<country, name, full_name, tag, isin, id, symbol, currency>")

    if country is None:
        if as_json:
            return json.dumps(stocks[columns].to_dict(orient='records'))
        else:
            return stocks[columns].to_dict(orient='records')
    elif country in stock_countries_as_list():
        if as_json:
            return json.dumps(
                stocks[stocks['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records'))
        else:
            return stocks[stocks['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records')


def stock_countries_as_list():
    """
    This function returns a listing with all the available countries from where stocks can be retrieved, so to
    let the user know which of them are available, since the parameter country is mandatory in every stock retrieval
    function. Also, not just the available countries, but the required name is provided since Investing.com has a
    certain country name standard and countries should be specified the same way they are in Investing.com.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with stocks as indexed in Investing.com

    Raises:
        FileNotFoundError: raised if stock countries file was not found.
        IOError: raised when stock countries file is missing or empty.

    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'stocks', 'stock_countries.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        countries = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0071: stock countries file not found or errored.")

    if countries is None:
        raise IOError("ERR#0036: stock countries list not found or unable to retrieve.")
    else:
        return countries['country'].tolist()
