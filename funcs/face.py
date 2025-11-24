import cv2
import os
from deepface import DeepFace
from .utils import clear_screen, draw_box

#Static class holding all facial detection functions
class Face:
    #Static function to detect face from file input
    @staticmethod
    def file_input(path):
        try:
            if not os.path.isfile(path):#Check if file exists
                print("File not found")
                return
            img = cv2.imread(path)#Read file path and image
            if img is None:#If no image return back
                print("Could not load image")
                return
            #Store all detections in a variable
            detections = DeepFace.extract_faces(img_path=path, detector_backend='opencv', enforce_detection=False)
            #Declare and create points around faces
            for d in detections:
                fa = d["facial_area"]#List storing detection values
                x = fa["x"]#x Axis
                y = fa["y"]#Y Axis
                w = fa["w"]#Width
                h = fa["h"]#Height
                cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)#Draw Rectangle around face with green color
            print(f"Found {len(detections)} face(s). Press any key to close image") #Inform user of how many detections
            cv2.imshow("Faces", img)#Display image and detections
            clear_screen()#Clear screen and return to menu
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cv2.waitKey(0)#Wait for key input to quit
            cv2.destroyAllWindows()#Exit all windows
    #Static function to detected faces from a camera
    @staticmethod
    def camera_input():
        try:
            capture = cv2.VideoCapture(0, cv2.CAP_V4L2)#Initialize video capture
            if not capture.isOpened():#Check if camera is opened
                print("Could not open camera")
                return
            while True:#Loop for capturing camera
                ret, frame = capture.read()#Read the camera
                if not ret:#If no data
                    print("Failed to read frame")
                    break
                #Store live detections in a variable
                detections = DeepFace.extract_faces(img_path= frame, detector_backend='opencv', enforce_detection=False)
                #Declare and create points around faces
                for d in detections:
                    fa = d["facial_area"]#List containing detection values
                    x = fa["x"]#X Axis
                    y = fa["y"]#Y Axis
                    w = fa["w"]#Width
                    h = fa['h']#Height
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)#Draw rectangle around the face/s

                cv2.imshow("Camera", frame)#Display camera with detections

                if cv2.waitKey(1) & 0xFF == ord('q'):#Check statement to see if q has been pressed
                    break
            capture.release()#Deinitialize camera
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cv2.destroyAllWindows()#Close the window
            clear_screen()#Clear screen and return to menu

