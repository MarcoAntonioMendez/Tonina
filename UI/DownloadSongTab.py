import customtkinter as ctk
import PIL as pil
import subprocess
import logging
import os
import threading
from UI import downloader
from DownloadEngine import mp3_downloader_engine


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


PROGRESS_BAR_POP_UP_TITLE_TEXT = "Downloading..."
PROGRESS_BAR_POP_UP_WIDTH = 300
PROGRESS_BAR_POP_UP_HEIGHT = 533

METADATA_MISSING_TEXT = "Some metadata field \n\
was not entered \n\
correctly :(, please \n\
make sure that all of the \n\
metadata (song's title, \n\
artist name, cover album, \n\
etc.) was entered \n\
in its totality."
METADATA_MISSING_X_POS = 10
METADATA_MISSING_Y_POS = 10


RETURN_TO_MAIN_WINDOW_BUTTON_TEXT = "Go Back to the Main Screen"
RETURN_TO_MAIN_WINDOW_BUTTON_X_POS = 17
RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS = 480
RETURN_TO_MAIN_WINDOW_BUTTON_DISABLED_BACKGROUND_COLOR = "#0f2933"


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

        # Initializing the downloader_engine
        self.__downloader_engine = mp3_downloader_engine.Mp3DownloaderEngine()

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


        # Creating a progress bar pop up
        self.__top = ctk.CTkToplevel()
        self.__top.title(PROGRESS_BAR_POP_UP_TITLE_TEXT)
        self.__top.minsize(PROGRESS_BAR_POP_UP_WIDTH,PROGRESS_BAR_POP_UP_HEIGHT)
        self.__top.maxsize(PROGRESS_BAR_POP_UP_WIDTH,PROGRESS_BAR_POP_UP_HEIGHT)
        # Setting the size of the progress bar pop up
        screen_width = self.__top.winfo_screenwidth()
        screen_height = self.__top.winfo_screenheight()
        x_pos = int((screen_width - PROGRESS_BAR_POP_UP_WIDTH)/2)
        y_pos = int((screen_height - PROGRESS_BAR_POP_UP_HEIGHT)/2)
        self.__top.geometry(f"{PROGRESS_BAR_POP_UP_WIDTH}x{PROGRESS_BAR_POP_UP_HEIGHT}+{x_pos}+{y_pos}")



        #Creating the progress bar pop up canvas, so elements can be rendered in there.
        # Setting the background of the progress bar pop up
        self.__progress_bar_canvas = ctk.CTkCanvas(self.__top,\
                                                width=PROGRESS_BAR_POP_UP_WIDTH,\
                                                height=PROGRESS_BAR_POP_UP_HEIGHT,\
                                                highlightthickness=0)
        self.__progress_bar_canvas.pack(fill="both", expand=True)
        background = pil.ImageTk.PhotoImage(pil.Image.open("Images/progress_bar_pop_up_background.png").convert("RGBA"))
        self.__progress_bar_canvas.create_image(0, 0, anchor="nw", image=background)




        # If the user entered the metadata correctly, then the song will start to be downloaded.
        # If some of the metadata is missing, then the software will show a warning message
        if(all_metadata_set):
            # All metadata is fine, starting to download
            # Setting the thread where the download will run on
            self.set_download_progress_interface()
            download_thread = threading.Thread(target=self.download_song)
            download_thread.start()
        else:
            # Some metadata is missing, inform the user of the issue
            self.inform_user_some_metadata_is_missing()



        # Disables the original root and only progress bar pop up stays active
        self.__top.focus()
        self.__top.transient(self.__root)
        self.__top.grab_set()
        self.__top.wait_window(self.__top)



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



    def inform_user_some_metadata_is_missing(self):
        self.__progress_bar_canvas.create_text(METADATA_MISSING_X_POS,\
                                    METADATA_MISSING_Y_POS, anchor="nw",\
                                    text=METADATA_MISSING_TEXT, font=('Times New Roman',24),\
                                    fill=TONINA_TITLE_TEXT_COLOR)


        # Creating the return to the main window button
        self.__return_to_main_window_button = ctk.CTkButton(self.__top,\
                                            font=('Times New Roman',21,"italic"),\
                                            text=RETURN_TO_MAIN_WINDOW_BUTTON_TEXT,\
                                            fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                                            text_color=TONINA_TITLE_TEXT_COLOR,\
                                            border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,\
                                            corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,\
                                            border_color=RESET_BUTTON_BORDER_COLOR,\
                                            command=self.return_to_main_window)
        self.__return_to_main_window_button.place(x = RETURN_TO_MAIN_WINDOW_BUTTON_X_POS,\
                                                y = RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS)



    def return_to_main_window(self):
        self.__top.destroy()
        self.__top.update()



    def set_download_progress_interface(self):
        # Adding graphical elements to inform the user the status of the download
        # Adding the album cover of the song being downloaded
        pil_image = pil.Image.open(self.__album_cover_image_file_full_path)
        ctk_image = ctk.CTkImage(light_image=pil_image,dark_image=pil_image,\
                                size=(ALBUM_COVER_IMAGE_FOR_STATUS_SIZE, ALBUM_COVER_IMAGE_FOR_STATUS_SIZE))
        album_cover_image_for_status = ctk.CTkLabel(self.__top, image=ctk_image, text="")
        album_cover_image_for_status.place(x = ALBUM_COVER_IMAGE_FOR_STATUS_X_POS,\
                                            y = ALBUM_COVER_IMAGE_FOR_STATUS_Y_POS)

        # Adding the name of te song being downloaded
        song_title_for_status = ctk.CTkLabel(self.__top,text=self.__widget_entries[SONG_TITLE_INDEX].get(),\
                            font=('Times New Roman',19),wraplength=STATUS_LABELS_WRAP_LENGTH,\
                            fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                            text_color=TONINA_TITLE_TEXT_COLOR)
        song_title_for_status.place(x = SONG_TITLE_FOR_STATUS_X_POS, y = SONG_TITLE_FOR_STATUS_Y_POS)
        self.__top.update_idletasks()

        # Adding the name of te song being downloaded
        song_artist_for_status = ctk.CTkLabel(self.__top,text=self.__widget_entries[ARTIST_NAME_INDEX].get(),\
                            font=('Times New Roman',19),wraplength=STATUS_LABELS_WRAP_LENGTH,\
                            fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                            text_color=TONINA_TITLE_TEXT_COLOR)
        song_artist_for_status.place(x = SONG_TITLE_FOR_STATUS_X_POS,\
            y = SONG_TITLE_FOR_STATUS_Y_POS + song_title_for_status.winfo_height()\
            + song_artist_for_status.winfo_height() + STATUS_LABELS_SPACE_BETWEEN)
        self.__top.update_idletasks()


        # Adding the progress bar
        self.__progress_bar = ctk.CTkProgressBar(self.__top,orientation="horizontal",\
                                                determinate_speed=6.2,width=250,height=20,\
                                                progress_color="green")
        self.__progress_bar.set(0)
        self.__progress_bar.place(x = SONG_TITLE_FOR_STATUS_X_POS,\
            y = SONG_TITLE_FOR_STATUS_Y_POS + song_title_for_status.winfo_height()\
            + song_artist_for_status.winfo_height() + PROGRESS_BAR_SPACE_BETWEEN)
        self.__top.update_idletasks()



        # Adding the label that will hold the specif stage in which the download is being carried on.
        self.__download_status_label = ctk.CTkLabel(self.__top,text=DOWNLOAD_STARTING_STATUS,\
                            font=('Times New Roman',16),wraplength=STATUS_LABELS_WRAP_LENGTH,\
                            fg_color=CHOOSE_ALBUM_COVER_BACKGROUND_COLOR,\
                            text_color=TONINA_TITLE_TEXT_COLOR)
        self.__download_status_label.place(x = SONG_TITLE_FOR_STATUS_X_POS,\
            y = SONG_TITLE_FOR_STATUS_Y_POS + song_title_for_status.winfo_height()\
            + song_artist_for_status.winfo_height() + self.__download_status_label.winfo_height()\
            + self.__progress_bar.winfo_height() + PROGRESS_BAR_SPACE_BETWEEN\
            + DOWNLOAD_STATUS_SPACE_BETWEEN)
        self.__top.update_idletasks()



        # Creating return to the main window button
        self.__return_to_main_window_button = ctk.CTkButton(self.__top,\
                                            font=('Times New Roman',21,"italic"),\
                                            text=RETURN_TO_MAIN_WINDOW_BUTTON_TEXT,\
                                            fg_color=RETURN_TO_MAIN_WINDOW_BUTTON_DISABLED_BACKGROUND_COLOR,\
                                            text_color=TONINA_TITLE_TEXT_COLOR,\
                                            border_width=CHOOSE_ALBUM_COVER_BORDER_WIDTH,\
                                            corner_radius=CHOOSE_ALBUM_COVER_CORNER_RADIUS,\
                                            border_color=RESET_BUTTON_BORDER_COLOR,\
                                            command=self.return_to_main_window,\
                                            state=ctk.DISABLED)
        self.__return_to_main_window_button.place(x = RETURN_TO_MAIN_WINDOW_BUTTON_X_POS,\
                                                y = RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS)
        self.__top.update_idletasks()



    def download_song(self):
        # Starting the download process
        self.__downloader_engine.download_song(\
            song_title = self.__widget_entries[SONG_TITLE_INDEX].get(),\
            artist_name = self.__widget_entries[ARTIST_NAME_INDEX].get(),\
            album_name = self.__widget_entries[ALBUM_NAME_INDEX].get(),\
            track_position_in_album = self.__widget_entries[ALBUM_TRACK_POSITION_INDEX].get(),\
            song_genre = self.__widget_entries[SONG_GENRE_INDEX].get(),\
            song_year = self.__widget_entries[SONG_YEAR_INDEX].get(),\
            youtube_url = self.__widget_entries[SONG_YOUTUBE_URL_INDEX].get(),\
            album_cover_image = self.__album_cover_image_file_full_path,\
            return_to_main_window_button = self.__return_to_main_window_button,\
            progress_bar = self.__progress_bar,\
            download_status_label = self.__download_status_label)