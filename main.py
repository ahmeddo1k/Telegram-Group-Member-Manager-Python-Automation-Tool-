import asyncio

from telethon import TelegramClient

import config
import scraper
import adder


async def main():

    async with TelegramClient("session", config.API_ID, config.API_HASH) as client:

        print("1 - Scrape Members")
        print("2 - Add Members")

        choice = input("Select: ")

        if choice == "1":

            await scraper.scrape_members(client, config.SOURCE_GROUP)

        elif choice == "2":

            await adder.add_members(client, config.TARGET_GROUP)


asyncio.run(main())
