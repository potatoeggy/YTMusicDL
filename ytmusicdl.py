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

for i, song in enumerate(songs[:10], start=1):
    print(f"{i}. {song['title']} - {song['artists'][0]['name']}")

choice = int(input("Select a number: "))
song = songs[choice-1]
video_id: str = song["videoId"]
title: str = song["title"]
album: str = song["album"]["name"]
year: str = song["year"] if song.get("year", "None") != "None" else ""
artists: list[str] = [a["name"] for a in song["artists"]]
art: str = song["thumbnails"][-1]["url"] if song["thumbnails"] else ""

playlist = ytmusic.get_watch_playlist(video_id)
lyric_id = playlist["lyrics"]
try:
    lyrics = ytmusic.get_lyrics(lyric_id)["lyrics"]
except Exception:
    # no lyrics found
    print("No lyrics found")
    lyrics = None

# download video
video = YouTube(f"https://music.youtube.com/watch?v={video_id}")
video.streams.get_audio_only().download()

mp_file = f"{title}.mp3"

# convert video to mp3
try:
    subprocess.run(["ffmpeg", "-i", f"{title}.mp4", mp_file], check=True)
except Exception:
    mp_file = "output.mp3"
#    subprocess.run(["ffmpeg", "-i", f"'{title}.mp4'", mp_file], check=True)


# set metadata
audiofile = eyed3.load(mp_file)
audiofile.tag.title = title
audiofile.tag.artist = ",".join(artists)
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

if lyrics:
    # write lyric file
    with open(f"{new_name}.lrc", "w", encoding="utf-8") as file:
        file.write(lyrics)

# clean up
os.remove(f"{title}.mp4")
