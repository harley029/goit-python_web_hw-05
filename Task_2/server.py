import asyncio
import logging
import websockets

import names
import aiohttp

from datetime import datetime, timedelta
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if "exchange" in message.lower():
                exchange = Exchange(message)
                message = await exchange.rates()
            await self.send_to_clients(f"{ws.name}: {message}")

class Exchange:
    def __init__(self,message:str):
        self.message = message

    async def url_list(self, amount: int):
        urls = []
        for i in range(amount):
            shift_days = datetime.today() - timedelta(days=i)
            delta = shift_days.strftime("%d.%m.%Y")
            url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={delta}"
            urls.append({"date": delta, "url": url})
        return urls

    async def parse_days(self, days:str) -> int:
        amount = days.split(' ')
        if len(amount) == 1:
            return 1
        return int(amount[1])

    async def get_data(self,url: dict):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url["url"]) as response:
                    if response.status == 200:
                        respond = await response.json()
                        currencies = respond["exchangeRate"]
                        result = {}
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

    async def output(self,results:list) -> str:
        result = ""
        for item in results:
            key = list(item.keys())
            result += f"{key[0]}: "
            result += f"EUR: sale - {item[key[0]]['EUR']['sale']}, purchase - {item[key[0]]['EUR']['purchase']};  "
            result += f"USD: sale - {item[key[0]]['USD']['sale']}, purchase - {item[key[0]]['USD']['purchase']};  "
        logging.info(result)
        return result

    async def rates(self) -> str:
        days = await self.parse_days(self.message)
        urls = await self.url_list(days)
        tasks = [asyncio.create_task(self.get_data(item)) for item in urls]
        results = await asyncio.gather(*tasks)
        return await self.output(results)

async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
