import cv2
import mediapipe as mp

import time
import draw
from homeController import HomeController

cap = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

global_result = None
global_result_dict = {
    "Closed_Fist" : 0,
    "Open_Palm" : 0,
    "Pointing_Up" : 0,
    "Thumb_Down" : 0,
    "Thumb_Up" : 0,
    "Victory" : 0,
    "Unknown" : 0,
    "ILoveYou" : 0,
    }
global_current_gesture = ''
global_current_gesture_count = 0


global_img = None
hc = None
def control():
    global global_current_gesture, global_current_gesture_count
    match global_current_gesture:
        case "Closed_Fist":
            hc.clickTvOff()
        case "Open_Palm":
            hc.clickTvOn()
        case "Pointing_Up":
            hc.clickRegular()
        case "Thumb_Down":
            hc.clickTvDown()
        case "Thumb_Up":
            hc.clickTvUp()
        case "Victory":
            hc.clickThatTime()
        case "Unknown":
            pass
        case "ILoveYou":
            pass
    global_current_gesture_count = 0

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global global_img, global_result, global_current_gesture_count, global_current_gesture

    global_result = result
    global_img = draw.draw_landmarks_on_image(output_image.numpy_view(),result)

    
    pass
    #print('gesture recognition result: {}'.format(result))

if __name__ == "__main__":
    hc = HomeController()
    time.sleep(5)
    hc.setList()

    options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path='model/gesture_recognizer.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        min_hand_presence_confidence = 0.005,
        min_hand_detection_confidence = 0.005,
        min_tracking_confidence = 0.005,
        result_callback=print_result)


    prev = 0
    capturing = True
    timestamp = 0
    with GestureRecognizer.create_from_options(options) as recognizer:


        while capturing:

            time_elapsed = time.time() - prev
            ret, original_image = cap.read()
            height, width = original_image.shape[:2]
            
            image = original_image[height//2:,width//2:]

            cv2.imwrite("frame.png", image) 
            image = cv2.imread("frame.png")

            
            if not ret:
                print("Ignoring empty frame")
                break

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            recognition_result = recognizer.recognize_async(mp_image, timestamp)
            timestamp = timestamp + 1


            if global_result is not None:
                original_image[height//2:,width//2:] = global_img


                cv2.imshow('MediaPipe Hands',original_image )
                

                if( len(global_result.gestures) > 0):


                    top_gesture = global_result.gestures[0][0].category_name
                    if (global_current_gesture == top_gesture):
                        print(global_current_gesture_count)
                        global_current_gesture_count +=1
                    else:
                        global_current_gesture_count = 0
                        global_current_gesture = top_gesture

                    if global_current_gesture_count > 30:
                        control()



        
            if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
                break
            


    cap.release()

