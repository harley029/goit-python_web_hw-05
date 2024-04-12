import asyncio
import json
import sys

from datetime import datetime, timedelta

import aiohttp


async def get_data(session, delta: str):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={delta}"
    async with session.get(url) as response:
        # print("Status:", response.status)
        # print("Content-type:", response.headers["content-type"])
        # print(response.ok)
        respond = await response.json()
        currencies = respond["exchangeRate"]
        result = {}
        for item in range(len(currencies)):
            if (
                currencies[item]["currency"] == "USD"
                or currencies[item]["currency"] == "EUR"
            ):
                rates = {}
                rates["sale"] = currencies[item]["saleRate"]
                rates["purchase"] = currencies[item]["purchaseRate"]
                result[currencies[item]["currency"]] = rates
        return {delta: result}


async def main():
    days = 1
    rez = []
    async with aiohttp.ClientSession() as session:
        for i in range(days):
            shift_day = datetime.today() - timedelta(days=i)
            delta = shift_day.strftime("%d.%m.%Y")
            prom_rez = await get_data(session, delta)
            rez.append(prom_rez)
        return rez


if __name__ == "__main__":
    r = asyncio.run(main())
    print(json.dumps(r, indent=2))
