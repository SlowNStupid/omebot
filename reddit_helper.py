import json

import asyncpraw


async def get_nsfw_pics(token_json: json):
    result = []
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
                or submission.url.endswith(".webp") \
                or submission.url.endswith(".gif"):
            result.append(submission.url)

    return result
