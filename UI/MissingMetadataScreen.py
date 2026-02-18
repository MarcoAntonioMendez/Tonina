import customtkinter as ctk


# General Constants
METADATA_MISSING_SCREEN_BACKGROUND_COLOR = "#360185"


MISSING_METADATA_SCREEN_TITLE_TEXT = "Error: Missing metadata."
MISSING_METADATA_SCREEN_WIDTH = 300
MISSING_METADATA_SCREEN_HEIGHT = 533


RETURN_TO_MAIN_WINDOW_BUTTON_TEXT = "Go Back to the Main Screen"
RETURN_TO_MAIN_WINDOW_BUTTON_X_POS = 17
RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS = 480
RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_WIDTH = 3
RETURN_TO_MAIN_WINDOW_BUTTON_CORNER_RADIUS = 5
RETURN_TO_MAIN_WINDOW_BUTTON_TEXT_COLOR = "#eed6b7"
RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_COLOR = "#1680c7"
RETURN_TO_MAIN_WINDOW_BUTTON_DISABLED_BACKGROUND_COLOR = "#0f2933"
RETURN_TO_MAIN_WINDOW_BUTTON_BACKGROUND_COLOR = "#59239a"


METADATA_MISSING_TEXT_COLOR = "#eed6b7"
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

class MissingMetadataScreen:
    def __init__(self, root):
        self.__root = root


    def inform_user_some_metadata_is_missing(self):
        # Creating the frame
        self.__top = ctk.CTkToplevel(fg_color=METADATA_MISSING_SCREEN_BACKGROUND_COLOR)
        self.__top.title(MISSING_METADATA_SCREEN_TITLE_TEXT)
        self.__top.minsize(MISSING_METADATA_SCREEN_WIDTH,MISSING_METADATA_SCREEN_HEIGHT)
        self.__top.maxsize(MISSING_METADATA_SCREEN_WIDTH,MISSING_METADATA_SCREEN_HEIGHT)
        # Setting the size of the frame
        screen_width = self.__top.winfo_screenwidth()
        screen_height = self.__top.winfo_screenheight()
        x_pos = int((screen_width - MISSING_METADATA_SCREEN_WIDTH)/2)
        y_pos = int((screen_height - MISSING_METADATA_SCREEN_HEIGHT)/2)
        self.__top.geometry(f"{MISSING_METADATA_SCREEN_WIDTH}x{MISSING_METADATA_SCREEN_HEIGHT}+{x_pos}+{y_pos}")


        # Creating the label text to inform the user some metadata is missing
        self.__missing_metadata_message_label = ctk.CTkLabel(self.__top,
                                            font=('Times New Roman',24),
                                            text=METADATA_MISSING_TEXT,
                                            anchor="nw",
                                            text_color=RETURN_TO_MAIN_WINDOW_BUTTON_TEXT_COLOR)
        self.__missing_metadata_message_label.place(x=METADATA_MISSING_X_POS, y=METADATA_MISSING_Y_POS)


        # Creating the return to the main window button
        self.__return_to_main_window_button = ctk.CTkButton(self.__top,
                                            font=('Times New Roman',21,"italic"),
                                            text=RETURN_TO_MAIN_WINDOW_BUTTON_TEXT,
                                            fg_color=RETURN_TO_MAIN_WINDOW_BUTTON_BACKGROUND_COLOR,
                                            text_color=RETURN_TO_MAIN_WINDOW_BUTTON_TEXT_COLOR,
                                            border_width=RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_WIDTH,
                                            corner_radius=RETURN_TO_MAIN_WINDOW_BUTTON_CORNER_RADIUS,
                                            border_color=RETURN_TO_MAIN_WINDOW_BUTTON_BORDER_COLOR,
                                            command=self.return_to_main_window)
        self.__return_to_main_window_button.place(x = RETURN_TO_MAIN_WINDOW_BUTTON_X_POS,
                                                y = RETURN_TO_MAIN_WINDOW_BUTTON_Y_POS)


        # Disables the original root and only the MissingMetadataScreen becomes active
        self.__top.focus()
        self.__top.transient(self.__root)
        self.__top.grab_set()
        self.__top.wait_window(self.__top)



    def return_to_main_window(self):
        self.__top.destroy()
        self.__top.update()






