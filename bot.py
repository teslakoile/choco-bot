import asyncio
import os
from datetime import datetime, timedelta

import discord
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from icecream import ic

intents = discord.Intents.default()

intents.messages = True
intents.message_content = True

client = discord.Client(intents=intents)

load_dotenv()
discord_bot_token = os.getenv("DISCORD_BOT_TOKEN")

youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube_channel_id = os.getenv("YOUTUBE_CHANNEL_ID")
discord_channel_id = os.getenv("DISCORD_CHANNEL_ID")

youtube = build("youtube", "v3", developerKey=youtube_api_key)
# channel_response = youtube.channels().list(id=channel_id, part='contentDetails').execute()
# # ic(channel_response)
# uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
# # ic(uploads_playlist_id)
# playlist_response = youtube.playlistItems().list(playlistId=uploads_playlist_id,
# part='snippet', maxResults=5).execute()
# # ic(playlist_response)
# comments_response = youtube.commentThreads().list(videoId="iLHmCy2EhQI", part='snippet,
# replies', textFormat='plainText').execute()
# ic(comments_response)


async def check_new_comments(youtube_channel_id, last_check_time):
    # Fetch the upload playlist ID of the channel
    channel_response = (
        youtube.channels().list(id=youtube_channel_id, part="contentDetails").execute()
    )
    uploads_playlist_id = channel_response["items"][0]["contentDetails"][
        "relatedPlaylists"
    ]["uploads"]

    # Fetch recent videos from the upload playlist
    playlist_response = (
        youtube.playlistItems()
        .list(playlistId=uploads_playlist_id, part="snippet", maxResults=5)
        .execute()
    )

    new_comments = []
    for video in playlist_response["items"]:
        video_id = video["snippet"]["resourceId"]["videoId"]
        video_title = video["snippet"]["title"]
        # Fetch comments for each video
        try:

            comments_response = (
                youtube.commentThreads()
                .list(videoId=video_id, part="snippet,replies", textFormat="plainText")
                .execute()
            )

            for comment_thread in comments_response["items"]:
                comment = comment_thread["snippet"]["topLevelComment"]["snippet"]
                comment_time = datetime.strptime(
                    comment["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if comment_time > last_check_time:
                    new_comments.append(
                        {
                            "video": video_title,
                            "author": comment["authorDisplayName"],
                            "text": comment["textDisplay"],
                            "time": comment["publishedAt"],
                        }
                    )
                    # Check for replies
                    if "replies" in comment_thread:
                        for reply in comment_thread["replies"]["comments"]:
                            reply_time = datetime.strptime(
                                reply["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
                            )
                            if reply_time > last_check_time:
                                new_comments.append(
                                    {
                                        "video": video_title,
                                        "author": reply["authorDisplayName"],
                                        "text": reply["textDisplay"],
                                        "time": reply["publishedAt"],
                                    }
                                )
        except HttpError as error:
            # Check if the error is due to disabled comments
            if (
                error.resp.status == 403
                and "commentsDisabled" in error.content.decode()
            ):
                print(f"Comments are disabled for the video: {video_id}. Skipping.")
            else:
                # If the error is due to another issue, re-raise the exception
                raise

    return new_comments


# ic(check_new_comments(youtube_channel_id, datetime(2021, 8, 1, 0, 0, 0)))


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.last_check_time = datetime.utcnow() - timedelta(hours=1)
        self.channel_id = discord_channel_id

        # Schedule the check for new comments
        self.bg_task = self.loop.create_task(self.schedule_check_comments())

    async def schedule_check_comments(self):
        await self.wait_until_ready()
        while not self.is_closed():
            channel = self.get_channel(int(self.channel_id))
            ic(channel)
            new_comments = await check_new_comments(
                youtube_channel_id, self.last_check_time
            )
            ic(new_comments)
            if new_comments:
                message = "New comments:\n" + "\n".join(
                    [
                        f"Comment on YouTube video: \"{c['video']}\"\nby user: \" \
                            {c['author']}\"\n\"{c['text']}\"\nat time {c['time']}."
                        for c in new_comments
                    ]
                )
                await channel.send(message)
                ic(message)
            else:
                try:
                    await channel.send("No new comments.")
                except Exception as e:
                    print(f"An error occurred while sending a message: {e}")
            self.last_check_time = datetime.utcnow()
            ic(self.last_check_time)
            await asyncio.sleep(3600)  # Wait for 1 hour


client = MyClient(intents=intents)
client.run(discord_bot_token)
