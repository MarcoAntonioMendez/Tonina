import customtkinter as ctk
import PIL as pil
import subprocess
import logging
import os
import threading
from UI import downloader
from UI import MissingMetadataScreen
from UI import DownloadSongProgressScreen


# General Constants
TONINA_TITLE = "TONINÁ"
TONINA_TITLE_TEXT_COLOR = "#eed6b7"


SONG_METADATA_SECTIONS_TEXTS_LIST = ["Title:","Artist:","Album:","Album Track:",\
                                    "Genre:","Year:","Youtube URL:","Album Cover:"]
# The following indexes must follow the order of the past list (SONG_METADATA_SECTIONS_TEXTS_LIST)
SONG_TITLE_INDEX = 0
ARTIST_NAME_INDEX = 1
ALBUM_NAME_INDEX = 2
ALBUM_TRACK_POSITION_INDEX = 3
SONG_GENRE_INDEX = 4
SONG_YEAR_INDEX = 5
SONG_YOUTUBE_URL_INDEX = 6


DOWNLOAD_SONG_TAB_NAME = "Download New Song"


# Constants for labels containing the text of the metadata parameters.
LABELS_METADATA_SECTION_DIFF = 42
INITIAL_LABEL_SECTION_RECTANGLE_X_POS_1,INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_1 = 20, 20
INITIAL_LABEL_SECTION_RECTANGLE_X_POS_2,INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_2 = 230, 50
INITIAL_LABEL_SECTION_TEXT_X_POS = 30
INITIAL_LABEL_SECTION_TEXT_Y_POS = 25
LABEL_RECTANGLE_OUTLINE_COLOR = "#7636C3"


# Constants for entries in which the user will enter the value for metadata parameter.
ENTRY_WIDGET_WIDTH = 685
INITIAL_ENTRY_SECTION_X_POS = 240
ENTRY_SECTION_Y_POS_OFFSET = 5


# Constants for the button to choose an album cover image
CHOOSE_ALBUM_COVER_TEXT = "Choose Image"
CHOOSE_ALBUM_COVER_BACKGROUND_COLOR = "#59239a"
CHOOSE_ALBUM_COVER_BORDER_COLOR = "#998a76"
CHOOSE_ALBUM_COVER_BORDER_WIDTH = 3
CHOOSE_ALBUM_COVER_CORNER_RADIUS = 5


# Constants for the button  to download the song
DOWNLOAD_SONG_BUTTON_TEXT = "Download Song"
DOWNLOAD_SONG_BUTTON_BORDER_COLOR = "#c74716"
DOWNLOAD_SONG_BUTTON_SIZE = 35
DOWNLOAD_SONG_BUTTON_X_POS = 673
DOWNLOAD_SONG_BUTTON_Y_POS = 390


# Constants for the button to reset the entries for metadata parameters
RESET_BUTTON_TEXT = "Reset"
RESET_BUTTON_BORDER_COLOR = "#1680c7"
RESET_BUTTON_X_POS = 25
RESET_BUTTON_Y_POS = 390


CHOOSE_ALBUM_COVER_FILE_DIALOG_TEXT = "Select an image for the album cover"
CHOOSE_ALBUM_COVER_FILE_DIALOG_IMAGES_TEXT = "Images"


