#! https://discord.com/api/oauth2/authorize?client_id=835149234122129418&permissions=3406912&scope=bot
import random
import re
import os

import asyncprawcore.exceptions
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

nsfw_pics = []
dong_pics = []
beaver_pics = []
food_pics = []

nsfw_pics_enabled = True
dong_pics_enabled = True
beaver_pics_enabled = True
food_pics_enabled = True


def get_members(message):
    target_users = []
    msg = message.content
    if msg == "ome.sendfood" or msg == "ome.sendnude" or msg == "ome.senddong" or msg == "ome.sendbeaver":
        target_users.append(message.author)
        return target_users

    match = re.search("\\s<@[!&]*(.+)>", msg)
    if match:
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


async def send_picture_in_dm(target_users,
                             author=None,
                             msg_to_others="",
                             msg_to_self="",
                             picture=None,
                             repeat_times=1,
                             is_secret=False,
                             secret_msg=""):
    for target_user in target_users:
        dm_channel = await target_user.create_dm()
        for x in range(repeat_times):
            if target_user == author:
                await dm_channel.send(content=msg_to_self + picture.pop())
            elif is_secret:
                await dm_channel.send(content=secret_msg + picture.pop())
            else:
                await dm_channel.send(content=msg_to_others + author.display_name + "\n" + picture.pop())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("ome"):
        secret_msg = False
        send_times = 1

        global food_pics
        global food_pics_enabled
        try:
            if len(food_pics) < 1:
                food_pics = await reddit_scraper.get_food_pics()
                random.shuffle(food_pics)
                food_pics_enabled = True
        except asyncprawcore.exceptions.Forbidden:
            food_pics_enabled = False
            del food_pics[:]

        global nsfw_pics
        global nsfw_pics_enabled

        try:
            if len(nsfw_pics) < 1:
                nsfw_pics = await reddit_scraper.get_nsfw_pics()
                random.shuffle(nsfw_pics)
                nsfw_pics_enabled = True
        except asyncprawcore.exceptions.Forbidden:
            nsfw_pics_enabled = False
            del nsfw_pics[:]

        global dong_pics
        global dong_pics_enabled

        try:
            if len(dong_pics) < 1:
                dong_pics = await reddit_scraper.get_dong_pics()
                random.shuffle(dong_pics)
                dong_pics_enabled = True
        except asyncprawcore.exceptions.Forbidden:
            dong_pics_enabled = False
            del dong_pics[:]

        global beaver_pics
        global beaver_pics_enabled

        try:
            if len(beaver_pics) < 1:
                beaver_pics = await reddit_scraper.get_beaver_pics()
                random.shuffle(beaver_pics)
                beaver_pics_enabled = True
        except asyncprawcore.exceptions.Forbidden:
            beaver_pics_enabled = False
            del beaver_pics[:]

        msg = message.content

        secret_match = re.search("\\s(?:<@[!&]*.+>\\s)*(secret)", msg.lower())
        number_match = re.search("\\s(\\d)+\\s*", msg.lower())

        if secret_match:
            secret_msg = True
            msg = msg.replace(secret_match.group(1), "").strip()

            await message.delete()

        if number_match:
            msg = msg.replace(number_match.group(0), "").strip()

            if int(number_match.group(0)) <= 44:
                send_times = int(number_match.group(0))
            else:
                send_times = 44

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

            cmd_embed.add_field(name="ome.food *secret*",
                                value="Request bot to post food picture to the channel,"
                                      " optionally include \"secret\" to request anonymously",
                                inline=True)
            cmd_embed.add_field(name="ome.sendfood <mention> *secret*",
                                value="Request bot to send food porn to yourself or to other "
                                      "(mention a person or role after the command), "
                                      "optionally include \"secret\" to send anonymously",
                                inline=True)

            cmd_embed.add_field(name="--------------------------------------------------------------------------------",
                                value="------------------------------------------------------------------------------",
                                inline=False)

            cmd_embed.add_field(name="ome.nsfw *secret*",
                                value="Request bot to post a porn picture to the channel, "
                                      "optionally include \"secret\" to request anonymously",
                                inline=True)
            cmd_embed.add_field(name="ome.sendnude <mention> *secret*",
                                value="Request bot to send a porn picture to yourself or to other "
                                      "(mention a person or role after the command), "
                                      "optionally include \"secret\" to send anonymously",
                                inline=True)

            cmd_embed.add_field(name="--------------------------------------------------------------------------------",
                                value="------------------------------------------------------------------------------",
                                inline=False)

            cmd_embed.add_field(name="ome.dong *secret*",
                                value="Request bot to post a dong picture to the channel, "
                                      "optionally include \"secret\" to request anonymously",
                                inline=True)
            cmd_embed.add_field(name="ome.senddong <mention> *secret*",
                                value="Request bot to send a dong picture to yourself or to other "
                                      "(mention a person or role after the command), "
                                      "optionally include \"secret\" to send anonymously",
                                inline=True)

            cmd_embed.add_field(name="--------------------------------------------------------------------------------",
                                value="------------------------------------------------------------------------------",
                                inline=False)

            cmd_embed.add_field(name="ome.beaver *secret*",
                                value="Request bot to post a beaver picture to the channel, "
                                      "optionally include \"secret\" to request anonymously",
                                inline=True)
            cmd_embed.add_field(name="ome.sendbeaver <mention> *secret*",
                                value="Request bot to send a beaver picture to yourself or to other "
                                      "(mention a person or role after the command), "
                                      "optionally include \"secret\" to send anonymously",
                                inline=True)

            await message.channel.send(embed=cmd_embed)
        elif msg == "ome.clean":
            all_msg = await message.channel.history(limit=None).flatten()
            filtered_msg = [i for i in all_msg if i.author == client.user
                            or i.content.startswith("ome.")
                            or i.content == "ome"]
            for cur_msg in filtered_msg:
                if type(message.channel) == discord.DMChannel:
                    if cur_msg.author == client.user:
                        await cur_msg.delete()
                else:
                    await cur_msg.delete()
        elif msg.startswith("ome.sendfood"):
            if not food_pics_enabled:
                await message.channel.send(content="Food pics are not enabled (most likely "
                                                   "acquiring pictures is not possible atm)")
                return

            target_users = []
            if msg == "ome.sendfood":
                target_users.append(message.author)
            else:
                target_users = get_members(message)

            if secret_msg:
                await send_picture_in_dm(target_users, picture=food_pics, repeat_times=send_times,
                                         is_secret=True, secret_msg="Food courtesy of your secret admirer =P\n")
            else:
                await send_picture_in_dm(target_users, message.author, "Food courtesy of ",
                                         "Food courtesy of yourself??? Get a job, you lazy ass...\n", food_pics,
                                         repeat_times=send_times)
        elif msg == "ome.food":
            if not food_pics_enabled:
                await message.channel.send(content="Food pics are not enabled (most likely "
                                                   "acquiring pictures is not possible atm)")
                return

            for x in range(send_times):
                await message.channel.send(content=food_pics.pop())
        elif message.channel.is_nsfw():
            if msg.startswith("ome.sendnude"):
                if not nsfw_pics_enabled:
                    await message.channel.send(content="Nude pics are not enabled (most likely "
                                                       "acquiring pictures is not possible atm)")
                    return

                target_users = []
                if msg == "ome.sendnude":
                    target_users.append(message.author)
                else:
                    target_users = get_members(message)
                if secret_msg:
                    await send_picture_in_dm(target_users, picture=nsfw_pics, repeat_times=send_times,
                                             is_secret=True, secret_msg="Nude courtesy of your secret admirer =P\n")
                else:
                    await send_picture_in_dm(target_users, message.author, "Nude courtesy of ",
                                             "Nude courtesy of yourself??? You need some help...\n", nsfw_pics,
                                             repeat_times=send_times)
            elif msg == "ome.nsfw":
                if not nsfw_pics_enabled:
                    await message.channel.send(content="NSFW pics are not enabled (most likely "
                                                       "acquiring pictures is not possible atm)")
                    return

                for x in range(send_times):
                    await message.channel.send(content=nsfw_pics.pop())
            elif msg.startswith("ome.senddong"):
                if not dong_pics_enabled:
                    await message.channel.send(content="Dong pics are not enabled (most likely "
                                                       "acquiring pictures is not possible atm)")
                    return

                target_users = []
                if msg == "ome.senddong":
                    target_users.append(message.author)
                else:
                    target_users = get_members(message)
                if secret_msg:
                    await send_picture_in_dm(target_users, picture=dong_pics, repeat_times=send_times,
                                             is_secret=True, secret_msg="Dong courtesy of your secret admirer =P\n")
                else:
                    await send_picture_in_dm(target_users, message.author, "Nude courtesy of ",
                                             "Dong courtesy of yourself??? You need some help...\n", dong_pics,
                                             repeat_times=send_times)
            elif msg == "ome.dong":
                if not dong_pics_enabled:
                    await message.channel.send(content="Dong pics are not enabled (most likely "
                                                       "acquiring pictures is not possible atm)")
                    return

                for x in range(send_times):
                    await message.channel.send(content=dong_pics.pop())
            elif msg.startswith("ome.sendbeaver"):
                if not dong_pics_enabled:
                    await message.channel.send(content="Beaver pics are not enabled (most likely "
                                                       "acquiring pictures is not possible atm)")
                    return

                target_users = []
                if msg == "ome.sendbeaver":
                    target_users.append(message.author)
                else:
                    target_users = get_members(message)
                if secret_msg:
                    await send_picture_in_dm(target_users, picture=beaver_pics, repeat_times=send_times,
                                             is_secret=True, secret_msg="Beaver courtesy of your secret admirer =P\n")
                else:
                    await send_picture_in_dm(target_users, message.author, "Nude courtesy of ",
                                             "Beaver courtesy of yourself??? You need some help...\n", beaver_pics,
                                             repeat_times=send_times)
            elif msg == "ome.beaver":
                if not beaver_pics_enabled:
                    await message.channel.send(content="Beaver pics are not enabled (most likely "
                                                       "acquiring pictures is not possible atm)")
                    return

                for x in range(send_times):
                    await message.channel.send(content=beaver_pics.pop())

            if type(message.channel) == discord.TextChannel and not secret_msg:
                if message.author.id not in freq_users:
                    freq_users[message.author.id] = 1
                else:
                    freq_users[message.author.id] = freq_users[message.author.id] + 1

                if random.randint(1, 100) >= 95 and not secret_msg:
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
                            content=message.author.mention + ", I see you're a pervert ;)")
        elif not message.channel.is_nsfw():
            await message.channel.send(content="This commands needs to be run from NSFW channel")
            return


if __name__ == "__main__":
    if discord_bot_token is not None:
        client.run(discord_bot_token)
