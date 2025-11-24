import os
import textwrap

output_dir = "./output"
face_input = "./data/faces"
audio_input = "./data/audio"
menu_width = 30

def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')#Check if windows or linux

def draw_box(title, options):
    try:
        title_box = textwrap.wrap(title, width=menu_width)#Create the title box
        print("\n╔" + "═"*menu_width + "╗")#Print top line
        for line in title_box:#For loop to get all text for the title box
            print("║" + line.center(menu_width) + "║")#Print items in the center of the box
        print("╚" + "═"*menu_width + "╝")#Print bottom of title box

        for entry in options:#Loop through option
            wrapped_lines = textwrap.wrap(entry, width=menu_width)#Wrap every entry in options
            for line in wrapped_lines:#For loop to display all options
                print("║" + line.center(menu_width) + "║")#Print options in the center of the box
        print("╚" + "═"*menu_width + "╝")#Print bottom line of box
    except:
        print("Could not draw menu.")
        clear_screen()
        return
