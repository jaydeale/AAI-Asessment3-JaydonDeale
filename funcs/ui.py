import os
import textwrap
from .face import Face
from .audio import Audio
from .utils import clear_screen, draw_box, audio_input, face_input, menu_width, output_dir

#Screen class holding all extra display menu's
class Screen():
    #Facial Detection Menu
    @staticmethod
    def face_menu():
        clear_screen()#Clear screen before displaying menu
        title = "Camera & File Facial Detection Menu"#Set the window title
        options = ["[1] Detect from file.", "[2] Detect from camera.", "[b] Return to main menu."]#Set the options
        try:
            while True:#Main Face Menu Loop
                draw_box(title, options)
                choice = input("Option> ")#Get user input
                if choice == "1":#Check for choice 1
                    path = input("Enter file name> ")#Get file path
                    Face.file_input(face_input + path)#Call the func to detect faces from file
                elif choice == "2":#Check for choice 2
                    Face.camera_input()#Call the func to detect faces from camera
                elif choice.lower() == "b":#Check for choice to go back
                    break#Break the loop to return to main menu
                else:#Check for invalid input
                    print("Enter a valid choice.")#Print input Error
                    clear_screen()

        except Exception as e:
            print(f"Error: {e}")
        finally:
            clear_screen()
            return
    #Function to display Audio Menu    
    @staticmethod
    def audio_menu():
        try:
            clear_screen()#Clear screen before display
            title = "Audio Speech to text menu"#Set menu title
            options = ["[1] Transcribe from file.", "[2] Transcribe from microphone.", "[b] Return to main menu."]#Declare menu options
            while True:#Main audio menu loop
                draw_box(title, options)
                choice = input("Option> ")#Get user input
                if choice == "1":#Check for choice 1
                    path = input("Enter file name> ")#Get file path name
                    while True:#Loop for file transcription
                        if path and os.path.exists(audio_input + path):#check if file exists
                            output_name = input("Enter output name> ")#Set the output name
                            Audio.file_input(audio_input + path, output_name)#Function call to transcribe from file
                            break#Exit the loop
                        elif path.lower() == "q":#Check for quit input
                            break#Exit the loop
                        else:#Check for invalid input
                            print("Enter a valid file name.")#Notify the user
                elif choice == "2":#Check for choice 2
                    Audio.microphone_input()#Func call to transcribe from microphone
                elif choice.lower() == "b":#Check to return to main menu
                    break#Exit the loop
                else:#Check for invalid input
                    print("Enter a valid option.")#Notify user
        except Exception as e:
            print(f"Error: {e}")
        finally:
            clear_screen()
            return
