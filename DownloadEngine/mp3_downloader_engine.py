import yt_dlp
import os
import logging
import customtkinter as ctk
from pathlib import Path

# Constants
BETA_KEYBOARD = "_beta"
RETURN_TO_MAIN_WINDOW_BUTTON_ENABLED_BACKGROUND_COLOR = "#59239a"


class Mp3DownloaderEngine:
    def __init__(self):
        print()

    def download_song(self, song_title: str, artist_name: str, album_name: str,\
                    track_position_in_album: str, song_genre: str, youtube_url: str,\
                    album_cover_image: str, return_to_main_window_button,\
                    progress_bar, download_status_label):
        self.__song_title = song_title
        self.__artist_name = artist_name
        self.__album_name = album_name
        self.__track_position_in_album = track_position_in_album
        self.__song_genre = song_genre
        self.__youtube_url = youtube_url
        self.__album_cover_image = album_cover_image
        self.__return_to_main_window_button = return_to_main_window_button
        self.__progress_bar = progress_bar
        self.__download_status_label = download_status_label


        #--------------------- Making the actual download ------------------------------
        logging.warning("Starting to download: " + self.__song_title)
        self.__progress_bar.step()

        # Setting the filename
        safe_song_title_for_filename = self.clear_string_from_forbidden_chars_for_file_names(self.__song_title)
        safe_artist_name_for_file_name = self.clear_string_from_forbidden_chars_for_file_names(self.__artist_name)
        filename = safe_song_title_for_filename + "_" + safe_artist_name_for_file_name + BETA_KEYBOARD

        #Changing to the default download directory
        os.chdir(str(Path.home())+"/Downloads")
        self.__progress_bar.step()
        self.__download_status_label.configure(text="Extrayendo audio...")

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
        self.__progress_bar.step()
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(self.__youtube_url)

        logging.warning("The raw download of: " + self.__song_title + " has been finished (Metadata has not been set yet).")
        self.__progress_bar.step()

        # Now that the raw download of the song has finished, it's time to set the metadata.
        logging.warning("Setting up the metadata for: " + filename)


        # Creating command
        command_to_add_metadata = ""
        self.__progress_bar.step()

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
        self.__progress_bar.step()


        # Executing the metadata command
        self.__download_status_label.configure(text="Estableciendo metadata...")
        os.system(command_to_add_metadata)
        self.__progress_bar.step()

        # Removing leftover files
        os.remove(filename+".mp3")
        self.__progress_bar.step()
        self.__download_status_label.configure(\
            text="DESCARGA FINALIZADA! El Archivo ha sido guardado en la carpeta de descargas :D.")


        # Enabling the return to the main window button
        self.__return_to_main_window_button.configure(state=ctk.NORMAL,\
            fg_color=RETURN_TO_MAIN_WINDOW_BUTTON_ENABLED_BACKGROUND_COLOR)


    def clear_string_from_forbidden_chars_for_file_names(self, string_to_clean):
        forbidden_chars = ['<','>',':','"','/','|','?','*',"'",' ','(',')']
        clean_string = string_to_clean
        for char in forbidden_chars:
            clean_string = clean_string.replace(char, "_")
        return clean_string
