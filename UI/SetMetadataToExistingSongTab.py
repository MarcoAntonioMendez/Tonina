import customtkinter as ctk
import PIL as pil
import subprocess
import logging
import os
import threading
from UI import downloader
from UI import MissingMetadataScreen


# General constants
SET_METADATA_TO_EXISTING_SONG_SONG_TAB_NAME = "Set Metadata to an Existing Song"


class SetMetadataToExistingSongTab:
    def __init__(self, main_root, tabs, original_working_dir):
        # Initializing list of entry widgets
        self.__widget_entries = []

        # Initializing string to hold album cover image file path
        self.__album_cover_image_file_full_path = ""

        # Saving original working directory
        self.__original_working_dir = original_working_dir

        # Savinf the main root
        self.__root = main_root

        # Initializing the MissingMetadataScreen in case it's needed.
        self.__missing_metadata_screen = MissingMetadataScreen.MissingMetadataScreen(main_root)


        # Setting the tab where user downloads a song.
        self.__set_metadata_to_an_existing_song_tab = tabs.add(SET_METADATA_TO_EXISTING_SONG_SONG_TAB_NAME)
        self.__set_metadata_to_an_existing_song_tab_canvas = ctk.CTkCanvas(
                                                        self.__set_metadata_to_an_existing_song_tab,
                                                        width=downloader.WINDOW_WIDTH,
                                                        height=downloader.WINDOW_HEIGHT,
                                                        highlightthickness=0,
                                                        background=downloader.TABS_BACKGROUND_COLOR)
        self.__set_metadata_to_an_existing_song_tab_canvas.pack(fill="both", expand=True)



    def set_interface(self):
        print()

