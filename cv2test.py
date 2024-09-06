import cv2
import time


# Initialize the camera (0 is the default camera)
cap = cv2.VideoCapture(0)
time.sleep(3)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Loop to continuously get frames from the camera
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # If frame is read correctly, ret is True
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break
    
    height, width = frame.shape[:2]

    frame = frame[height//2:,width//2:]
    
    # Display the resulting frame
    cv2.imshow('Camera Feed', frame)
    
    # Break the loop when 'q' is pressed
    if cv2.waitKey(5) & 0xFF == 27:  # Press 'ESC' to exit
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
