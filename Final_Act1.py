# This program allows you to take 4 photos of yourself and it outputs the 4 photos in a frame just like the ones in photobooths. 
# Start
# Click space to capture photo 1, 2, 3, 4
# Output Results
# Click s to save and d to discard
# Click y if you wanna retake and n if you wanna exit the program
# Stop

import cv2 # I used this to access the camera so I can use the photos taken for the  photobooth
import numpy as np # I used this to stack the photos 
from PIL import Image, ImageDraw, ImageFont # I imported this so the font on the photobooth looks pretty hihi...
while True:
    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Photobooth")

    # This section provides the background of our photobooth
    photos = []
    count = 0 
    background_col = (244,194,194)
    border = 100

    # This section provides the font layout of the photobooth frame the the user is gonna use when they take photos
    frame_text = 'Our Memories'
    font_type = "Lobster-Regular.ttf"
    font_size = 50

    try:
        font = ImageFont.truetype("Lobster-Regular.ttf", font_size)
    except IOError:
        print(f"Font file not found. Falling back to default font.")
        font = ImageFont.load_default(font_size)


    # This section allows you or me to take photos or escape the program. If you hit space you will take the photo 
    # And if you hit escape, you will exit the program
    while count < 4 :
        ret, frame= cam.read()

        if not ret:
            print("Failed to grab frame")
        cv2.imshow("Photobooth", frame)

        k = cv2.waitKey(1)

        if k%256==27:
            print("Escape hit")
            break

        elif k%256 ==32:
            image = "opencv_frame_{}.png".format(count)
            photos.append(frame)
            print(f"Photo {count + 1} Taken")
            count +=1

    # This section stacks the photos into the format I want them to be stacked. 
    if len(photos) == 4:

        top = np.hstack((photos[0], photos[1])) #h stack horizontal po
        bottom = np.hstack((photos[2],photos[3]))

        photobooth = np.vstack((top,bottom)) #v stack vertical

        photobooth_height, photobooth_width = photobooth.shape[:2]
        background = np.full((photobooth_height + 2 * border, photobooth_width + 2 * border, 3), background_col, dtype=np.uint8)
        background[border:border + photobooth_height, border:border + photobooth_width] = photobooth
        cv2.rectangle(background, (border, border), (background.shape[1] - border, background.shape[0] - border), (0, 0, 0), 5)
        background = cv2.resize(background, (background.shape[1] // 2, background.shape[0] // 2))


    # This section kasi diba sa opencv bgr yung color, this convert it to rgb  
        pil_img = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

    #Etong section na i2 ay nag hahandle ng text shits na nakalagay sa photobooth frame para istetik hihi
        bbox = draw.textbbox((0, 0), frame_text, font=font)
        text_width = bbox[2] - bbox[0]  
        text_height = bbox[3] - bbox[1]  

        # This section adds a border around the text "Our Memories" para mas noticeable bali iniistack niya lang yung text para mag mukang border
        border_offset = 2 

        text_position = ((pil_img.width - text_width)//2, border ) 

        draw.text((text_position[0] - border_offset, text_position[1] - border_offset), frame_text, font=font, fill=(0, 0, 0)) 
        draw.text((text_position[0] + border_offset, text_position[1] - border_offset), frame_text, font=font, fill=(0, 0, 0))  
        draw.text((text_position[0] - border_offset, text_position[1] + border_offset), frame_text, font=font, fill=(0, 0, 0))  
        draw.text((text_position[0] + border_offset, text_position[1] + border_offset), frame_text, font=font, fill=(0, 0, 0))  

        draw.text(text_position, frame_text, font=font, fill=(255, 255, 0)) 

    # Convert ulit indecisive ako e saka need 
        background = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        cv2.imshow("Our Memories!", background)

        # This section will ask you if you wanna discard or save your photo. 

        print ("Do you wanna save (s) or Discard (d)")

        while True:

            ok = cv2.waitKey(1)

            if ok%256 == 27:
                print("Goodbye!")
                break

            elif ok%256. == ord ('s'):
                cv2.imwrite("Memories.png", background)
                print ("Photobooth saved!")
                break

            elif ok%256 == ord('d'):
                print ("Photo discarded.")
                break

    # I put the whole thing sa loob ng while loop para po pwede ulitin ng user kung gusto nila. Shown below.

    try_again = input("Do you want to try again? (y/n): ").strip().lower()
    if try_again == 'y':
        print("Let's take more photos!")
        count = 0
        photos.clear()
        continue

    elif try_again == 'n':
        print("Thanks for using the photobooth!")
        break 

    else:
        print("Invalid input. Please enter 'y' or 'n'.")




    cam.release()

    cv2.destroyAllWindows()

    #Ngayon ko lang po narealize na kung sana nilagay ko nalang sa function to lahat mas madali buhay ko. Thank you.