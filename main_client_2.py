"""
This module shows the aiohttp module implementention for Privat Bank API 
"""

import asyncio
import json
import sys

from datetime import datetime, timedelta

import aiohttp


async def get_data(url: dict):
    """
    This function is used to retrieve data from a specific URL.
    Args: url (dict): A dictionary containing the date and URL to retrieve data from.
    Returns: dict: A dictionary containing the date and the currency exchange rates
             for the specified date.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url["url"]) as response:
                if response.status == 200:
                    respond = await response.json()
                    currencies = respond["exchangeRate"]
                    result = {}
                    # цей цикл далі реалізован через enumerate, що більш Python-way, але теж працює
                    # for item in range(len(currencies)):
                    #     if (
                    #             currencies[item]["currency"] == "USD"
                    #             or currencies[item]["currency"] == "EUR"
                    #         ):
                    #             rates = {}
                    #             rates["sale"] = currencies[item]["saleRate"]
                    #             rates["purchase"] = currencies[item]["purchaseRate"]
                    #             result[currencies[item]["currency"]] = rates
                    for i, item in enumerate(currencies):
                        if item["currency"] == "USD" or item["currency"] == "EUR":
                            rates = {}
                            rates["sale"] = currencies[i]["saleRate"]
                            rates["purchase"] = currencies[i]["purchaseRate"]
                            result[currencies[i]["currency"]] = rates
                    return {url["date"]: result}
                print(f"Error status: {response.status} for {url['ukl']}")
        except (aiohttp.ClientConnectionError, aiohttp.InvalidURL) as err:
            print(f"Connection error: {url['ukl']}", str(err))


def url_list(amount: int):
    """
    This function generates a list of URLs.
    Args: amount (int): The number of days to generate URLs for.
    Returns: list: A list of dictionaries, where each dictionary contains
             the date and URL to retrieve data for.
    """
    urls = []
    for i in range(amount):
        shift_days = datetime.today() - timedelta(days=i)
        delta = shift_days.strftime("%d.%m.%Y")
        url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={delta}"
        urls.append({"date": delta, "url": url})
    return urls


async def main(days: int):
    """
    This function is the main function of the script.
    Args: days (int): The number of days to retrieve data for.
    Returns: list: A list of dictionaries, where each dictionary represents a day
              and its currency exchange rates.
    """
    urls = url_list(days)
    tasks = [asyncio.create_task(get_data(item)) for item in urls]
    # tasks = [get_data(item) for item in urls]
    results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    if len(sys.argv) == 2 and int(sys.argv[1]) <= 10:
        DAYS = int(sys.argv[1])
    else:
        DAYS = 1
    r = asyncio.run(main(DAYS))
    print(json.dumps(r, indent=2))
