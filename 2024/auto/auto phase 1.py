import time
import cv2
import numpy as np
import autodefs as auto
from autodefs import set_rc_channel_pwm
from oepnc import Video
from pymavlink import mavutil

auto.init()

height, width = 0, 0

timer = time.time()

auto.look_at(0)
time.sleep(0.1)

while True:
    current = time.time()
    if cap.frame_available():
        frame = cap.frame()
        
        capframe = color(frame, [0, 0, 0], [0, 0, 29])
        
        greyscale = cv2.cvtColor(capframe, cv2.COLOR_BGR2GRAY)

        _, binary_image =  cv2.threshold(greyscale, 150, 255, cv2.THRESH_BINARY)

        all_contours, hierachy = cv2.findCounters(binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        centx, centy = 0, 0
        for contour in all_contours: 
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

            if len(approx) == 4:
                x, y, w, h == cv2.boundingRect(approx)
                aspect_ratio = float(w) / h

                cv2.drawContours(frame, [approx], -1, (0, 255, 0), 3)
                centx = x + w/2
                centy = y + h/2

        frame = cv2.circle(frame, (centx, centy), 3, (0, 255, 0), 3)

        depth = 1500 + ((-20/27) * np.power(centy, 1) + 400)
        lat = 1500 + ((5/12) * np.power(centx, 1) - 400)
        while current <= timer + 10:
            set_rc_channel_pwm(3, int(depth))
            set_rc_channel_pwm(6, int(lat))
            set_rc_channel_pwm(5, 1550)


        cv2.imshow('frame', frame)
        if not cap.frame_available():
            print("tears")
    # write the frame to the output file
    if cv2.waitKey(1) == ord('q'):
        time.sleep(0.1)
        set_rc_channel_pwm(3, 1500)
        set_rc_channel_pwm(6, 1500)
        set_rc_channel_pwm(5, 1500)
        break

cap.release()
cv2.destroyAllWindows()
