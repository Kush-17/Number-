# -*- coding: utf-8 -*-
"""combined_script.py"""

import cv2
import easyocr

harcascade = "/haarcascade_russian_plate_number.xml"
reader = easyocr.Reader(['en'])

data = {
    'Andhra Pradesh': 'AP',
    'Arunachal Pradesh': 'AR',
    'Assam': 'AS',
    'Bihar': 'BR',
    'Chhattisgarh': 'CG',
    'Goa': 'GA',
    'Gujarat': 'GJ',
    'Haryana': 'HR',
    'Himachal Pradesh': 'HP',
    'Jammu and Kashmir': 'JK',
    'Jharkhand': 'JH',
    'Karnataka': 'KA',
    'Kerala': 'KL',
    'Madhya Pradesh': 'MP',
    'Maharashtra': 'MH',
    'Manipur': 'MN',
    'Meghalaya': 'ML',
    'Mizoram': 'MZ',
    'Nagaland': 'NL',
    'Orissa': 'OR',
    'Punjab': 'PB',
    'Rajasthan': 'RJ',
    'Sikkim': 'SK',
    'Tamil Nadu': 'TN',
    'Tripura': 'TR',
    'Uttarakhand': 'UK',
    'Uttar Pradesh': 'UP',
    'West Bengal': 'WB',
    'Telangana': 'TS',
    'Andaman and Nicobar Islands': 'AN',
    'Chandigarh': 'CH',
    'Dadra and Nagar Haveli': 'DH',
    'Daman and Diu': 'DD',
    'Delhi': 'DL',
    'Lakshadweep': 'LD',
    'Pondicherry': 'PY'
}

def process_image(image):
    # Process the image to detect number plates
    plate_cascade = cv2.CascadeClassifier(harcascade)

    # if plate_cascade.empty():
    #     print("Error: Cascade classifier not loaded.")
    #     return image

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    for (x, y, w, h) in plates:
        area = w * h

        if area > min_area:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(image, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)

            img_roi = image[y: y + h, x:x + w]
            cv2.imshow("ROI", img_roi)

            # Perform OCR on the detected number plate
            output = reader.readtext(img_roi)

            # Extract the abbreviation
            if output:
                st_name = output[0][1][:2]

                # Get the state/UT name
                st_name1 = get_state_name(st_name)
                print("State/UT Name for Abbreviation", st_name, ":", st_name1)

                # Save the scanned image
                cv2.imwrite("scaned_img_" + str(count) + ".jpg", img_roi)
                count += 1

    return image


# Function to get state/UT name based on abbreviation
def get_state_name(abbreviation):
    abbreviation = abbreviation.upper()  # Convert to uppercase
    if abbreviation in data.values():
        for state, abbr in data.items():
            if abbr == abbreviation:
                return state
    return 'Abbreviation not found'

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    cap.set(3, 640)  # width
    cap.set(4, 480)  # height

    min_area = 500
    count = 0

    while True:
        success, img = cap.read()
        if not success:
            print("Error: Failed to read frame from the camera.")
        else:
            print("Capture Success")

        processed_img = process_image(img)
        cv2.imshow("Processed Image", processed_img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed
            break

 

