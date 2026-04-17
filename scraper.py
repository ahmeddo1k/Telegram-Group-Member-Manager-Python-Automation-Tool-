import csv
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


async def scrape_members(client, group):

    members = []

    participants = await client(
        GetParticipantsRequest(
            group,
            ChannelParticipantsSearch(""),
            0,
            1000,
            hash=0
        )
    )

    for user in participants.users:

        if user.username:
            members.append(user.username)

    with open("members.csv", "w", newline="") as f:

        writer = csv.writer(f)

        for m in members:
            writer.writerow([m])

    print(f"Saved {len(members)} members")
