#! https://discord.com/api/oauth2/authorize?client_id=835149234122129418&permissions=3406912&scope=bot
import json
import random
import re

import discord

import reddit_helper

token_json = json.load(open("tokens.txt"))
reddit_scraper = reddit_helper.RedditScraper(token_json)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

freq_users = {}
nsfw_pics = []


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("ome"):
        global nsfw_pics
        if len(nsfw_pics) < 1:
            nsfw_pics = await reddit_scraper.get_nsfw_pics()
            random.shuffle(nsfw_pics)

        msg = message.content
        if msg == "ome":
            await message.channel.send("Olen Omena!")
        elif msg.startswith("ome.help"):
            await message.channel.send("Commands:\n"
                                       "    ome.clean\n"
                                       "    ome.sendnude\n"
                                       "    ome.nsfw\n")
        elif msg == "ome.clean":
            message_list = []
            async for cur_msg in message.channel.history(limit=200):
                if cur_msg.author == client.user \
                        or cur_msg.content.startswith("ome.") \
                        or cur_msg.content == "ome":
                    if type(message.channel) == discord.DMChannel:
                        if cur_msg.author == client.user:
                            await cur_msg.delete()
                    else:
                        message_list.append(cur_msg)

            if len(message_list) > 0:
                await message.channel.delete_messages(message_list)
        elif message.channel.is_nsfw():
            if msg.startswith("ome.sendnude"):
                match = re.search("ome.sendnude\\s<@.(.+)>", msg)
                if msg == "ome.sendnude":
                    dm_channel = await message.author.create_dm()
                    await dm_channel.send(
                        content="Nude courtesy of yourself??? You need help...\n" + nsfw_pics.pop())
                    # await message.delete()
                elif match is not None:
                    mention_id = int(match.group(1))
                    target_user = message.guild.get_member(mention_id)
                    if target_user is not None:
                        dm_channel = await target_user.create_dm()
                        await dm_channel.send(
                            content="Nude courtesy of " + message.author.display_name + "\n" + nsfw_pics.pop())
                    else:
                        target_role = message.guild.get_role(mention_id)
                        if target_role is not None:
                            for cur_member in target_role.members:
                                dm_channel = await cur_member.create_dm()
                                await dm_channel.send(
                                    content="Nude courtesy of " + message.author.display_name + "\n" + nsfw_pics.pop())
                    # await message.delete()
            elif msg == "ome.nsfw":
                await message.channel.send(content=nsfw_pics.pop())

            if type(message.channel) == discord.TextChannel:
                if message.author.id not in freq_users:
                    freq_users[message.author.id] = 1
                else:
                    freq_users[message.author.id] = freq_users[message.author.id] + 1

                if random.randint(1, 10 + 1) >= 6:
                    if freq_users[message.author.id] > 100:
                        await message.channel.send(
                            content=message.author.mention + "... You need a help...")
                    elif freq_users[message.author.id] > 50:
                        await message.channel.send(
                            content=message.author.mention + ", I see you're a real pervert,"
                                                             " requesting nudes over 50 times ;)")
                    elif freq_users[message.author.id] > 10:
                        await message.channel.send(
                            content=message.author.mention + ", I see you're a pervert,"
                                                             " requesting nudes over 10 times ;)")


if __name__ == "__main__":
    client.run(token_json["discord_bot_token"])
