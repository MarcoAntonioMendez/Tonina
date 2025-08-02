import customtkinter as ctk
import PIL as pil
import subprocess
import logging

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

class Downloader:
    def __init__(self):
        # Initializing the root to contain the main frame of the GUI application
        self.__root = ctk.CTk()

        # Initializing canvas
        self.__canvas = ctk.CTkCanvas(self.__root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0)
        self.__canvas.pack(fill="both", expand=True)

        # Initializing list of entry widgets
        self.__widget_entries = []


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
                                                                border_color=CHOOSE_ALBUM_COVER_BORDER_COLOR)
                self.__choose_album_cover_button.place(x = x_pos, y = y_pos)





