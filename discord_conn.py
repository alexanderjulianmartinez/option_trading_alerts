import os
import discord
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL_ID_1')


class DiscordConnClient(discord.Client):
    async def on_ready(self):
        print(
            f'{self.user} is connected to Discord and scanning for option trading alerts...\n'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return None
        elif 'Call @' in message.content or 'C @' in message.content:
            print(f'Call Option Alert: {message.content}')
        elif 'Put @' in message.content or 'P @' in message.content:
            print(f'Put Option Alert: {message.content}')


def run_discord_client():
    client = DiscordConnClient()
    client.run(DISCORD_TOKEN)


if __name__ == "__main__":
    run_discord_client()
