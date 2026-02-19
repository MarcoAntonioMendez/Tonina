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
TONINA_TITLE_TEXT_COLOR = "#eed6b7"

# Constants for metadata
SONG_METADATA_SECTIONS_TEXTS_LIST = ["Title:","Artist:","Album:","Album Track:",\
                                    "Genre:","Year:","Mp3 File:","Album Cover:"]
# The following indexes must follow the order of the past list (SONG_METADATA_SECTIONS_TEXTS_LIST)
SONG_TITLE_INDEX = 0
ARTIST_NAME_INDEX = 1
ALBUM_NAME_INDEX = 2
ALBUM_TRACK_POSITION_INDEX = 3
SONG_GENRE_INDEX = 4
SONG_YEAR_INDEX = 5


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

CHOOSE_ALBUM_COVER_TEXT = "Choose Image"
CHOOSE_ALBUM_COVER_BACKGROUND_COLOR = "#59239a"
CHOOSE_ALBUM_COVER_BORDER_COLOR = "#998a76"
CHOOSE_ALBUM_COVER_BORDER_WIDTH = 3
CHOOSE_ALBUM_COVER_CORNER_RADIUS = 5

CHOOSE_MP3_FILE_TEXT = "Choose Mp3 File"
CHOOSE_MP3_FILE_BACKGROUND_COLOR = "#59239a"
CHOOSE_MP3_FILE_BORDER_WIDTH = 3
CHOOSE_MP3_FILE_CORNER_RADIUS = 5
CHOOSE_MP3_FILE_BORDER_COLOR = "#998a76"



# Constants for the button set the metadata to the the song
SET_METADATA_BUTTON_TEXT = "Set Metadata"
SET_METADATA_BUTTON_BORDER_COLOR = "#c74716"
ACTION_BUTTON_SIZE = 35
SET_METADATA_BUTTON_X_POS = 705
SET_METADATA_BUTTON_Y_POS = 390


# Constants for the button to reset the entries for metadata parameters
RESET_BUTTON_TEXT = "Reset"
RESET_BUTTON_BORDER_COLOR = "#1680c7"
RESET_BUTTON_X_POS = 25
RESET_BUTTON_Y_POS = 390

CHOOSE_ALBUM_COVER_FILE_DIALOG_TEXT = "Select an image for the album cover"
SUPPORTED_IMAGES_EXTENSIONS = [("Images","*.png"),("Images","*.jpg")]


CHOOSE_MP3_FILE_DIALOG_TEXT = "Select an mp3 file"
SUPPORTED_MUSIC_FILE_EXTENSIONS = [("Mp3 files","*.mp3")]

