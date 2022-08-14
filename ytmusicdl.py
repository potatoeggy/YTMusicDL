import imghdr
import io
import os
import subprocess
from ytmusicapi import YTMusic
from pytube import YouTube
import eyed3
from eyed3.id3.tag import TagTemplate
from eyed3.id3.frames import ImageFrame
import requests

ytmusic = YTMusic()

# typer? who needs typer when you have input()?
query = input("Query: ")
# getting ID doesn't get you any metadata so searching it is

songs = [i for i in ytmusic.search(query) if i["resultType"] == "song"]
# TODO: let user pick song

song = songs[0]
video_id: str = song["videoId"]
title: str = song["title"]
album: str = song["album"]["name"]
year: str = song["year"] if song["year"] != "None" else ""
artists: list[str] = [a["name"] for a in song["artists"]]
art: str = song["thumbnails"][-1]["url"] if song["thumbnails"] else ""

playlist = ytmusic.get_watch_playlist(video_id)
lyric_id = playlist["lyrics"]
lyrics = ytmusic.get_lyrics(lyric_id)["lyrics"]

# download video
video = YouTube(f"https://music.youtube.com/watch?v={video_id}")
video.streams.get_audio_only().download()

# convert video to mp3
subprocess.run(["ffmpeg", "-i", f"{title}.mp4", f"{title}.mp3"], check=True)


# set metadata
audiofile = eyed3.load(f"{title}.mp3")
audiofile.tag.title = title
audiofile.tag.artist = "/".join(artists)
audiofile.tag.album = album
audiofile.tag.year = year

# set cover
image_data = requests.get(art).content
with io.BytesIO(image_data) as byte_data:
    mimetype = f"image/{imghdr.what(byte_data)}"
audiofile.tag.images.set(ImageFrame.FRONT_COVER, image_data, mimetype)

# write metadata and rename file
new_name = TagTemplate(
    '$title - $artist').substitute(audiofile.tag, zeropad=True)
audiofile.tag.save()
audiofile.rename(new_name)

# write lyric file
with open(f"{new_name}.lrc", "w", encoding="utf-8") as file:
    file.write(lyrics)

# clean up
os.remove(f"{title}.mp4")
