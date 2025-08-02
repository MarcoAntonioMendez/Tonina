import customtkinter as ctk
import PIL as pil
import subprocess
import logging
from DownloadEngine import mp3_downloader_engine

APPLICATION_NAME = "Toniná"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

FFMPEG_NOT_INSTALLED_MESSAGE = "Sorry, FFMPEG is not installed on your computer :( \
                                \nPlease close this window and install FFMPEG to use this software correctly."
FFMPEG_NOT_INSTALLED_MESSAGE_X_POS = 100
FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS = 10

TONINA_TITLE = "TONINÁ"
TONINA_TITLE_X_POS = 340
TONINA_TITLE_Y_POS = 5
TONINA_TITLE_TEXT_COLOR = "#eed6b7"


SONG_METADATA_SECTIONS_TEXTS_LIST = ["Título:","Artista:","Álbum:","Posición en Álbum:",\
                                    "Género:","Youtube URL:","Portada de Álbum:"]

LABELS_METADATA_SECTION_DIFF = 42
INITIAL_LABEL_SECTION_RECTANGLE_X_POS_1,INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_1 = 20, 90
INITIAL_LABEL_SECTION_RECTANGLE_X_POS_2,INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_2 = 250, 120
INITIAL_LABEL_SECTION_TEXT_X_POS = 30
INITIAL_LABEL_SECTION_TEXT_Y_POS = 92
LABEL_RECTANGLE_OUTLINE_COLOR = "#7636C3"

ENTRY_WIDGET_WIDTH = 685
INITIAL_ENTRY_SECTION_X_POS = 260

CHOOSE_ALBUM_COVER_TEXT = "Elegir Imagen"
CHOOSE_ALBUM_COVER_BACKGROUND_COLOR = "#59239a"
CHOOSE_ALBUM_COVER_BORDER_COLOR = "#998a76"
CHOOSE_ALBUM_COVER_BORDER_WIDTH = 3
CHOOSE_ALBUM_COVER_CORNER_RADIUS = 5


DOWNLOAD_SONG_BUTTON_TEXT = "Descargar Canción"
DOWNLOAD_SONG_BUTTON_BORDER_COLOR = "#c74716"
DOWNLOAD_SONG_BUTTON_SIZE = 35
DOWNLOAD_SONG_BUTTON_X_POS = 650
DOWNLOAD_SONG_BUTTON_Y_POS = 450


RESET_BUTTON_TEXT = "Reset"
RESET_BUTTON_BORDER_COLOR = "#1680c7"
RESET_BUTTON_X_POS = 20
RESET_BUTTON_Y_POS = 450


CHOOSE_ALBUM_COVER_FILE_DIALOG_TEXT = "Selecciona una imagen para la portadata del álbum"
CHOOSE_ALBUM_COVER_FILE_DIALOG_IMAGES_TEXT = "Imágenes"


PROGRESS_BAR_POP_UP_TITLE_TEXT = "Descargando..."
PROGRESS_BAR_POP_UP_WIDTH = 300
PROGRESS_BAR_POP_UP_HEIGHT = 533

METADATA_MISSING_TEXT = "Algún campo de la metadata \n\
no ha sido ingresado \n\
correctamente :(, por favor \n\
asegúrese de que toda la \n\
metadata (título de la \n\
canción, artista, portada \n\
del álbum etc.) fue ingresada \n\
en su totalidad."
METADATA_MISSING_X_POS = 10
METADATA_MISSING_Y_POS = 10


RETURN_TO_MAIN_WINDOW_BUTTON_TEXT = "Volver a la Pantalla Principal"
RETURN_TO_MAIN_WINDOW_BUTTON_X_POS = 17
RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS = 480

