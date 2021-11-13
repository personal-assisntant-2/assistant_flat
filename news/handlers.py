import aiohttp
import asyncio
import humanize

# client timeout, total number of seconds for the whole request.
TIMEOUT = 7


#  myfin.by ################################################################
async def parse_data_myfin(data):
    """
    Parses the response text (https://myfin.by/crypto-rates/{...})
    """
    rate = data.split('"birzha_info_head_rates">')[1].split('$')[0].strip()

    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_myfin(session, url):
    """
    Makes a request for https://myfin.by/crypto-rates/{...}
    """
    async with session.get(url) as resp:
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_myfin(data)


async def client_myfin(list_url):
    """
    Client aiohttp. The session makes multiple requests to the same server.
    """
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)

    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        # formation of a list of tasks
        requests = [requests_course_myfin(session, url) for url in list_url]
        # run the tasks and get the result
        results = await asyncio.gather(*requests, return_exceptions=True)

    return handler_result(results)


# bitinfocharts.com #########################################################
async def parse_data_bitinfo(data):
    """
    Parses the response text (https://bitinfocharts.com/ru/{...})
    """
    rate = data.split('"price"')[1].split('>')[1].split('<')[0].strip().replace(',', '')

    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_bitinfo(session, url):
    """
    Makes a request for https://bitinfocharts.com/ru/{...}
    """
    async with session.get(url) as resp:
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_bitinfo(data)


async def client_bitinfo(list_url):
    """
    Client aiohttp. The session makes multiple requests to the same server.
    """
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)

    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        # formation of a list of tasks
        requests = [requests_course_bitinfo(session, url) for url in list_url]
        # run the tasks and get the result
        results = await asyncio.gather(*requests, return_exceptions=True)

    return handler_result(results)


# bitstat.top #################################################################
async def parse_data_bitstat(data):
    """
    Parses the response text (https://bitstat.top/coin.php?id_coin={...})
    """
    rate = data.split('"ticker_usd">')[1].split('$')[0].replace(' ', '')

    return humanize.intcomma('%.2f' % float(rate))


async def requests_course_bitstat(session, url):
    """
    Makes a request for https://bitstat.top/coin.php?id_coin={...}
    """
    async with session.get(url) as resp:
        data = await resp.text()
        if resp.status != 200:
            return
        return await parse_data_bitstat(data)


async def client_bitstat(list_url):
    """
    Client aiohttp. The session makes multiple requests to the same server.
    """
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)

    async with aiohttp.ClientSession(timeout=timeout, connector=aiohttp.TCPConnector(limit=64, ssl=False)) as session:
        # formation of a list of tasks
        requests = [requests_course_bitstat(session, url) for url in list_url]
        # run the tasks and get the result
        results = await asyncio.gather(*requests, return_exceptions=True)

    return handler_result(results)


def handler_result(results):
    """
    Iterates over the answers, checks if the answer is of type Exception, then replaces it with "".
    """
    result_no_exception = list()
    for result in results:
        if isinstance(result, Exception):
            result_no_exception.append('')
        else:
            result_no_exception.append(result)
    bitcoin, ethereum, bitcoin_cash = result_no_exception
    return {'bitcoin': bitcoin, 'ethereum': ethereum, 'bitcoin_cash': bitcoin_cash}
