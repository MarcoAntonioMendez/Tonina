import customtkinter as ctk
import PIL as pil
import threading
from UI import DownloadSongTab
from DownloadEngine import mp3_downloader_engine


# General constants
DOWNLOAD_PROGRESS_SCREEN_BACKGROUND_COLOR = "#360185"
DOWNLOAD_PROGRESS_SCREEN_TITLE_TEXT = "Downloading..."
DOWNLOAD_PROGRESS_SCREEN_WIDTH = 300
DOWNLOAD_PROGRESS_SCREEN_HEIGHT = 533



# Constants for asking user to select a directory
SELECT_DIRECTORY_BUTTON_TEXT = "Select a Directory"
SELECT_DIRECTORY_BUTTON_X_POS = 17
SELECT_DIRECTORY_BUTTON_Y_POS = 200
SELECT_DIRECTORY_BUTTON_BORDER_WIDTH = 3
SELECT_DIRECTORY_BUTTON_CORNER_RADIUS = 5
SELECT_DIRECTORY_BUTTON_TEXT_COLOR = "#eed6b7"
SELECT_DIRECTORY_BUTTON_BORDER_COLOR = "#1680c7"
SELECT_DIRECTORY_BUTTON_BACKGROUND_COLOR = "#59239a"

ASK_USER_TO_SELECT_DIRECTORY_TEXT_COLOR = "#eed6b7"
ASK_USER_TO_SELECT_DIRECTORY_TEXT = "Please select a directory \n\
where the song will \n\
be saved to."
ASK_USER_TO_SELECT_DIRECTORY_TEXT_X_POS = 10
ASK_USER_TO_SELECT_DIRECTORY_TEXT_Y_POS = 10



# Constants for download progress screen
ALBUM_COVER_IMAGE_FOR_STATUS_SIZE = 150
ALBUM_COVER_IMAGE_FOR_STATUS_X_POS = 80
ALBUM_COVER_IMAGE_FOR_STATUS_Y_POS = 20
STATUS_LABELS_SPACE_BETWEEN = 5
STATUS_LABELS_WRAP_LENGTH = 250
SONG_TITLE_FOR_STATUS_X_POS = 20
SONG_TITLE_FOR_STATUS_Y_POS = 190
DOWNLOAD_STARTING_STATUS = "Starting the download..."
PROGRESS_BAR_SPACE_BETWEEN = 50
DOWNLOAD_STATUS_SPACE_BETWEEN = 10
DOWNLOAD_PROGRESS_STATUS_TEXTS_COLOR = "#eed6b7"


RETURN_TO_MAIN_WINDOW_BUTTON_TEXT = "Go Back to the Main Screen"
RETURN_TO_MAIN_WINDOW_BUTTON_X_POS = 17
RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS = 480
RETURN_TO_MAIN_WINDOW_BUTTON_DISABLED_BACKGROUND_COLOR = "#0f2933"
RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_WIDTH = 3
RETURN_TO_MAIN_WINDOW_BUTTON_CORNER_RADIUS = 5
RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_COLOR = "#1680c7"


