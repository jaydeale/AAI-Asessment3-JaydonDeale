from funcs.ui import Screen
from funcs.utils import clear_screen, draw_box
from funcs.startup import check_and_install_packages

#Main function
def main():
    try:
        clear_screen()#Clear screen
        title = "MultiModel AI Detection"#Set title
        options = ["[1] Face Menu.", "[2] Audio Menu.", "[q] Quit"]#Set options
        while True:#Main loop for main menu
            draw_box(title, options)
            choice = input("Option> ")#Get user input
            if choice == "1":#Check for first option
                Screen.face_menu()#Func call to go to face menu
            elif choice == "2":#Check for second option
                Screen.audio_menu()#Func call to go to audio menu
            elif choice.lower() == "q":#Check for third menu
                print("Goodbye")#Notify user its closing
                exit()#Quit the program
            else:#Check for invalid Input
                print("Enter a valid option.")
    except Exception as e:
        print(f"Error: {e}")
#Startup init
if __name__ == "__main__":
    #Print disclaimer to help users
    print("########################################")
    print("#              DISCLAIMER              #")
    print("#   PLEASE ENSURE ALL INPUT FILES ARE  #")
    print("#     LOCATED IN /data AND IN THEIR    #")
    print("#           RESPECTIVE FOLDERS         #")
    print("########################################")
    try:
        #Start import Initialization
        check_and_install_packages()
        #Start main loop
        main()
    except Exception as e:
        print(f"Error: {e}")
