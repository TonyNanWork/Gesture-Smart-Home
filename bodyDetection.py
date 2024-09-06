import cv2
import mediapipe as mp

import time
import draw
from homeController import HomeController

cap = cv2.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
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

def print_pose_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global global_img, global_result, global_current_gesture_count, global_current_gesture

    global_result = result
    global_img = draw.draw_landmarks_on_pose_image(output_image.numpy_view(),result)

    
    pass
    #print('gesture recognition result: {}'.format(result))

if __name__ == "__main__":
    #hc = HomeController()
    time.sleep(5)
    #hc.setList()

    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path='model/pose_landmarker_heavy.task'),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_pose_result)


    prev = 0
    capturing = True
    timestamp = 0
    with PoseLandmarker.create_from_options(options) as recognizer:


        while capturing:

            time_elapsed = time.time() - prev
            ret, image = cap.read()

            

            if not ret:
                print("Ignoring empty frame")
                break

            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
            recognition_result = recognizer.detect_async(mp_image, timestamp)
            timestamp = timestamp + 1


            if global_result is not None:

                if global_result.pose_landmarks:
                    print(global_result.pose_landmarks)
                    landmark = global_result.pose_landmarks[14]
                    x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                    # Define a simple square bounding box around the wrist for demonstration
                    box_size = 100  # Adjust based on the desired size
                    cropped_hand = image[max(0, y-box_size):min(image.shape[0], y+box_size), max(0, x-box_size):min(image.shape[1], x+box_size)]
                    global_img = cropped_hand
                    print (global_result.pos)
                    
                cv2.imshow('MediaPipe Hands',global_img )
                


            if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
                break
            


    cap.release()

