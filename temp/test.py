import asyncio

# import aiohttp


# async def fetch_url(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return await response.text()

# async def main():
#     urls = ["https://example.com", "https://python.org", "https://google.com", "https://privatbank.ua"]
#     tasks = [fetch_url(url) for url in urls]
#     results = await asyncio.gather(*tasks)
#     for url, content in zip(urls, results):
#         print(f"Fetched {len(content)} bytes from {url}")

# asyncio.run(main())

# ----------------------------------------------------------------
# async def io_operation(task_name, delay):
#     await asyncio.sleep(delay)
#     print(f"Task {task_name} completed")


# async def main():
#     tasks = [
#         io_operation("A", 3),
#         io_operation("B", 1),
#         io_operation("C", 2),
#         io_operation("D", 1)
#     ]
#     await asyncio.gather(*tasks)

# asyncio.run(main())

# ----------------------------------------------------------------
# class MyAwaitable:
#     def __await__(self):
#         yield
#         return 42

# async def main():
#     result = await MyAwaitable()
#     print(result)

# asyncio.run(main())


# ----------------------------------------------------------------
# async def foo():
#     await asyncio.sleep(2)
#     print("Hello from foo!")


# async def bar():
#     await asyncio.sleep(1)
#     print("Hello from bar!")

# async def main():
#     task1 = asyncio.create_task(foo())
#     task2 = asyncio.create_task(bar())
#     await task1
#     await task2

# asyncio.run(main())
# ----------------------------------------------------------------

#!/usr/bin/env python3
# rand.py

# import asyncio
# import random

# # ANSI colors
# c = (
#     "\033[0m",  # End of color
#     "\033[36m",  # Cyan
#     "\033[91m",  # Red
#     "\033[35m",  # Magenta
# )


# async def makerandom(idx: int, threshold: int = 6) -> int:
#     print(c[idx + 1] + f"Initiated makerandom({idx}).")
#     i = random.randint(0, 10)
#     while i <= threshold:
#         print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
#         await asyncio.sleep(idx + 1)
#         i = random.randint(0, 10)
#     print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
#     return i


# async def main():
#     res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
#     return res


# if __name__ == "__main__":
#     random.seed(444)
#     r1, r2, r3 = asyncio.run(main())
#     print()
#     print(f"r1: {r1}, r2: {r2}, r3: {r3}")

# ----------------------------------------------------------------