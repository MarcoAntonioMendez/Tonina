import os
import logging
import subprocess
import customtkinter as ctk
from pathlib import Path

# Constants
BETA_KEYBOARD = "_beta"
RETURN_TO_MAIN_WINDOW_BUTTON_ENABLED_BACKGROUND_COLOR = "#59239a"


class MetadataSetter:
    def __init__(self):
        print()

    def set_metadata(self, 
                    song_title: str,
                    artist_name: str,
                    album_name: str,
                    track_position_in_album: str,
                    song_genre: str,
                    song_year: str,
                    album_cover_image: str,
                    directory_where_song_will_be_saved_to: str,
                    filename: str):
        #Changing to the default download directory
        os.chdir(directory_where_song_will_be_saved_to)

        # Creating command
        command_to_add_metadata = ""

        # Adding the initial part for using ffmpeg
        command_to_add_metadata += "ffmpeg -i "

        # Adding the filename of the downloaded file
        command_to_add_metadata += filename + ".mp3"

        # Adding the album artwork
        command_to_add_metadata += " -i " + album_cover_image + " -map 0:0 -map 1:0 -id3v2_version 3"

        # Adding the title
        command_to_add_metadata += " -metadata title=" + "\"" + song_title + "\""

        # Adding the artist
        command_to_add_metadata += " -metadata album_artist=" + "\"" + artist_name + "\""
        command_to_add_metadata += " -metadata composer=" + "\"" + artist_name + "\""
        command_to_add_metadata += " -metadata artist=" + "\"" + artist_name + "\""

        # Adding the album name
        command_to_add_metadata += " -metadata album=" + "\"" + album_name + "\""

        # Adding the track_number
        command_to_add_metadata += " -metadata track=" + "\"" + track_position_in_album + "\""

        # Adding the genre
        command_to_add_metadata += " -metadata genre=" + "\"" + song_genre + "\""

        # Adding the year
        command_to_add_metadata += " -metadata year=" + "\"" + song_year + "\""

        # Adding the quality and final output filename
        command_to_add_metadata += " -b:a 320k " + filename.replace(BETA_KEYBOARD, "") + ".mp3"

        # Executing the metadata command
        os.system(command_to_add_metadata)

        # Removing leftover files
        os.remove(filename+".mp3")



    def set_metadata_without_beta_word(self, 
                    song_title: str,
                    artist_name: str,
                    album_name: str,
                    track_position_in_album: str,
                    song_genre: str,
                    song_year: str,
                    album_cover_image: str,
                    directory_where_song_will_be_saved_to: str,
                    filename: str):
        #Changing to the default download directory
        os.chdir(directory_where_song_will_be_saved_to)

        # Creating command
        command_to_add_metadata = ""

        # Adding the initial part for using ffmpeg
        command_to_add_metadata += "ffmpeg -i "

        # Adding the filename of the downloaded file
        command_to_add_metadata += filename

        # Adding the album artwork
        command_to_add_metadata += " -i " + album_cover_image + " -map 0:0 -map 1:0 -id3v2_version 3"

        # Adding the title
        command_to_add_metadata += " -metadata title=" + "\"" + song_title + "\""

        # Adding the artist
        command_to_add_metadata += " -metadata album_artist=" + "\"" + artist_name + "\""
        command_to_add_metadata += " -metadata composer=" + "\"" + artist_name + "\""
        command_to_add_metadata += " -metadata artist=" + "\"" + artist_name + "\""

        # Adding the album name
        command_to_add_metadata += " -metadata album=" + "\"" + album_name + "\""

        # Adding the track_number
        command_to_add_metadata += " -metadata track=" + "\"" + track_position_in_album + "\""

        # Adding the genre
        command_to_add_metadata += " -metadata genre=" + "\"" + song_genre + "\""

        # Adding the year
        command_to_add_metadata += " -metadata year=" + "\"" + song_year + "\""

        # Adding the quality and final output filename
        command_to_add_metadata += " -b:a 320k " + "ms_new_" + filename

        # Executing the metadata command
        os.system(command_to_add_metadata)



