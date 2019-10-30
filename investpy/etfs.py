#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import datetime
import json
from random import randint
import logging

import pandas as pd
import pkg_resources
import requests
import unidecode
from lxml.html import fromstring

from investpy.utils import user_agent
from investpy.utils.Data import Data

from investpy.data.etfs_data import etfs_as_df, etfs_as_list, etfs_as_dict
from investpy.data.etfs_data import etf_countries_as_list


def get_etfs(country=None):
    """
    This function retrieves all the available countries to retrieve etfs from, as the listed
    countries are the ones indexed on Investing.com. The purpose of this function is to list
    the countries which have available etfs according to Investing.com data, so to ease the
    etf retrieval process of a particular country.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`pandas.DataFrame` - etfs:
            The resulting :obj:`pandas.DataFrame` contains all the etfs basic information stored on `etfs.csv`, since it
            was previously retrieved in `investpy.etfs.retrieve_etfs()`. Unless the country is specified, all the
            available etfs indexed on Investing.com is returned, but if it is specified, just the etfs from that country
            are returned.

            In the case that the file reading of `etfs.csv` or the retrieval process from Investing.com was
            successfully completed, the resulting :obj:`pandas.DataFrame` will look like::

                country | name | symbol | tag | id | currency
                --------|------|--------|-----|----|----------
                xxxxxxx | xxxx | xxxxxx | xxx | xx | xxxxxxxx

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing.
    """

    return etfs_as_df(country=country)


def get_etfs_list(country=None):
    """
    This function retrieves all the available etfs indexed on Investing.com, already
    stored on `etfs.csv`, which if does not exists, will be created by `investpy.etfs.retrieve_etfs()`.
    This function also allows the users to specify which country do they want to retrieve data from or if they
    want to retrieve it from every listed country; so on, a listing of etfs will be returned. This function
    helps the user to get to know which etfs are available on Investing.com.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.

    Returns:
        :obj:`list` - etfs_list:
            The resulting :obj:`list` contains the retrieved data from the `etfs.csv` file, which is
            a listing of the names of the etfs listed on Investing.com, which is the input for data
            retrieval functions as the name of the etf to retrieve data from needs to be specified.

            In case the listing was successfully retrieved, the :obj:`list` will look like::

                etfs_list = ['Betashares U.S. Equities Strong Bear Currency Hedg',
                            'Betashares Active Australian Hybrids',
                            'Australian High Interest Cash', ...]

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing or empty.
    
    """

    return etfs_as_list(country=country)


