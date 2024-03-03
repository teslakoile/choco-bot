import asyncio
import os
from datetime import datetime, timedelta, timezone

import discord
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True
BUFFER_PERIOD = timedelta(minutes=2)

client = discord.Client(intents=intents)

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube_channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")

youtube = build("youtube", "v3", developerKey=youtube_api_key)


async def check_new_comments(youtube_channel_id, last_check_time):
    channel_response = (
        youtube.channels().list(id=youtube_channel_id, part="contentDetails").execute()
    )
    uploads_playlist_id = channel_response["items"][0]["contentDetails"][
        "relatedPlaylists"
    ]["uploads"]

    new_comments = []
    next_page_token = None

    while True:
        playlist_response = (
            youtube.playlistItems()
            .list(
                playlistId=uploads_playlist_id,
                part="snippet",
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )

        for video in playlist_response["items"]:
            video_id = video["snippet"]["resourceId"]["videoId"]
            video_title = video["snippet"]["title"]
            try:
                comments_response = (
                    youtube.commentThreads()
                    .list(
                        videoId=video_id, part="snippet,replies", textFormat="plainText"
                    )
                    .execute()
                )

                for comment_thread in comments_response["items"]:
                    comment = comment_thread["snippet"]["topLevelComment"]["snippet"]
                    if "publishedAt" in comment:
                        comment_time = datetime.strptime(
                            comment["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                        )
                        last_check_time = last_check_time.replace(tzinfo=timezone.utc)
                        comment_time = comment_time.replace(tzinfo=timezone.utc)
                        if comment_time > last_check_time:
                            new_comments.append(
                                {
                                    "video": video_title,
                                    "author": comment["authorDisplayName"],
                                    "text": comment["textDisplay"],
                                    "time": comment["publishedAt"],
                                    "videoId": video_id,
                                }
                            )
            except HttpError as error:
                if (
                    error.resp.status == 403
                    and "commentsDisabled" in error.content.decode()
                ):
                    print(f"Comments are disabled for the video: {video_id}. Skipping.")
                else:
                    raise

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    return new_comments


discord_user_id = "1202167609613893642"


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.last_check_time = datetime.utcnow() - timedelta(hours=4)
        self.channel_id = discord_channel_id
        self.bg_task = self.loop.create_task(self.schedule_check_comments())

    async def schedule_check_comments(self):
        await self.wait_until_ready()
        while not self.is_closed():
            cycle_start_time = datetime.utcnow()
            effective_last_check_time = self.last_check_time - BUFFER_PERIOD
            channel = self.get_channel(int(self.channel_id))
            new_comments = await check_new_comments(
                youtube_channel_id, effective_last_check_time
            )
            if new_comments:
                comments_count = len(new_comments)
                comments_word = "comment" if comments_count == 1 else "comments"
                last_check_formatted = (
                    self.last_check_time.replace(tzinfo=timezone.utc)
                    .astimezone(timezone(timedelta(hours=8)))
                    .strftime("%b. %d, %I:%M %p")
                )
                formatted_comments = []
                for c in new_comments:
                    parsed_time = datetime.strptime(c["time"], "%Y-%m-%dT%H:%M:%SZ")
                    utc_time = parsed_time.replace(tzinfo=timezone.utc)
                    target_timezone = timezone(timedelta(hours=8))
                    localized_time = utc_time.astimezone(target_timezone)
                    formatted_time = localized_time.strftime("%b. %d, %I:%M %p")
                    comment_str = (
                        f"{c['author']} commented \"{c['text']}\" on your "
                        f"video [{c['video']}](https://www.youtube.com/watch?v={c['videoId']}) "
                        f"at {formatted_time}"
                    )

                    formatted_comments.append(comment_str)
                message = (
                    f"Hi <@{discord_user_id}>! You got {comments_count} "
                    f"new {comments_word} since {last_check_formatted}:\n"
                    + "\n".join(formatted_comments)
                )
                await channel.send(message)
            else:
                last_check_formatted = (
                    self.last_check_time.replace(tzinfo=timezone.utc)
                    .astimezone(timezone(timedelta(hours=8)))
                    .strftime("%b. %d, %I:%M %p")
                )
                await channel.send(f"No new comments since {last_check_formatted}.")
            self.last_check_time = cycle_start_time
            await asyncio.sleep(14400)


client = MyClient(intents=intents)
client.run(discord_bot_token)
