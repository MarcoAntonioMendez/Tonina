import yt_dlp
import os
import logging
import customtkinter as ctk
from pathlib import Path
from DownloadEngine import metadata_setter

# Constants
BETA_KEYBOARD = "_beta"
RETURN_TO_MAIN_WINDOW_BUTTON_ENABLED_BACKGROUND_COLOR = "#59239a"


class Mp3DownloaderEngine:
    def __init__(self):
        self.__metadata_setter = metadata_setter.MetadataSetter()

    def download_song(self, song_title: str,
                    artist_name: str,
                    album_name: str,
                    track_position_in_album: str,
                    song_genre: str,
                    song_year: str,
                    youtube_url: str,
                    album_cover_image: str,
                    return_to_main_window_button: ctk.windows.widgets.ctk_button.CTkButton,
                    progress_bar: ctk.windows.widgets.ctk_progressbar.CTkProgressBar,
                    download_status_label: ctk.windows.widgets.ctk_label.CTkLabel,
                    directory_where_song_will_be_saved_to: str):
        self.__song_title = song_title
        self.__artist_name = artist_name
        self.__album_name = album_name
        self.__track_position_in_album = track_position_in_album
        self.__song_genre = song_genre
        self.__song_year = song_year
        self.__youtube_url = youtube_url
        self.__album_cover_image = album_cover_image
        self.__return_to_main_window_button = return_to_main_window_button
        self.__progress_bar = progress_bar
        self.__download_status_label = download_status_label
        self.__directory_where_song_will_be_saved_to = directory_where_song_will_be_saved_to


        #--------------------- Making the actual download ------------------------------
        logging.warning("Starting to download: " + self.__song_title)

        # Setting the filename
        safe_song_title_for_filename = self.clear_string_from_forbidden_chars_for_file_names(self.__song_title)
        safe_artist_name_for_file_name = self.clear_string_from_forbidden_chars_for_file_names(self.__artist_name)
        filename = safe_song_title_for_filename + "_" + safe_artist_name_for_file_name + BETA_KEYBOARD

        #Changing to the default download directory
        os.chdir(self.__directory_where_song_will_be_saved_to)
        self.__download_status_label.configure(text="Extracting audio...")

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
        #--------------------- Finishing Making the actual download ------------------------------




        #--------------------- Setting Metadata ------------------------------
        # Executing the metadata command
        self.__download_status_label.configure(text="Setting metadata...")
        self.__metadata_setter.set_metadata(
                    song_title = song_title,
                    artist_name = artist_name,
                    album_name = album_name,
                    track_position_in_album = track_position_in_album,
                    song_genre = song_genre,
                    song_year = song_year,
                    album_cover_image = album_cover_image,
                    directory_where_song_will_be_saved_to = directory_where_song_will_be_saved_to,
                    filename = filename)
        #--------------------- Finished Setting Metadata ------------------------------
        

        
        self.__download_status_label.configure(\
            text="DOWNLOAD FINISHED! The file has been saved in the " + self.__directory_where_song_will_be_saved_to + " folder :D")
        self.__progress_bar.stop()
        self.__progress_bar.configure(mode="determinate",progress_color="green")
        self.__progress_bar.set(100)


        # Enabling the return to the main window button
        self.__return_to_main_window_button.configure(state=ctk.NORMAL,\
            fg_color=RETURN_TO_MAIN_WINDOW_BUTTON_ENABLED_BACKGROUND_COLOR)



    def clear_string_from_forbidden_chars_for_file_names(self, string_to_clean):
        forbidden_chars = ['<','>',':','"','/','|','?','*',"'",' ','(',')']
        clean_string = string_to_clean
        for char in forbidden_chars:
            clean_string = clean_string.replace(char, "_")
        return clean_string