def get_etfs_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available etfs indexed on Investing.com, already
    stored on `etfs.csv`, which if does not exists, will be created by `investpy.etfs.retrieve_etfs()`.
    This function also allows the user to specify which country do they want to retrieve data from,
    or from every listed country; the columns which the user wants to be included on the resulting
    :obj:`dict`; and the output of the function (:obj:`dict` or :obj:`json`).

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available etfs from.
        columns (:obj:`list`, optional):
            names of the columns of the etf data to retrieve <country, country_code, id, name, symbol, tag>
        as_json (:obj:`bool`, optional):
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - etfs_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                {
                    'country': country,
                    'id': id,
                    'tag': tag,
                    'name': name,
                    'symbol': symbol,
                    'currency': currency
                }

    Raises:
        ValueError: raised when any of the input arguments is not valid.
        IOError: raised when `etfs.csv` file is missing or empty.
    
    """

    return etfs_as_dict(country=country, columns=columns, as_json=as_json)


def get_etf_countries():
    """
    This function retrieves all the available countries to retrieve etfs from, as the listed
    countries are the ones indexed on Investing.com. The purpose of this function is to list
    the countries which have available etfs according to Investing.com data, so to ease the
    etf retrieval process of a particular country.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the countries listed on Investing.com with
            etfs available to retrieve data from.

            In the case that the file reading of `etf_countries.csv` which contains the names and codes of the countries
            with etfs was successfully completed, the resulting :obj:`list` will look like::

                countries = ['australia', 'austria', 'belgium', 'brazil', ...]

    Raises:
        FileNotFoundError: raised when `etf_countries.csv` file is missing.
    
    """

    return etf_countries_as_list()


def get_etf_recent_data(etf, country, as_json=False, order='ascending', debug=False):
    """
    This function retrieves recent historical data from the introduced `etf` from Investing
    via Web Scraping. The resulting data can it either be stored in a :obj:`pandas.DataFrame` or in a
    :obj:`json` file, with `ascending` or `descending` order.

    Args:
        etf (:obj:`str`): name of the etf to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the etf is.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified etf via argument. The dataset contains the open, high, low and close
            values for the selected etf on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | currency
                -----||--------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    recent: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: etfs object/file not found or unable to retrieve.
        RuntimeError: introduced etf does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if etf information was unavailable or not found.

    Examples:
        >>> investpy.get_etf_recent_data(etf='bbva accion dj eurostoxx 50', country='spain', as_json=False, order='ascending', debug=False)
                          Open    High     Low   Close Currency
            Date
            2019-08-13  33.115  33.780  32.985  33.585      EUR
            2019-08-14  33.335  33.335  32.880  32.905      EUR
            2019-08-15  32.790  32.925  32.455  32.845      EUR
            2019-08-16  33.115  33.200  33.115  33.305      EUR
            2019-08-19  33.605  33.735  33.490  33.685      EUR

    """

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_etf_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    etfs = etfs[etfs['country'] == unidecode.unidecode(country.lower())]

    etf = etf.strip()
    etf = etf.lower()

    if unidecode.unidecode(etf) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + etf + " not found, check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('investpy')

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced etf on Investing.com')

    symbol = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'symbol']
    id_ = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'id']
    name = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'name']

    etf_currency = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'currency']

    logger.info(str(etf) + ' found on Investing.com')

    header = "Datos históricos " + symbol

    params = {
        "curr_id": id_,
        "smlID": str(randint(1000000, 99999999)),
        "header": header,
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action": "historical_data"
    }

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    url = "https://es.investing.com/instruments/HistoricalDataAjax"

    logger.info('Request sent to Investing.com!')

    req = requests.post(url, headers=head, data=params)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
    result = list()

    if path_:
        logger.info('Data parsing process starting...')

        for elements_ in path_:
            info = []
            for nested_ in elements_.xpath(".//td"):
                info.append(nested_.text_content())

            if info[0] == 'No se encontraron resultados':
                raise IndexError("ERR#0010: etf information unavailable or not found.")

            etf_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
            etf_close = float(info[1].replace('.', '').replace(',', '.'))
            etf_open = float(info[2].replace('.', '').replace(',', '.'))
            etf_high = float(info[3].replace('.', '').replace(',', '.'))
            etf_low = float(info[4].replace('.', '').replace(',', '.'))

            result.insert(len(result), Data(etf_date, etf_open, etf_high, etf_low, etf_close, None, etf_currency))

        if order in ['ascending', 'asc']:
            result = result[::-1]
        elif order in ['descending', 'desc']:
            result = result

        logger.info('Data parsing process finished...')

        if as_json is True:
            json_ = {'name': name,
                     'recent':
                         [value.etf_as_json() for value in result]
                     }

            return json.dumps(json_, sort_keys=False)
        elif as_json is False:
            df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
            df.set_index('Date', inplace=True)

            return df

    else:
        raise RuntimeError("ERR#0004: data retrieval error while scraping.")


def get_etf_historical_data(etf, country, from_date, to_date, as_json=False, order='ascending', debug=False):
    """
    This function retrieves historical data from the introduced `etf` from Investing
    via Web Scraping on the introduced date range. The resulting data can it either be
    stored in a :obj:`pandas.DataFrame` or in a :obj:`json` object with `ascending` or `descending` order.

    Args:
        etf (:obj:`str`): name of the etf to retrieve recent historical data from.
        country (:obj:`str`): name of the country from where the etf is.
        from_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, from where data is going to be retrieved.
        to_date (:obj:`str`): date as `str` formatted as `dd/mm/yyyy`, until where data is going to be retrieved.
        as_json (:obj:`bool`, optional):
            to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).
        order (:obj:`str`, optional):
            optional argument to define the order of the retrieved data (`ascending`, `asc` or `descending`, `desc`).
        debug (:obj:`bool`, optional):
            optional argument to either show or hide debug messages on log, `True` or `False`, respectively.

    Returns:
        :obj:`pandas.DataFrame` or :obj:`json`:
            The function returns either a :obj:`pandas.DataFrame` or a :obj:`json` file containing the retrieved
            recent data from the specified etf via argument. The dataset contains the open, high, low and close
            values for the selected etf on market days.

            The returned data is case we use default arguments will look like::

                date || open | high | low | close | currency
                -----||--------------------------------------
                xxxx || xxxx | xxxx | xxx | xxxxx | xxxxxxxx

            but if we define `as_json=True`, then the output will be::

                {
                    name: name,
                    historical: [
                        {
                            date: dd/mm/yyyy,
                            open: x,
                            high: x,
                            low: x,
                            close: x,
                            currency: x
                        },
                        ...
                    ]
                }

    Raises:
        ValueError: argument error.
        IOError: etfs object/file not found or unable to retrieve.
        RuntimeError: introduced etf does not match any of the indexed ones.
        ConnectionError: if GET requests does not return 200 status code.
        IndexError: if etf information was unavailable or not found.

    Examples:
        >>> investpy.get_etf_historical_data(etf='bbva accion dj eurostoxx 50', country='spain', from_date='01/01/2010', to_date='01/01/2019', as_json=False, order='ascending', debug=False)
                         Open   High    Low  Close Currency
            Date
            2011-12-07  23.70  23.70  23.70  23.62      EUR
            2011-12-08  23.53  23.60  23.15  23.04      EUR
            2011-12-09  23.36  23.60  23.36  23.62      EUR
            2011-12-12  23.15  23.26  23.00  22.88      EUR
            2011-12-13  22.88  22.88  22.88  22.80      EUR

    """

    if not etf:
        raise ValueError("ERR#0031: etf parameter is mandatory and must be a valid etf name.")

    if not isinstance(etf, str):
        raise ValueError("ERR#0030: etf argument needs to be a str.")

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    if order not in ['ascending', 'asc', 'descending', 'desc']:
        raise ValueError("ERR#0003: order argument can just be ascending (asc) or descending (desc), str type.")

    if not isinstance(debug, bool):
        raise ValueError("ERR#0033: debug argument can just be a boolean value, either True or False.")

    try:
        datetime.datetime.strptime(from_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    try:
        datetime.datetime.strptime(to_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("ERR#0011: incorrect data format, it should be 'dd/mm/yyyy'.")

    start_date = datetime.datetime.strptime(from_date, '%d/%m/%Y')
    end_date = datetime.datetime.strptime(to_date, '%d/%m/%Y')

    if start_date >= end_date:
        raise ValueError("ERR#0032: to_date should be greater than from_date, both formatted as 'dd/mm/yyyy'.")

    date_interval = {
        'intervals': [],
    }

    flag = True

    while flag is True:
        diff = end_date.year - start_date.year

        if diff > 20:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': start_date.replace(year=start_date.year + 20).strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            start_date = start_date.replace(year=start_date.year + 20)
        else:
            obj = {
                'start': start_date.strftime('%d/%m/%Y'),
                'end': end_date.strftime('%d/%m/%Y'),
            }

            date_interval['intervals'].append(obj)

            flag = False

    interval_limit = len(date_interval['intervals'])
    interval_counter = 0

    data_flag = False

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    if unidecode.unidecode(country.lower()) not in get_etf_countries():
        raise RuntimeError("ERR#0034: country " + country.lower() + " not found, check if it is correct.")

    etfs = etfs[etfs['country'] == unidecode.unidecode(country.lower())]

    etf = etf.strip()
    etf = etf.lower()

    if unidecode.unidecode(etf) not in [unidecode.unidecode(value.lower()) for value in etfs['name'].tolist()]:
        raise RuntimeError("ERR#0019: etf " + str(etf) + " not found in " + str(country.lower()) + ", check if it is correct.")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('investpy')

    if debug is False:
        logger.disabled = True
    else:
        logger.disabled = False

    logger.info('Searching introduced etf on Investing.com')

    symbol = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'symbol']
    id_ = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'id']
    name = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'name']

    etf_currency = etfs.loc[(etfs['name'].str.lower() == etf).idxmax(), 'currency']

    logger.info(str(etf) + ' found on Investing.com')

    final = list()

    header = "Datos históricos " + symbol

    for index in range(len(date_interval['intervals'])):
        interval_counter += 1

        params = {
            "curr_id": id_,
            "smlID": str(randint(1000000, 99999999)),
            "header": header,
            "st_date": date_interval['intervals'][index]['start'],
            "end_date": date_interval['intervals'][index]['end'],
            "interval_sec": "Daily",
            "sort_col": "date",
            "sort_ord": "DESC",
            "action": "historical_data"
        }

        head = {
            "User-Agent": user_agent.get_random(),
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "text/html",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

        url = "https://es.investing.com/instruments/HistoricalDataAjax"

        logger.info('Request sent to Investing.com!')

        req = requests.post(url, headers=head, data=params)

        if req.status_code != 200:
            raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

        logger.info('Request to Investing.com data succeeded with code ' + str(req.status_code) + '!')

        if not req.text:
            continue

        root_ = fromstring(req.text)
        path_ = root_.xpath(".//table[@id='curr_table']/tbody/tr")
        result = list()

        if path_:
            logger.info('Data parsing process starting...')

            for elements_ in path_:
                info = []

                for nested_ in elements_.xpath(".//td"):
                    info.append(nested_.text_content())

                if info[0] == 'No se encontraron resultados':
                    if interval_counter < interval_limit:
                        data_flag = False
                    else:
                        raise IndexError("ERR#0010: etf information unavailable or not found.")
                else:
                    data_flag = True

                if data_flag is True:
                    etf_date = datetime.datetime.strptime(info[0].replace('.', '-'), '%d-%m-%Y')
                    etf_close = float(info[1].replace('.', '').replace(',', '.'))
                    etf_open = float(info[2].replace('.', '').replace(',', '.'))
                    etf_high = float(info[3].replace('.', '').replace(',', '.'))
                    etf_low = float(info[4].replace('.', '').replace(',', '.'))

                    result.insert(len(result),
                                  Data(etf_date, etf_open, etf_high, etf_low, etf_close, None, etf_currency))

            if data_flag is True:
                if order in ['ascending', 'asc']:
                    result = result[::-1]
                elif order in ['descending', 'desc']:
                    result = result

                if as_json is True:
                    json_ = {'name': name,
                             'historical':
                                 [value.etf_as_json() for value in result]
                             }

                    final.append(json_)
                elif as_json is False:
                    df = pd.DataFrame.from_records([value.etf_to_dict() for value in result])
                    df.set_index('Date', inplace=True)

                    final.append(df)

        else:
            raise RuntimeError("ERR#0004: data retrieval error while scraping.")

    logger.info('Data parsing process finished...')

    if as_json is True:
        return json.dumps(final[0], sort_keys=False)
    elif as_json is False:
        return pd.concat(final)


def get_etfs_overview(country, as_json=False):
    """
    This function retrieves an overview containing all the real time data available for the main ETFs from a country,
    such as the ETF names, symbols, current value, etc. as indexed in Investing.com. So on, the main usage of this
    function is to get an overview on the main ETFs from a country, so to get a general view.

    Args:
        country (:obj:`str`): name of the country to retrieve the ETFs overview from.
        as_json (:obj:`bool`, optional):
            optional argument to determine the format of the output data (:obj:`pandas.DataFrame` or :obj:`json`).

    Returns:
        :obj:`pandas.DataFrame` - etfs_overview:
            The resulting :obj:`pandas.DataFrame` contains all the data available in Investing.com of the main ETFs
            from a country in order to get an overview of it.

            If the retrieval process succeeded, the resulting :obj:`pandas.DataFrame` should look like::

                country | name | full_name | symbol | last | change | turnover
                --------|------|-----------|--------|------|--------|----------
                xxxxxxx | xxxx | xxxxxxxxx | xxxxxx | xxxx | xxxxxx | xxxxxxxx
    
    Raises:
        ValueError: raised if there was any argument error.
        FileNotFoundError:  raised when `etf_countries.csv` file is missing.
        RuntimeError: raised it the introduced country does not match any of the indexed ones.
        ConnectionError: raised if GET requests does not return 200 status code.
    
    """

    if country is None:
        raise ValueError("ERR#0039: country can not be None, it should be a str.")

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    head = {
        "User-Agent": user_agent.get_random(),
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    if unidecode.unidecode(country.lower()) not in get_etf_countries():
        raise RuntimeError('ERR#0025: specified country value not valid.')

    if country.lower() == 'united states':
        country= 'usa'
    elif country.lower() == 'united kingdom':
        country = 'uk'

    url = "https://www.investing.com/etfs/world-etfs?&issuer_filter=0"

    req = requests.get(url, headers=head)

    if req.status_code != 200:
        raise ConnectionError("ERR#0015: error " + str(req.status_code) + ", try again later.")

    root_ = fromstring(req.text)
    path_ = root_.xpath(".//section[@id='leftColumn']/h3")

    results = list()

    if path_:
        for element_ in path_:
            link = element_.xpath(".//a")[0].get("href")
            link = link.replace('/etfs/', '').replace('-etfs', '')
            
            if link == unidecode.unidecode(country.lower()):
                flag = False

                while flag is False:
                    element_ = element_.getnext()
                    if element_.tag == 'table':
                        flag = True

                table = element_.xpath(".//tbody/tr")

                for row in table:
                    id_ = row.get('id').replace('pair_', '')
                    symbol = row.xpath(".//td[contains(@class, 'symbol')]")[0].get('title')

                    nested = row.xpath(".//a")[0]
                    name = nested.text.strip()
                    full_name = nested.get('title').rstrip()

                    # In Euro Zone the ETFs are from different countries so the country is specified
                    country_flag = row.xpath(".//td[@class='flag']/span")[0].get('title')
                    country_flag = unidecode.unidecode(country_flag.lower())

                    last_path = ".//td[@class='" + 'pid-' + str(id_) + '-last' + "']"
                    last = row.xpath(last_path)[0].text_content()

                    change_path = ".//td[contains(@class, '" + 'pid-' + str(id_) + '-pcp' + "')]"
                    change = row.xpath(change_path)[0].text_content()

                    turnover_path = ".//td[contains(@class, '" + 'pid-' + str(id_) + '-turnover' + "')]"
                    turnover = row.xpath(turnover_path)[0].text_content()

                    if turnover == '':
                        continue

                    if turnover.__contains__('K'):
                        turnover = int(float(turnover.replace('K', '').replace('.', '').replace(',', '.')) * 1000)
                    elif turnover.__contains__('M'):
                        turnover = int(float(turnover.replace('M', '').replace('.', '').replace(',', '.')) * 1000000)
                    else:
                        turnover = int(float(turnover.replace('.', '').replace(',', '.')))

                    data = {
                        "country": country_flag,
                        "name": name,
                        "full_name": full_name,
                        "symbol": symbol,
                        "last": float(last.replace('.', '').replace(',', '.')),
                        "change": change,
                        "turnover": turnover,
                    }

                    results.append(data)

                break

    df = pd.DataFrame(results)

    if as_json:
        return df.to_json(orient='records')
    else:
        return df


def search_etfs(by, value):
    """
    This function searches etfs by the introduced value for the specified field. This means that this function
    is going to search if there is a value that matches the introduced value for the specified field which is the
    `etfs.csv` column name to search in. Available fields to search etfs are 'name' and 'symbol'.

    Args:
        by (:obj:`str`): name of the field to search for, which is the column name ('name' or 'symbol').
        value (:obj:`str`): value of the field to search for, which is the str that is going to be searched.

    Returns:
        :obj:`pandas.DataFrame` - search_result:
            The resulting `pandas.DataFrame` contains the search results from the given query (the specified value
            in the specified field). If there are no results and error will be raised, but otherwise this
            `pandas.DataFrame` will contain all the available field values that match the introduced query.

    Raises:
        ValueError: raised if any of the introduced params is not valid or errored.
        IOError: raised if data could not be retrieved due to file error.
        RuntimeError: raised if no results were found for the introduced value in the introduced field.
    
    """

    available_search_fields = ['name', 'symbol']

    if not by:
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if not isinstance(by, str):
        raise ValueError('ERR#0006: the introduced field to search is mandatory and should be a str.')

    if isinstance(by, str) and by not in available_search_fields:
        raise ValueError('ERR#0026: the introduced field to search can either just be '
                         + ' or '.join(available_search_fields))

    if not value:
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    if not isinstance(value, str):
        raise ValueError('ERR#0017: the introduced value to search is mandatory and should be a str.')

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'etfs', 'etfs.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        etfs = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0058: etfs file not found or errored.")

    if etfs is None:
        raise IOError("ERR#0009: etfs object not found or unable to retrieve.")

    etfs['matches'] = etfs[by].str.contains(value, case=False)

    search_result = etfs.loc[etfs['matches'] == True].copy()

    if len(search_result) == 0:
        raise RuntimeError('ERR#0043: no results were found for the introduced ' + str(by) + '.')

    search_result.drop(columns=['tag', 'id', 'matches'], inplace=True)
    search_result.reset_index(drop=True, inplace=True)

    return search_result
