import praw

reddit = praw.Reddit(client_id="cQ_NXPbSXuCOaQ",
                     client_secret="TdD3Mg3Z4YO5rk1Vdazk2pB8tO-9Og",
                     user_agent="OmeBot",
                     username="Freedom_Pulu",
                     password="mmmmm36")

nsfwSubReddit = reddit.subreddit("nsfw").hot(limit=100)

for submission in nsfwSubReddit:
    print(submission.title, submission.url)