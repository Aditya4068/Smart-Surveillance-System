import customtkinter
import os
from PIL import Image, ImageTk

from in_out import in_out
from motion import noise
from Detection import numplate



from find_motion import find_motion
from identify import maincall


class App(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Smart Surveillance System")
        self.geometry("700x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #create list of saved persons
        myList = os.listdir('data/temp/')

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "detection.png")), size=(20, 20))
        self.image_icon_image2 = customtkinter.CTkImage(Image.open(os.path.join(image_path, "folder.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))
        self.history_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "history_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "history_light.png")), size=(20, 20))
        self.indoor_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "indoor_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "indoor_light.png")), size=(20, 20))
        self.car_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "car_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "car_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Control Panel", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Indoor",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.indoor_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Outdoor",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.car_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.frame_4_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="History",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.history_image, anchor="w", command=self.frame_4_button_event)
        self.frame_4_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.large_test_image)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.label = customtkinter.CTkLabel(master=self.home_frame, text="Welcome to the Smart Surveillance System!\n\nThe system provides the following modes:\n\n1. Indoor Surveillance: \n- Face Identification\n- Visitor Detection\n- Motion Detection\n- Stolen Item Detection\n\n2. Outdoor Surveillance: \n- License Plate Detection")
        self.label.grid(row=1, column=0, padx=20, pady=10)

        # self.home_frame_button_1 = customtkinter.CTkButton(self.home_frame, text="Stolen Item Detection", image=self.image_icon_image, command = find_motion, width=5)
        # self.home_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        # self.home_frame_button_2 = customtkinter.CTkButton(self.home_frame, text="License Plate Detection", image=self.image_icon_image, command = numplate, width=5)
        # self.home_frame_button_2.grid(row=2, column=0, padx=20, pady=10)
        # self.home_frame_button_3 = customtkinter.CTkButton(self.home_frame, text="Motion Detection", image=self.image_icon_image, command=noise, width=5)
        # self.home_frame_button_3.grid(row=3, column=0, padx=20, pady=10)
        # self.home_frame_button_4 = customtkinter.CTkButton(self.home_frame, text="Visitor Detection", image=self.image_icon_image, command=in_out, width=5)
        # self.home_frame_button_4.grid(row=4, column=0, padx=20, pady=10)
        # self.home_frame_button_5 = customtkinter.CTkButton(self.home_frame, text="Face ID", image=self.image_icon_image, command=maincall, width=5)
        # self.home_frame_button_5.grid(row=5, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)
        self.second_frame.rowconfigure(0, weight=0, pad=100)

        self.second_label = customtkinter.CTkLabel(master=self.second_frame, text=" \n ")
        self.second_label.grid(row=0, column=0, padx=20, pady=10)

        self.second_frame_button_1 = customtkinter.CTkButton(self.second_frame, text="Start Indoor Surveillance", image=self.image_icon_image, command = maincall, width=5, border_spacing=20, font=("TkDefaultFont", 20))
        self.second_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        #self.second_frame_button_1.config(height = 10, width = 10)

        self.second_frame_button_2 = customtkinter.CTkButton(self.second_frame, text="Start Stolen Item Detection", image=self.image_icon_image, command = find_motion, width=5, border_spacing=20, font=("TkDefaultFont", 20))
        self.second_frame_button_2.grid(row=2, column=0, padx=20, pady=20)


        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.rowconfigure(0, weight=0, pad=100)

        self.third_label = customtkinter.CTkLabel(master=self.third_frame, text=" \n ")
        self.third_label.grid(row=0, column=0, padx=20, pady=10)

        self.third_frame_button_1 = customtkinter.CTkButton(self.third_frame, text="Start Outdoor Surveillance", image=self.image_icon_image, command = numplate, width=5, border_spacing=20, font=("TkDefaultFont", 20))
        self.third_frame_button_1.grid(row=1, column=0, padx=20, pady=10)

        file = "NumberPlate.csv"

        self.third_frame_button_2 = customtkinter.CTkButton(self.third_frame, text="View License Plate Register", image=self.image_icon_image, command = lambda: os.startfile(file), width=5, border_spacing=20, font=("TkDefaultFont", 20))
        self.third_frame_button_2.grid(row=2, column=0, padx=20, pady=20)


        # create fourth frame
        self.fourth_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.fourth_frame.grid_columnconfigure(0, weight=1)
        self.fourth_frame.rowconfigure(0, weight=0)

        self.textbox = customtkinter.CTkTextbox(master=self.fourth_frame, height = 150, width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, padx=20, pady=30)
        self.textbox.insert("0.0", "List of Saved Persons:\n\n")
        for name in myList:
            savename = name.rstrip(".jpg")
            self.textbox.insert("end", f"{savename}\n")
        self.textbox.configure(state="disabled")

        visitor_path = "C:/Users/Aditya/Desktop/Smart Surveillance System March1/visitors/in"
        self.fourth_frame_button_1 = customtkinter.CTkButton(self.fourth_frame, text="View Visitor Entry History", image=self.image_icon_image2, command = lambda: os.startfile(visitor_path), width=5, border_spacing=12)
        self.fourth_frame_button_1.grid(row=1, column=0, padx=20, pady=10)
        
        intruder_path = "C:/Users/Aditya/Desktop/Smart Surveillance System March1/data/stored"
        self.fourth_frame_button_2 = customtkinter.CTkButton(self.fourth_frame, text="View Unknown Intruder History", image=self.image_icon_image2, command = lambda: os.startfile(intruder_path), width=5, border_spacing=12)
        self.fourth_frame_button_2.grid(row=2, column=0, padx=20, pady=10)

        stolen_path = "C:/Users/Aditya/Desktop/Smart Surveillance System March1/stolen"
        self.fourth_frame_button_3 = customtkinter.CTkButton(self.fourth_frame, text="View Stolen Item History", image=self.image_icon_image2, command = lambda: os.startfile(stolen_path), width=5, border_spacing=12)
        self.fourth_frame_button_3.grid(row=3, column=0, padx=20, pady=10)

        # select default frame
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")
        self.frame_4_button.configure(fg_color=("gray75", "gray25") if name == "frame_4" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()
        if name == "frame_4":
            self.fourth_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.fourth_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")
    
    def frame_4_button_event(self):
        self.select_frame_by_name("frame_4")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


#if __name__ == "__main__":
#    app = App()
#    app.mainloop()

def main_gui():
    app = App()
    app.mainloop()

