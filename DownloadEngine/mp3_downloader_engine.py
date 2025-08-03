import yt_dlp
import os
import logging
from pathlib import Path

# Constants
BETA_KEYBOARD = "_beta"


class Mp3DownloaderEngine:
    def __init__(self):
        print()

    def download_song(self, song_title: str, artist_name: str, album_name: str,\
                    track_position_in_album: str, song_genre: str, youtube_url: str,\
                    album_cover_image: str):
        self.__song_title = song_title
        self.__artist_name = artist_name
        self.__album_name = album_name
        self.__track_position_in_album = track_position_in_album
        self.__song_genre = song_genre
        self.__youtube_url = youtube_url
        self.__album_cover_image = album_cover_image


        #--------------------- Making the actual download ------------------------------
        logging.warning("Starting to download: " + self.__song_title)

        # Setting the filename
        safe_song_title_for_filename = self.clear_string_from_forbidden_chars_for_file_names(self.__song_title)
        safe_artist_name_for_file_name = self.clear_string_from_forbidden_chars_for_file_names(self.__artist_name)
        filename = safe_song_title_for_filename + "_" + safe_artist_name_for_file_name + BETA_KEYBOARD

        #Changing to the default download directory
        os.chdir(str(Path.home())+"/Downloads")

        # Setting up YoutubeDLP options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'outtmpl': filename,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(self.__youtube_url)

        logging.warning("The raw download of: " + self.__song_title + " has been finished (Metadata has not been set yet).")

        # Now that the raw download of the song has finished, it's time to set the metadata.
        logging.warning("Setting up the metadata for: " + filename)


        # Creating command
        command_to_add_metadata = ""

        # Adding the initial part for using ffmpeg
        command_to_add_metadata += "ffmpeg -i "

        # Adding the filename of the downloaded file
        command_to_add_metadata += filename + ".mp3"

        # Adding the album artwork
        command_to_add_metadata += " -i " + self.__album_cover_image + " -map 0:0 -map 1:0 -id3v2_version 3"

        # Adding the title
        command_to_add_metadata += " -metadata title=" + "\"" + self.__song_title + "\""

        # Adding the artist
        command_to_add_metadata += " -metadata album_artist=" + "\"" + self.__artist_name + "\""
        command_to_add_metadata += " -metadata composer=" + "\"" + self.__artist_name + "\""
        command_to_add_metadata += " -metadata artist=" + "\"" + self.__artist_name + "\""

        # Adding the album name
        command_to_add_metadata += " -metadata album=" + "\"" + self.__album_name + "\""

        # Adding the track_number
        command_to_add_metadata += " -metadata track=" + "\"" + self.__track_position_in_album + "\""

        # Adding the genre
        command_to_add_metadata += " -metadata genre=" + "\"" + self.__song_genre + "\""

        # Adding the quality and final output filename
        command_to_add_metadata += " -b:a 320k " + filename.replace(BETA_KEYBOARD, "") + ".mp3"


        # Executing the metadata command
        os.system(command_to_add_metadata)

        # Removing leftover files
        os.remove(filename+".mp3")


    def clear_string_from_forbidden_chars_for_file_names(self, string_to_clean):
        forbidden_chars = ['<','>',':','"','/','|','?','*',' ']
        clean_string = string_to_clean
        for char in forbidden_chars:
            clean_string = clean_string.replace(char, "_")
        return clean_string
