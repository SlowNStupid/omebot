import json
import re

import asyncpraw


async def get_pictures_from_subreddit(subreddit):
    result = []
    async for submission in subreddit:
        if submission.url.endswith(".jpg") \
                or submission.url.endswith(".jpeg") \
                or submission.url.endswith(".png") \
                or submission.url.endswith(".webp") \
                or submission.url.endswith(".gif") \
                or submission.url.endswith(".gifv"):
            result.append(submission.url)
    return result


class RedditScraper:
    def __init__(self, token_json: json):
        self.reddit = asyncpraw.Reddit(client_id=token_json["reddit_id"],
                                       client_secret=token_json["reddit_secret"],
                                       user_agent="OmeBot",
                                       username=token_json["reddit_username"],
                                       password=token_json["reddit_password"])

    async def get_nsfw_pics(self):
        nsfw_sub = (await self.reddit.subreddit("nsfw+NSFW_GIF")).hot(limit=500)
        return await get_pictures_from_subreddit(nsfw_sub)

    async def get_food_pics(self):
        food_porn_sub = (await self.reddit.subreddit("FoodPorn")).hot(limit=500)
        return await get_pictures_from_subreddit(food_porn_sub)
