import asyncio
import json
import sys

from datetime import datetime, timedelta

import aiohttp


async def get_data(delta:str):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={delta}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            # print("Status:", response.status)
            # print("Content-type:", response.headers["content-type"])
            # print("Cookies: ", response.cookies)
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
            return {delta:result}


async def main():
    days = 6
    rez=[]
    for i in range(days):
        shift_day = datetime.today() - timedelta(days=i)
        delta = shift_day.strftime("%d.%m.%Y")
        prom_rez = get_data(delta)
        rez.append(prom_rez)
    return await asyncio.gather(*rez)


if __name__ == "__main__":
    r = asyncio.run(main())
    print(json.dumps(r, indent=2))

#     result ={}
#     currencies = r["exchangeRate"]
#     for item in range(len(currencies)):
#         if currencies[item]['currency'] == 'USD' or currencies[item]['currency'] == 'EUR':
#             rates={}
#             rates['sale'] = currencies[item]["saleRate"]
#             rates["purchase"] = currencies[item]["purchaseRate"]
#             result[currencies[item]["currency"]] = rates
#     print(json.dumps(result, indent=4))


# days=3
# for i in range (days):
#     shift_day=datetime.today() - timedelta(days=i)
#     delta=shift_day.strftime("%d.%m.%Y")
#     print(delta)
