#! https://discord.com/api/oauth2/authorize?client_id=835149234122129418&permissions=3406912&scope=bot
import random
import re
import os

import discord
import reddit_helper

from dotenv import load_dotenv
load_dotenv()

discord_bot_token = os.getenv("discord_bot_token")
reddit_id = os.getenv("reddit_id")
reddit_secret = os.getenv("reddit_secret")
reddit_username = os.getenv("reddit_username")
reddit_password = os.getenv("reddit_password")

if reddit_id is not None \
        and reddit_secret is not None \
        and reddit_username is not None \
        and reddit_password is not None:
    reddit_scraper = reddit_helper.RedditScraper(reddit_id, reddit_secret, reddit_username, reddit_password)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

freq_users = {}
food_pics = []
nsfw_pics = []


def get_members(message):
    target_users = []
    msg = message.content
    match = re.search("\\s<@.(.+)>", msg)
    if msg == "ome.sendfood" or msg == "ome.sendnude":
        target_users.append(message.author)
    if match is not None:
        mention_id = int(match.group(1))
        target_user = message.guild.get_member(mention_id)
        if target_user is not None:
            target_users.append(target_user)
        else:
            target_role = message.guild.get_role(mention_id)
            if target_role is not None:
                for target_user in target_role.members:
                    target_users.append(target_user)
    return target_users


async def send_picture_in_dm(target_users, author, message_to_others, message_to_self, picture):
    for target_user in target_users:
        dm_channel = await target_user.create_dm()
        if target_user == author:
            await dm_channel.send(content=message_to_self + picture.pop())
        else:
            await dm_channel.send(content=message_to_others + author.display_name + "\n" + picture.pop())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("ome"):
        global nsfw_pics
        if len(nsfw_pics) < 1:
            nsfw_pics = await reddit_scraper.get_nsfw_pics()
            random.shuffle(nsfw_pics)

        global food_pics
        if len(food_pics) < 1:
            food_pics = await reddit_scraper.get_food_pics()
            random.shuffle(food_pics)

        msg = message.content
        if msg == "ome":
            await message.channel.send("Olen Omena!")
        elif msg.startswith("ome.help"):
            cmd_embed = discord.Embed()
            cmd_embed.description = "Commands:"
            cmd_embed.add_field(name="ome.clean",
                                value="Delete message bot has sent and also commands used to call bot "
                                      "(if have permission) from the last 500 messages",
                                inline=False)

            cmd_embed.add_field(name="--------------------------------------------------------------------------------",
                                value="------------------------------------------------------------------------------",
                                inline=False)

            cmd_embed.add_field(name="ome.food",
                                value="Request bot to post food picture to the channel",
                                inline=True)
            cmd_embed.add_field(name="ome.sendfood <mention>",
                                value="Request bot to send food porn to yourself or to other "
                                      "(mention a person or role after the command)",
                                inline=True)

            cmd_embed.add_field(name="--------------------------------------------------------------------------------",
                                value="------------------------------------------------------------------------------",
                                inline=False)

            cmd_embed.add_field(name="ome.nsfw",
                                value="Request bot to post porn picture to the channel",
                                inline=True)
            cmd_embed.add_field(name="ome.sendnude <mention>",
                                value="Request bot to send porn to yourself or to other "
                                      "(mention a person or role after the command)",
                                inline=True)
            await message.channel.send(embed=cmd_embed)
        elif msg == "ome.clean":
            async for cur_msg in message.channel.history(limit=500):
                if cur_msg.author == client.user \
                        or cur_msg.content.startswith("ome.") \
                        or cur_msg.content == "ome":
                    if type(message.channel) == discord.DMChannel:
                        if cur_msg.author == client.user:
                            await cur_msg.delete()
                    else:
                        await cur_msg.delete()
        elif msg.startswith("ome.sendfood"):
            target_users = []
            if msg == "ome.sendfood":
                target_users.append(message.author)
            else:
                target_users = get_members(message)
            await send_picture_in_dm(target_users,
                                     message.author,
                                     "Food courtesy of ",
                                     "Food courtesy of yourself??? Get a job, you lazy ass...\n",
                                     food_pics)
        elif msg == "ome.food":
            await message.channel.send(content=food_pics.pop())
        elif message.channel.is_nsfw():
            if msg.startswith("ome.sendnude"):
                target_users = []
                if msg == "ome.sendnude":
                    target_users.append(message.author)
                else:
                    target_users = get_members(message)
                    await send_picture_in_dm(target_users,
                                         message.author,
                                         "Nude courtesy of ",
                                         "Nude courtesy of yourself??? You need some help...\n",
                                         nsfw_pics)
            elif msg == "ome.nsfw":
                await message.channel.send(content=nsfw_pics.pop())

            if type(message.channel) == discord.TextChannel:
                if message.author.id not in freq_users:
                    freq_users[message.author.id] = 1
                else:
                    freq_users[message.author.id] = freq_users[message.author.id] + 1

                if random.randint(1, 10 + 1) >= 8:
                    if freq_users[message.author.id] > 100:
                        await message.channel.send(
                            content=message.author.mention + "...You need help...")
                    elif freq_users[message.author.id] > 75:
                        await message.channel.send(
                            content=message.author.mention + ", please just stop...")
                    elif freq_users[message.author.id] > 50:
                        await message.channel.send(
                            content=message.author.mention + ", stop requesting me to post nudes! I'm tired of "
                                                             "hunting down those nudes!")
                    elif freq_users[message.author.id] > 25:
                        await message.channel.send(
                            content=message.author.mention + ", you know that pornhub exists, right?")
                    elif freq_users[message.author.id] > 10:
                        await message.channel.send(
                            content=message.author.mention + ", I see you're a pervert,"
                                                             " requesting nudes over 10 times ;)")


if __name__ == "__main__":
    if discord_bot_token is not None:
        client.run(discord_bot_token)