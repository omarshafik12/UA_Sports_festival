import cv2 as cv

# Set the camera index (0 for built-in, 1 for external webcam)
# The best backend API was CAP_MSMF which it printed as 1400.0, that's what it was doing searching through all the APIs till it saw that MSMF was teh best and finally used that.
# https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html#ga023786be1ee68a9105bf2e48c700294d
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
backend_id = cap.get(cv.CAP_PROP_BACKEND)
print(f"Backend ID: {backend_id}")


while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    # Draw rectangle on the frame
    img = cv.rectangle(frame, (100, 100), (200, 200), (128, 128, 128), 5)

    # Display the frame
    cv.imshow('Webcam Test', img)  # Display the modified frame with the rectangle
    cv.waitKey(1)

cap.release()
cv.destroyAllWindows()

#please stop running code as there is no exit funtion