class Downloader:
    def __init__(self):
        # Initializing the root to contain the main frame of the GUI application
        self.__root = ctk.CTk()

        # Initializing canvas
        self.__canvas = ctk.CTkCanvas(self.__root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
        self.__canvas.pack(fill="both", expand=True)

        # Initializing list of entry widgets
        self.__widget_entries = []

        # Initializing string to hold album cover image file path
        self.__album_cover_image_file_full_path = ""

        # Initializing the downloader_engine
        self.__downloader_engine = mp3_downloader_engine.Mp3DownloaderEngine()


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


        # Setting the background image of the program
        background_image = pil.Image.open("Images/background.png").convert("RGBA")
        background = pil.ImageTk.PhotoImage(background_image)
        self.__canvas.create_image(0, 0, anchor="nw", image=background)


        # Checking if FFMPEG is installed in user's computer
        is_ffmpeg_installed = True
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, check=True)
        except FileNotFoundError:
            logging.warning("ffmpeg is not installed in this computer, please install ffmpeg.")
            self.__canvas.create_text(FFMPEG_NOT_INSTALLED_MESSAGE_X_POS,\
                                    FFMPEG_NOT_INSTALLED_MESSAGE_Y_POS, anchor="nw",\
                                    text=FFMPEG_NOT_INSTALLED_MESSAGE, font=('Times New Roman',25),\
                                    fill="#eed6b7")
            is_ffmpeg_installed = False


        # If FFMPEG is installed, then the normal UI is created
        if(is_ffmpeg_installed):
            self.set_user_interface()

        # Starting the windows
        self.__root.mainloop()



    def set_user_interface(self):
        self.__canvas.create_text(TONINA_TITLE_X_POS,TONINA_TITLE_Y_POS, anchor="nw",\
                                    text=TONINA_TITLE, font=('Times New Roman',60),\
                                    fill=TONINA_TITLE_TEXT_COLOR)

        # Traversing through the list containing the song metadata text.
        # In each turn of the loop, the x and y coordinates of the visual elements are calcualted and set.
        for index in range(len(SONG_METADATA_SECTIONS_TEXTS_LIST)):
            #Painting rectangles to contain labels of song metadata
            diff = index*LABELS_METADATA_SECTION_DIFF
            x_pos_1 = INITIAL_LABEL_SECTION_RECTANGLE_X_POS_1
            y_pos_1 = INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_1+diff
            x_pos_2 = INITIAL_LABEL_SECTION_RECTANGLE_X_POS_2
            y_pos_2 = INITIAL_LABEL_SECTION_RECTANGLE_Y_POS_2+diff
            self.__canvas.create_rectangle(x_pos_1,y_pos_1,x_pos_2,y_pos_2,\
                                            outline=LABEL_RECTANGLE_OUTLINE_COLOR, width=2)


            # Painting the song metadata text
            x_pos = INITIAL_LABEL_SECTION_TEXT_X_POS
            y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff
            text = SONG_METADATA_SECTIONS_TEXTS_LIST[index]
            self.__canvas.create_text(x_pos,y_pos, anchor="nw",text=text,\
                                    font=('Times New Roman',20),fill=TONINA_TITLE_TEXT_COLOR)


            # Setting the textboxes and the button to choose album cover
            if(index != (len(SONG_METADATA_SECTIONS_TEXTS_LIST)-1) ):
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff
                entry_widget = ctk.CTkEntry(self.__root,font=('Times New Roman',20),width=ENTRY_WIDGET_WIDTH)
                entry_widget.place(x = x_pos, y = y_pos)
                self.__widget_entries.append(entry_widget)
            else:
                x_pos = INITIAL_ENTRY_SECTION_X_POS
                y_pos = INITIAL_LABEL_SECTION_TEXT_Y_POS+diff
                self.__choose_album_cover_button = ctk.CTkButton(self.__root,\
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
        self.__download_song_button = ctk.CTkButton(self.__root,\
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
        self.__reset_button = ctk.CTkButton(self.__root,\
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



    def reset_all_fields(self):
        # Clearing all entries and the album cover image file
        self.__album_cover_image_file_full_path = ""
        self.__choose_album_cover_button.configure(text=CHOOSE_ALBUM_COVER_TEXT)

        for entry in self.__widget_entries:
            entry.delete(0, ctk.END)




    def check_if_everything_is_good_to_download_a_song(self):
        # Checking all entries and album cover button
        all_metadata_set = self.has_all_metadta_been_set()


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
            self.download_song()
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










    def inform_user_some_metadata_is_missing(self):
        self.__progress_bar_canvas.create_text(METADATA_MISSING_X_POS,\
                                    METADATA_MISSING_Y_POS, anchor="nw",\
                                    text=METADATA_MISSING_TEXT, font=('Times New Roman',24),\
                                    fill=TONINA_TITLE_TEXT_COLOR)


        # Creating reset button
        reset_icon = ctk.CTkImage(pil.Image.open("Images/reset_icon.png"),\
                                    size=(DOWNLOAD_SONG_BUTTON_SIZE, DOWNLOAD_SONG_BUTTON_SIZE))
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













    def download_song(self):
        self.__downloader_engine.download_song()