class DownloadSongProgressScreen:
    def __init__(self, root):
        self.__root = root
        self.__top = None
        self.__directory_where_song_will_be_saved_to = None

        # Initializing the downloader_engine
        self.__downloader_engine = mp3_downloader_engine.Mp3DownloaderEngine()



    def download_song(self, album_cover_image_file_full_path, widget_entries):
        # Assigning some variables values
        self.__album_cover_image_file_full_path = album_cover_image_file_full_path
        self.__widget_entries = widget_entries


        # Prompting the user to select a directory where the song will be saved to.
        self.ask_the_user_to_select_a_directory()


        if(self.__directory_where_song_will_be_saved_to):
            # Now that user has selected a directory, the download starts
            self.start_the_download()



    def ask_the_user_to_select_a_directory(self):
        # Creating the frame
        self.build_frame()


        # Creating the label to inform the user to select a directory to save the song
        self.__ask_user_to_select_directory_label = ctk.CTkLabel(self.__top,
                                            font=('Times New Roman',27),
                                            text=ASK_USER_TO_SELECT_DIRECTORY_TEXT,
                                            anchor="nw",
                                            text_color=ASK_USER_TO_SELECT_DIRECTORY_TEXT_COLOR)
        self.__ask_user_to_select_directory_label.place(x=ASK_USER_TO_SELECT_DIRECTORY_TEXT_X_POS,
                                                        y=ASK_USER_TO_SELECT_DIRECTORY_TEXT_Y_POS)


        # Creating the button to prompt the user to select a directory
        self.__select_directory_button = ctk.CTkButton(self.__top,
                                            font=('Times New Roman',35,"italic"),
                                            text=SELECT_DIRECTORY_BUTTON_TEXT,
                                            fg_color=SELECT_DIRECTORY_BUTTON_BACKGROUND_COLOR,
                                            text_color=SELECT_DIRECTORY_BUTTON_TEXT_COLOR,
                                            border_width=SELECT_DIRECTORY_BUTTON_BORDER_WIDTH,
                                            corner_radius=SELECT_DIRECTORY_BUTTON_CORNER_RADIUS,
                                            border_color=SELECT_DIRECTORY_BUTTON_BORDER_COLOR,
                                            command=self.prompt_user_to_select_directory)
        self.__select_directory_button.place(x = SELECT_DIRECTORY_BUTTON_X_POS,
                                                y = SELECT_DIRECTORY_BUTTON_Y_POS)


        # Disables the original root and only the MissingMetadataScreen becomes active
        self.__top.focus()
        self.__top.transient(self.__root)
        self.__top.grab_set()
        self.__top.wait_window(self.__top)



    def build_frame(self):
        # Creating the frame
        self.__top = ctk.CTkToplevel(fg_color=DOWNLOAD_PROGRESS_SCREEN_BACKGROUND_COLOR)
        self.__top.title(DOWNLOAD_PROGRESS_SCREEN_TITLE_TEXT)
        self.__top.minsize(DOWNLOAD_PROGRESS_SCREEN_WIDTH,DOWNLOAD_PROGRESS_SCREEN_HEIGHT)
        self.__top.maxsize(DOWNLOAD_PROGRESS_SCREEN_WIDTH,DOWNLOAD_PROGRESS_SCREEN_HEIGHT)
        # Setting the size of the frame
        screen_width = self.__top.winfo_screenwidth()
        screen_height = self.__top.winfo_screenheight()
        x_pos = int((screen_width - DOWNLOAD_PROGRESS_SCREEN_WIDTH)/2)
        y_pos = int((screen_height - DOWNLOAD_PROGRESS_SCREEN_HEIGHT)/2)
        self.__top.geometry(f"{DOWNLOAD_PROGRESS_SCREEN_WIDTH}x{DOWNLOAD_PROGRESS_SCREEN_HEIGHT}+{x_pos}+{y_pos}")



    def prompt_user_to_select_directory(self):
        # Asking the user to select a directory where the song will be saved to
        self.__directory_where_song_will_be_saved_to = ctk.filedialog.askdirectory(title="Select a directory to where the song will be saved to:")


        # Checking if user actually chose a directory or if the cancel button was pressed
        if(self.__directory_where_song_will_be_saved_to):
            self.return_to_main_window()
        else:
            print()



    def start_the_download(self):
        # Creating the interface to inform the user about the download progress.
        self.build_download_interface()


        # Start the download
        download_thread = threading.Thread(target=self.call_the_downloader)
        download_thread.start()



    def build_download_interface(self):
        # Creating the frame
        self.build_frame()


        # Adding graphical elements
        # Adding the album cover of the song being downloaded
        pil_image = pil.Image.open(self.__album_cover_image_file_full_path)
        ctk_image = ctk.CTkImage(light_image=pil_image,
                        dark_image=pil_image,
                        size=(ALBUM_COVER_IMAGE_FOR_STATUS_SIZE, ALBUM_COVER_IMAGE_FOR_STATUS_SIZE))
        album_cover_image_for_status = ctk.CTkLabel(self.__top, image=ctk_image, text="")
        album_cover_image_for_status.place(x = ALBUM_COVER_IMAGE_FOR_STATUS_X_POS,
                                            y = ALBUM_COVER_IMAGE_FOR_STATUS_Y_POS)


        # Adding the name of te song being downloaded
        song_title_for_status = ctk.CTkLabel(self.__top,
                            text=self.__widget_entries[DownloadSongTab.SONG_TITLE_INDEX].get(),
                            font=('Times New Roman',19),
                            wraplength=STATUS_LABELS_WRAP_LENGTH,
                            fg_color=DOWNLOAD_PROGRESS_SCREEN_BACKGROUND_COLOR,
                            text_color=DOWNLOAD_PROGRESS_STATUS_TEXTS_COLOR)
        song_title_for_status.place(x = SONG_TITLE_FOR_STATUS_X_POS, y = SONG_TITLE_FOR_STATUS_Y_POS)
        self.__top.update_idletasks()


        # Adding the name of the artist being downloaded
        song_artist_for_status = ctk.CTkLabel(self.__top,
                            text=self.__widget_entries[DownloadSongTab.ARTIST_NAME_INDEX].get(),
                            font=('Times New Roman',19),
                            wraplength=STATUS_LABELS_WRAP_LENGTH,
                            fg_color=DOWNLOAD_PROGRESS_SCREEN_BACKGROUND_COLOR,
                            text_color=DOWNLOAD_PROGRESS_STATUS_TEXTS_COLOR)
        x_pos_for_artist_name = SONG_TITLE_FOR_STATUS_X_POS
        y_pos_for_artist_name = SONG_TITLE_FOR_STATUS_Y_POS\
                                + song_title_for_status.winfo_height()\
                                + song_artist_for_status.winfo_height()\
                                + STATUS_LABELS_SPACE_BETWEEN
        song_artist_for_status.place(x = x_pos_for_artist_name,y = y_pos_for_artist_name)
        self.__top.update_idletasks()


        # Adding the progress bar
        self.__progress_bar = ctk.CTkProgressBar(self.__top,
                                                orientation="horizontal",
                                                mode="indeterminate",
                                                width=250,
                                                height=20,
                                                progress_color="#DE1A58")
        self.__progress_bar.start()
        x_pos_for_progress_bar = SONG_TITLE_FOR_STATUS_X_POS
        y_pos_for_progress_bar = SONG_TITLE_FOR_STATUS_Y_POS\
                                + song_title_for_status.winfo_height()\
                                + song_artist_for_status.winfo_height()\
                                + PROGRESS_BAR_SPACE_BETWEEN
        self.__progress_bar.place(x = x_pos_for_progress_bar,y = y_pos_for_progress_bar)
        self.__top.update_idletasks()


        # Adding the label that will hold the specific stage in which the download is being carried on.
        self.__download_status_label = ctk.CTkLabel(self.__top,
                                                    text=DOWNLOAD_STARTING_STATUS,
                                                    font=('Times New Roman',16),
                                                    wraplength=STATUS_LABELS_WRAP_LENGTH,
                                                    fg_color=DOWNLOAD_PROGRESS_SCREEN_BACKGROUND_COLOR,
                                                    text_color=DOWNLOAD_PROGRESS_STATUS_TEXTS_COLOR)
        x_pos_download_status_label = SONG_TITLE_FOR_STATUS_X_POS
        y_pos_download_status_label = SONG_TITLE_FOR_STATUS_Y_POS\
                                    + song_title_for_status.winfo_height()\
                                    + song_artist_for_status.winfo_height()\
                                    + self.__download_status_label.winfo_height()\
                                    + self.__progress_bar.winfo_height()\
                                    + PROGRESS_BAR_SPACE_BETWEEN\
                                    + DOWNLOAD_STATUS_SPACE_BETWEEN
        self.__download_status_label.place(x=x_pos_download_status_label,y=y_pos_download_status_label)
        self.__top.update_idletasks()


        # Creating return to the main window button
        self.__return_to_main_window_button = ctk.CTkButton(self.__top,
                                            font=('Times New Roman',21,"italic"),
                                            text=RETURN_TO_MAIN_WINDOW_BUTTON_TEXT,
                                            fg_color=RETURN_TO_MAIN_WINDOW_BUTTON_DISABLED_BACKGROUND_COLOR,
                                            text_color=DOWNLOAD_PROGRESS_STATUS_TEXTS_COLOR,
                                            border_width=RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_WIDTH,
                                            corner_radius=RETURN_TO_MAIN_WINDOW_BUTTON_CORNER_RADIUS,
                                            border_color=RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_COLOR,
                                            command=self.return_to_main_window,
                                            state=ctk.DISABLED)
        self.__return_to_main_window_button.place(x = RETURN_TO_MAIN_WINDOW_BUTTON_X_POS,\
                                                y = RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS)
        self.__top.update_idletasks()



    def return_to_main_window(self):
        self.__top.destroy()
        self.__top.update()



    def call_the_downloader(self):
        # Start the download
        self.__downloader_engine.download_song(
            song_title = self.__widget_entries[DownloadSongTab.SONG_TITLE_INDEX].get(),
            artist_name = self.__widget_entries[DownloadSongTab.ARTIST_NAME_INDEX].get(),
            album_name = self.__widget_entries[DownloadSongTab.ALBUM_NAME_INDEX].get(),
            track_position_in_album = self.__widget_entries[DownloadSongTab.ALBUM_TRACK_POSITION_INDEX].get(),
            song_genre = self.__widget_entries[DownloadSongTab.SONG_GENRE_INDEX].get(),
            song_year = self.__widget_entries[DownloadSongTab.SONG_YEAR_INDEX].get(),
            youtube_url = self.__widget_entries[DownloadSongTab.SONG_YOUTUBE_URL_INDEX].get(),
            album_cover_image = self.__album_cover_image_file_full_path,
            return_to_main_window_button = self.__return_to_main_window_button,
            progress_bar = self.__progress_bar,
            download_status_label = self.__download_status_label,
            directory_where_song_will_be_saved_to = self.__directory_where_song_will_be_saved_to)




