#! https://discord.com/api/oauth2/authorize?client_id=835149234122129418&permissions=3406912&scope=bot
import json
import random
import re

import discord
import asyncpraw

token_json = None
client = discord.Client()
nsfw_pics = []


@client.event
async def on_ready():
    reddit = asyncpraw.Reddit(client_id=token_json["reddit_id"],
                         client_secret=token_json["reddit_secret"],
                         user_agent="OmeBot",
                         username=token_json["reddit_username"],
                         password=token_json["reddit_password"])
    nsfw_sub = (await reddit.subreddit("nsfw")).hot(limit=500)
    async for submission in nsfw_sub:
        if submission.url.endswith(".jpg") \
                or submission.url.endswith(".jpeg") \
                or submission.url.endswith(".png") \
                or submission.url.endswith(".webp")\
                or submission.url.endswith(".gif"):
            nsfw_pics.append(submission.url)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("ome"):
        msg = message.content
        if msg == "ome":
            await message.channel.send("Olen Omena!")
        elif msg.startswith("ome.help"):
            await message.channel.send("Commands:\n"
                                       "    ome.clean\n"
                                       "    ome.sendnude\n"
                                       "    ome.nsfw\n")
        elif msg == "ome.clean":
            async for cur_msg in message.channel.history(limit=200):
                if cur_msg.author == client.user \
                        or cur_msg.content.startswith("ome.")\
                        or cur_msg.content == "ome":
                    await cur_msg.delete()
        elif msg.startswith("ome.sendnude") and message.channel.is_nsfw():
            sel_pic = random.randint(0, len(nsfw_pics) - 1)
            embed_msg = discord.Embed()
            embed_msg.set_image(url=nsfw_pics[sel_pic])

            match = re.search("ome.sendnude(.+)", msg)
            if match is None:
                dm_channel = await message.author.create_dm()
            else:
                user_id = match.group(1)[4:][:-1]
                target_user = await message.guild.fetch_member(user_id)
                dm_channel = await target_user.create_dm()

            await dm_channel.send(embed=embed_msg)
            del nsfw_pics[sel_pic]
        elif msg == "ome.nsfw" and message.channel.is_nsfw():
            sel_pic = random.randint(0, len(nsfw_pics) - 1)
            embed_msg = discord.Embed()
            embed_msg.set_image(url=nsfw_pics[sel_pic])

            await message.channel.send(embed=embed_msg)
            del nsfw_pics[sel_pic]


if __name__ == "__main__":
    token_json = json.load(open("tokens.txt"))
    client.run(token_json["discord_bot_token"])
