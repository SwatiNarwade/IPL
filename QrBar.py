import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Open the camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Adjust resolution width
cap.set(4, 720)   # Adjust resolution height

# Load authorized data from file
with open('myDataFile.txt', encoding='utf-8') as f:
    myDataList = [line.strip().lower() for line in f.readlines()]  # Strip and convert to lowercase

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image.")
        break

    # Convert to grayscale for better detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Increase contrast and sharpness
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)

    # Decode QR codes and barcodes
    for barcode in decode(gray):
        myData = barcode.data.decode('utf-8').strip().lower()  # Strip and lowercase
        print(f"Detected: {myData}")

        if myData in myDataList:
            myOutput = 'Authorized'
            myColor = (0, 255, 0)  # Green for authorized
        else:
            myOutput = 'Un-Authorized'
            myColor = (0, 0, 255)  # Red for unauthorized

        # Draw a polygon around the barcode
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, myColor, 3)

        # Display text near the QR code
        rect = barcode.rect
        cv2.putText(img, myOutput, (rect.left, rect.top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, myColor, 2)

    # Show the result
    cv2.imshow('Result', img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release camera and close windows
cap.release()
cv2.destroyAllWindows()
