import csv
import random
import asyncio

from telethon.tl.functions.channels import InviteToChannelRequest


async def add_members(client, target_group):

    with open("members.csv") as f:

        reader = csv.reader(f)

        for row in reader:

            username = row[0]

            try:

                user = await client.get_entity(username)

                await client(
                    InviteToChannelRequest(
                        target_group,
                        [user]
                    )
                )

                delay = random.randint(30, 90)

                print(f"Added {username} | waiting {delay}s")

                await asyncio.sleep(delay)

            except Exception as e:

                print("Error:", e)
