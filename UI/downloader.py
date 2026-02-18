import customtkinter as ctk
import PIL as pil
import subprocess
import logging
import os
import threading
from UI import DownloadSongTab
from UI import SetMetadataToExistingSongTab

APPLICATION_NAME = "Toniná"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

FFMPEG_NOT_INSTALLED_MESSAGE = "Sorry, FFMPEG is not installed on your computer :( \
                                \nPlease close this window and install FFMPEG to use this software correctly."
FFMPEG_NOT_INSTALLED_MESSAGE_X_POS = 100
FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS = 10


TAB_SEPARATOR = "🎧"
TABS_BACKGROUND_COLOR = "#360185"
TABS_FOREGROUND_COLOR = "#360185"
SEGMENTED_BUTTON_FG_COLOR = "#360185"
SEGMENTED_BUTTON_UNSELECTED_COLOR = "#360185"
SEGMENTED_BUTTON_SELECTED_COLOR = "#15173D"
SEGMENTED_BUTTON_UNSELECTED_HOVER_COLOR = "#F4B342"
TABS_TEXT_COLOR = "#DE1A58"
TABS_BORDER_COLOR = "#EDEDCE"


class Downloader:
    def __init__(self):
        # Initializing the root to contain the main frame of the GUI application
        self.__root = ctk.CTk()

        # Saving original running directory
        self.__original_working_dir = os.getcwd()

         # Initializing the three main tabs.
        # 1. Download Song
        # 2. Dummy tab, just a separator
        # 3. Set metadata on existing song
        self.__tabs = ctk.CTkTabview(self.__root,
                        width=WINDOW_WIDTH,
                        height=WINDOW_HEIGHT,
                        bg_color=TABS_BACKGROUND_COLOR,
                        fg_color=TABS_FOREGROUND_COLOR,
                        segmented_button_fg_color=SEGMENTED_BUTTON_FG_COLOR,
                        segmented_button_unselected_color=SEGMENTED_BUTTON_UNSELECTED_COLOR,
                        segmented_button_selected_color=SEGMENTED_BUTTON_SELECTED_COLOR,
                        segmented_button_unselected_hover_color=SEGMENTED_BUTTON_UNSELECTED_HOVER_COLOR,
                        text_color=TABS_TEXT_COLOR,
                        anchor="nw",
                        border_color=TABS_BORDER_COLOR,
                        border_width=3)
        self.__tabs._segmented_button.configure(font=ctk.CTkFont(family="Times New Roman", size=25, weight="bold"))
        self.__tabs.pack(fill="both", expand=True)

        # Setting the tab where user downloads a song.
        self.__download_song_tab = DownloadSongTab.DownloadSongTab(self.__root,
                                                                    self.__tabs,
                                                                    self.__original_working_dir)

        # Setting a dummy tab as a separator
        self.__tabs.add(TAB_SEPARATOR)
        self.__tabs._segmented_button._buttons_dict[TAB_SEPARATOR].configure(state="disabled")


        # Setting the tab where user downloads a song.
        self.__set_metadata_to_an_existing_song_tab = SetMetadataToExistingSongTab.SetMetadataToExistingSongTab(
                                                                    self.__root,
                                                                    self.__tabs,
                                                                    self.__original_working_dir)



    def start(self):
        # Calculating some coordinates to center the window frame in the middle of computer screen
        self.__root.minsize(WINDOW_WIDTH,WINDOW_HEIGHT)
        self.__root.maxsize(WINDOW_WIDTH,WINDOW_HEIGHT)
        screen_width = self.__root.winfo_screenwidth()
        screen_height = self.__root.winfo_screenheight()
        x_pos = int((screen_width - WINDOW_WIDTH)/2)
        y_pos = int((screen_height - WINDOW_HEIGHT)/2)
        self.__root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_pos}+{y_pos}")


        # Setting the icon of the application
        icon_photo_image = pil.ImageTk.PhotoImage(pil.Image.open("Images/glifo_maya_icon.png"))
        self.__root.wm_iconphoto(True,icon_photo_image)


        # Setting the application name
        self.__root.title(APPLICATION_NAME)


        # Checking if FFMPEG is installed in user's computer
        is_ffmpeg_installed = True
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except FileNotFoundError:
            logging.warning("ffmpeg is not installed in this computer, please install ffmpeg.")
            # Informing the user that ffmpeg is not installed correctly in the computer.
            self.__ffmpeg_not_installed_label_1 = ctk.CTkLabel(self.__download_song_tab,
                                                                anchor="nw",
                                                                text=FFMPEG_NOT_INSTALLED_MESSAGE,
                                                                font=('Times New Roman',25))
            self.__ffmpeg_not_installed_label_1.place(x = FFMPEG_NOT_INSTALLED_MESSAGE_X_POS,
                                                    y = FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS)

            self.__ffmpeg_not_installed_label_2 = ctk.CTkLabel(self.__set_metadata_to_an_existing_song_tab,
                                                                anchor="nw",
                                                                text=FFMPEG_NOT_INSTALLED_MESSAGE,
                                                                font=('Times New Roman',25))
            self.__ffmpeg_not_installed_label_2.place(x = FFMPEG_NOT_INSTALLED_MESSAGE_X_POS,
                                                    y = FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS)

            is_ffmpeg_installed = False


        # If FFMPEG is installed, then the normal UI is created
        if(is_ffmpeg_installed):
            self.set_user_interface()

        # Starting the windows
        self.__root.mainloop()



    def set_user_interface(self):
        self.__download_song_tab.set_interface()
        self.__set_metadata_to_an_existing_song_tab.set_interface()






