#! https://discord.com/api/oauth2/authorize?client_id=835149234122129418&permissions=3406912&scope=bot
import json
import random
import re

import discord

import reddit_helper

token_json = json.load(open("tokens.txt"))

intents = discord.Intents.default()
intents.typing = True
client = discord.Client(intents=intents)

channel_used = []
nsfw_pics = []


@client.event
async def on_typing(channel, user, when):
    if channel in channel_used \
            and channel.is_nsfw():
        chance_to_tease = random.randint(1, 10 + 1)
        if chance_to_tease <= 1:
            await channel.send(content="<@!" + user.mention + ", I see you're a pervert ;)")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if type(message.channel) == discord.TextChannel \
            and message.channel not in channel_used:
        channel_used.append(message.channel)

    if message.content.startswith("ome"):
        global nsfw_pics
        if len(nsfw_pics) < 1:
            nsfw_pics = await reddit_helper.get_nsfw_pics(token_json)

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
        else:
            sel_pic = random.randint(0, len(nsfw_pics) - 1)
            embed_msg = discord.Embed()
            embed_msg.set_image(url=nsfw_pics[sel_pic])

            if msg.startswith("ome.sendnude"):
                embed_msg.title = "Nude courtesy of " + message.author.display_name

                match = re.search("ome.sendnude(.+)", msg)
                if match is None:
                    dm_channel = await message.author.create_dm()
                else:
                    user_id = match.group(1)[4:][:-1]
                    target_user = await message.guild.fetch_member(user_id)
                    dm_channel = await target_user.create_dm()

                await dm_channel.send(embed=embed_msg)
            elif msg == "ome.nsfw" and message.channel.is_nsfw():
                await message.channel.send(embed=embed_msg)

            del nsfw_pics[sel_pic]


if __name__ == "__main__":
    client.run(token_json["discord_bot_token"])