class SetMetadataToExistingSongTab:
    def __init__(self, main_root, tabs, original_working_dir):
        # Initializing list of entry widgets
        self.__widget_entries = []

        # Initializing string to hold album cover image file path
        self.__album_cover_image_file_full_path = ""

        # Initializing string to hold mp3 file path
        self.__mp3_file_full_path = ""

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
        # Traversing through the list containing the song metadata text.
        # In each turn of the loop, the x and y coordinates of the visual elements are calcualted and set.
        for index in range(len(SONG_METADATA_SECTIONS_TEXTS_LIST)):
            #Painting rectangles to contain labels of song metadata
            diff = index*LABELS_METADATA_SECTION_DIFF
            x_pos_1 = INITIAL_LABEL_SECTION_RECTANGLE_X_POS_1
            y_pos_1 = INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_1+diff
            x_pos_2 = INITIAL_LABEL_SECTION_RECTANGLE_X_POS_2
            y_pos_2 = INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_2+diff
            self.__set_metadata_to_an_existing_song_tab_canvas.create_rectangle(x_pos_1,y_pos_1,x_pos_2,y_pos_2,\
                                            outline=LABEL_RECTANGLE_OUTLINE_COLOR, width=2)


            # Painting the song metadata text
            x_pos = INITIAL_LABEL_SECTION_TEXT_X_POS
            y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff
            text = SONG_METADATA_SECTIONS_TEXTS_LIST[index]
            self.__set_metadata_to_an_existing_song_tab_canvas.create_text(x_pos,y_pos, anchor="nw",text=text,\
                                    font=('Times New Roman',20),fill=TONINA_TITLE_TEXT_COLOR)


            # Setting the textboxes and the button to choose album cover
            if(index <=  SONG_YEAR_INDEX):
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff-ENTRY_SECTION_Y_POS_OFFSET
                entry_widget = ctk.CTkEntry(self.__set_metadata_to_an_existing_song_tab,
                                            font=('Times New Roman',20),
                                            width=ENTRY_WIDGET_WIDTH)
                entry_widget.place(x = x_pos, y = y_pos)
                entry_widget.bind("<<Paste>>", self.custom_paste_handler)
                entry_widget.bind("<Control-v>", self.custom_paste_handler)
                self.__widget_entries.append(entry_widget)
            elif(index == (SONG_YEAR_INDEX+1)):
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff-ENTRY_SECTION_Y_POS_OFFSET
                self.__choose_mp3_file_button = ctk.CTkButton(
                                                self.__set_metadata_to_an_existing_song_tab,
                                                font=('Times New Roman',20,"italic"),
                                                text=CHOOSE_MP3_FILE_TEXT,
                                                width=ENTRY_WIDGET_WIDTH,
                                                fg_color=CHOOSE_MP3_FILE_BACKGROUND_COLOR,
                                                text_color=TONINA_TITLE_TEXT_COLOR,
                                                border_width=CHOOSE_MP3_FILE_BORDER_WIDTH,
                                                corner_radius=CHOOSE_MP3_FILE_CORNER_RADIUS,
                                                border_color=CHOOSE_MP3_FILE_BORDER_COLOR,
                                                command=self.choose_mp3_file_dialog)
                self.__choose_mp3_file_button.place(x = x_pos, y = y_pos)
            else:
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff-ENTRY_SECTION_Y_POS_OFFSET
                self.__choose_album_cover_button = ctk.CTkButton(
                                                self.__set_metadata_to_an_existing_song_tab,
                                                font=('Times New Roman',20,"italic"),
                                                text=CHOOSE_ALBUM_COVER_TEXT,
                                                width=ENTRY_WIDGET_WIDTH,
                                                fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,
                                                text_color=TONINA_TITLE_TEXT_COLOR,
                                                border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,
                                                corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,
                                                border_color=CHOOSE_ALBUM_COVER_BORDER_COLOR,
                                                command=self.choose_album_cover_dialog)
                self.__choose_album_cover_button.place(x = x_pos, y = y_pos)


        # Creating download button
        button_icon = ctk.CTkImage(pil.Image.open("Images/red_arrow.png"),
                                    size=(ACTION_BUTTON_SIZE, ACTION_BUTTON_SIZE))
        self.__download_song_button = ctk.CTkButton(self.__set_metadata_to_an_existing_song_tab,
                                                    font=('Times New Roman',30,"italic"),
                                                    text=SET_METADATA_BUTTON_TEXT,
                                                    fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,
                                                    text_color=TONINA_TITLE_TEXT_COLOR,
                                                    border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,
                                                    corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,
                                                    border_color=SET_METADATA_BUTTON_BORDER_COLOR,
                                                    image=button_icon,
                                                    command=self.check_if_everything_is_good_to_set_metadata_to_a_song)
        self.__download_song_button.place(x=SET_METADATA_BUTTON_X_POS,y=SET_METADATA_BUTTON_Y_POS)


        # Creating reset button
        reset_icon = ctk.CTkImage(pil.Image.open("Images/reset_icon.png"),
                                    size=(ACTION_BUTTON_SIZE, ACTION_BUTTON_SIZE))
        self.__reset_button = ctk.CTkButton(self.__set_metadata_to_an_existing_song_tab,
                                            font=('Times New Roman',30,"italic"),
                                            text=RESET_BUTTON_TEXT,
                                            fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,
                                            text_color=TONINA_TITLE_TEXT_COLOR,
                                            border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,
                                            corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,
                                            border_color=RESET_BUTTON_BORDER_COLOR,
                                            image=reset_icon,
                                            command=self.reset_all_fields)
        self.__reset_button.place(x = RESET_BUTTON_X_POS,y = RESET_BUTTON_Y_POS)



    def choose_album_cover_dialog(self):
        # Prompting the user to choose a file
        self.__album_cover_image_file_full_path, file_name = self.choose_file_dialog(
                                            choose_file_prompt_text = CHOOSE_ALBUM_COVER_FILE_DIALOG_TEXT,
                                            type_of_file_extension = SUPPORTED_IMAGES_EXTENSIONS)

        # Checking the file was correctly selected
        if(self.__album_cover_image_file_full_path != None and file_name != None):
            self.__choose_album_cover_button.configure(text=file_name)
        else:
            self.__choose_album_cover_button.configure(text=CHOOSE_ALBUM_COVER_TEXT)



    def choose_mp3_file_dialog(self):
        # Prompting the user to choose a file
        self.__mp3_file_full_path, file_name = self.choose_file_dialog(
                                            choose_file_prompt_text = CHOOSE_MP3_FILE_DIALOG_TEXT,
                                            type_of_file_extension = SUPPORTED_MUSIC_FILE_EXTENSIONS)

        # Checking the file was correctly selected
        if(self.__mp3_file_full_path != None and file_name != None):
            self.__choose_mp3_file_button.configure(text=file_name)
        else:
            self.__choose_mp3_file_button.configure(text=CHOOSE_MP3_FILE_TEXT)




    def choose_file_dialog(self, choose_file_prompt_text: str, type_of_file_extension: list):
        # Opening the file dialog to choose a file
        selected_file_full_path = ctk.filedialog.askopenfilename(title=choose_file_prompt_text,
                                                        filetypes=type_of_file_extension)

        # Checking if user actually chose something or if the cancel button was pressed
        if(selected_file_full_path):

            file_name = ""

            # Getting only the file name from the full path
            for index in range(len(selected_file_full_path) - 1, -1, -1):
                if(selected_file_full_path[index] == '/'):
                    break
                else:
                    file_name += selected_file_full_path[index]

            # At this point, the file name is reversed so it's needed to sort it out
            file_name = file_name[::-1]

            # Changing the look of the self.__choose_album_cover_button
            return selected_file_full_path,file_name
        else:
            return None,None



    def check_if_everything_is_good_to_set_metadata_to_a_song(self):
        print()



    def reset_all_fields(self):
        # Clearing all entries and the album cover image file
        self.__album_cover_image_file_full_path = ""
        self.__choose_album_cover_button.configure(text=CHOOSE_ALBUM_COVER_TEXT)
        self.__choose_mp3_file_button.configure(text=CHOOSE_MP3_FILE_TEXT)

        for entry in self.__widget_entries:
            entry.delete(0, ctk.END)



    def custom_paste_handler(self,event):
        clipboard_content = event.widget.clipboard_get()
        event.widget.insert(ctk.END, clipboard_content)
        return "break"

