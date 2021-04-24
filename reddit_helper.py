import json
import re

import asyncpraw


class RedditScraper:
    def __init__(self, token_json: json):
        self.reddit = asyncpraw.Reddit(client_id=token_json["reddit_id"],
                                       client_secret=token_json["reddit_secret"],
                                       user_agent="OmeBot",
                                       username=token_json["reddit_username"],
                                       password=token_json["reddit_password"])

    async def get_nsfw_pics(self):
        result = []
        nsfw_sub = (await self.reddit.subreddit("nsfw+NSFW_GIF")).hot(limit=500)
        async for submission in nsfw_sub:
            if submission.url.endswith(".jpg") \
                    or submission.url.endswith(".jpeg") \
                    or submission.url.endswith(".png") \
                    or submission.url.endswith(".webp") \
                    or submission.url.endswith(".gif"):
                result.append(submission.url)
            else:
                match = re.search("redgifs.com/watch/(.+)", submission.url)
                if match is not None:
                    result.append(submission.url)

        return result