class DownloadSongTab:
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

        # Initializing the DownloadSongProgressScreen.
        self.__dowload_song_progress_screen = DownloadSongProgressScreen.DownloadSongProgressScreen(main_root)

        # Setting the tab where user downloads a song.
        self.__download_song_tab = tabs.add(DOWNLOAD_SONG_TAB_NAME)
        self.__download_song_tab_canvas = ctk.CTkCanvas(self.__download_song_tab,
                                                        width=downloader.WINDOW_WIDTH,
                                                        height=downloader.WINDOW_HEIGHT,
                                                        highlightthickness=0,
                                                        background=downloader.TABS_BACKGROUND_COLOR)
        self.__download_song_tab_canvas.pack(fill="both", expand=True)



    def set_interface(self):
        # Traversing through the list containing the song metadata text.
        # In each turn of the loop, the x and y coordinates of the visual elements are calcualted and set.
        for index in range(len(SONG_METADATA_SECTIONS_TEXTS_LIST)):
            #Painting rectangles to contain labels of song metadata
            diff = index*LABELS_METADATA_SECTION_DIFF
            x_pos_1 = INITIAL_LABEL_SECTION_RECTANGLE_X_POS_1
            y_pos_1 = INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_1+diff
            x_pos_2 = INITIAL_LABEL_SECTION_RECTANGLE_X_POS_2
            y_pos_2 = INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_2+diff
            self.__download_song_tab_canvas.create_rectangle(x_pos_1,y_pos_1,x_pos_2,y_pos_2,\
                                            outline=LABEL_RECTANGLE_OUTLINE_COLOR, width=2)


            # Painting the song metadata text
            x_pos = INITIAL_LABEL_SECTION_TEXT_X_POS
            y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff
            text = SONG_METADATA_SECTIONS_TEXTS_LIST[index]
            self.__download_song_tab_canvas.create_text(x_pos,y_pos, anchor="nw",text=text,\
                                    font=('Times New Roman',20),fill=TONINA_TITLE_TEXT_COLOR)


            # Setting the textboxes and the button to choose album cover
            if(index != (len(SONG_METADATA_SECTIONS_TEXTS_LIST)-1) ):
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff-ENTRY_SECTION_Y_POS_OFFSET
                entry_widget = ctk.CTkEntry(self.__download_song_tab,
                                            font=('Times New Roman',20),
                                            width=ENTRY_WIDGET_WIDTH)
                entry_widget.place(x = x_pos, y = y_pos)
                entry_widget.bind("<<Paste>>", self.custom_paste_handler)
                entry_widget.bind("<Control-v>", self.custom_paste_handler)
                self.__widget_entries.append(entry_widget)
            else:
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff-ENTRY_SECTION_Y_POS_OFFSET
                self.__choose_album_cover_button = ctk.CTkButton(self.__download_song_tab,
                                                font=('Times New Roman',20,"italic"),\
                                                text=CHOOSE_ALBUM_COVER_TEXT,\
                                                width=ENTRY_WIDGET_WIDTH,\
                                                fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                                                text_color=TONINA_TITLE_TEXT_COLOR,\
                                                border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,\
                                                corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,\
                                                border_color=CHOOSE_ALBUM_COVER_BORDER_COLOR,\
                                                command=self.choose_album_cover_dialog)
                self.__choose_album_cover_button.place(x = x_pos, y = y_pos)


        # Creating download button
        button_icon = ctk.CTkImage(pil.Image.open("Images/red_arrow.png"),\
                                    size=(DOWNLOAD_SONG_BUTTON_SIZE, DOWNLOAD_SONG_BUTTON_SIZE))
        self.__download_song_button = ctk.CTkButton(self.__download_song_tab,\
                                                    font=('Times New Roman',30,"italic"),\
                                                    text=DOWNLOAD_SONG_BUTTON_TEXT,\
                                                    fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                                                    text_color=TONINA_TITLE_TEXT_COLOR,\
                                                    border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,\
                                                    corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,\
                                                    border_color=DOWNLOAD_SONG_BUTTON_BORDER_COLOR,\
                                                    image=button_icon,\
                                                    command=self.check_if_everything_is_good_to_download_a_song)
        self.__download_song_button.place(x = DOWNLOAD_SONG_BUTTON_X_POS,\
                                        y = DOWNLOAD_SONG_BUTTON_Y_POS)


        # Creating reset button
        reset_icon = ctk.CTkImage(pil.Image.open("Images/reset_icon.png"),\
                                    size=(DOWNLOAD_SONG_BUTTON_SIZE, DOWNLOAD_SONG_BUTTON_SIZE))
        self.__reset_button = ctk.CTkButton(self.__download_song_tab,\
                                            font=('Times New Roman',30,"italic"),\
                                            text=RESET_BUTTON_TEXT,\
                                            fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                                            text_color=TONINA_TITLE_TEXT_COLOR,\
                                            border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,\
                                            corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,\
                                            border_color=RESET_BUTTON_BORDER_COLOR,\
                                            image=reset_icon,\
                                            command=self.reset_all_fields)
        self.__reset_button.place(x = RESET_BUTTON_X_POS,y = RESET_BUTTON_Y_POS)



    def choose_album_cover_dialog(self):
        # Opening the file dialog to choose an image for the album cover
        self.__album_cover_image_file_full_path = ctk.filedialog.askopenfilename(\
            title=CHOOSE_ALBUM_COVER_FILE_DIALOG_TEXT,\
            filetypes=[(CHOOSE_ALBUM_COVER_FILE_DIALOG_IMAGES_TEXT, "*.png"),\
            (CHOOSE_ALBUM_COVER_FILE_DIALOG_IMAGES_TEXT, "*.jpg")])

        # Checking if user actually chose something or if the cancel button was pressed
        if(self.__album_cover_image_file_full_path):

            self.__album_cover_image_file = ""

            # Getting only the file name from the full path
            for index in range(len(self.__album_cover_image_file_full_path) - 1, -1, -1):
                if(self.__album_cover_image_file_full_path[index] == '/'):
                    break
                else:
                    self.__album_cover_image_file += self.__album_cover_image_file_full_path[index]

            # At this point, the file name is reversed so it's needed to sort it out
            self.__album_cover_image_file = self.__album_cover_image_file[::-1]

            # Changing the look of the self.__choose_album_cover_button
            self.__choose_album_cover_button.configure(text=self.__album_cover_image_file)
        else:
            self.__choose_album_cover_button.configure(text=CHOOSE_ALBUM_COVER_TEXT)



    def check_if_everything_is_good_to_download_a_song(self):
        # Checking all entries and album cover button
        all_metadata_set = self.has_all_metadta_been_set()
        os.chdir(self.__original_working_dir)


        # If the user entered the metadata correctly, then the song will start to be downloaded.
        # If some of the metadata is missing, then the software will show a warning message
        if(all_metadata_set):
            # All metadata is fine, starting to download
            self.__dowload_song_progress_screen.download_song(
                album_cover_image_file_full_path = self.__album_cover_image_file_full_path,
                widget_entries = self.__widget_entries)
        else:
            # Some metadata is missing, inform the user of the issue
            self.__missing_metadata_screen.inform_user_some_metadata_is_missing()



    def has_all_metadta_been_set(self):
        all_metadata_set = True
        for entry in self.__widget_entries:
            if(entry.get() == ""):
                all_metadata_set = False

        if(self.__album_cover_image_file_full_path == ""):
            all_metadata_set = False

        return all_metadata_set



    def reset_all_fields(self):
        # Clearing all entries and the album cover image file
        self.__album_cover_image_file_full_path = ""
        self.__choose_album_cover_button.configure(text=CHOOSE_ALBUM_COVER_TEXT)

        for entry in self.__widget_entries:
            entry.delete(0, ctk.END)



    def custom_paste_handler(self,event):
        clipboard_content = event.widget.clipboard_get()
        event.widget.insert(ctk.END, clipboard_content)
        return "break"



