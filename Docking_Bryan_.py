import numpy as np
import cv2
from oepnc import Video
from pymavlink import mavutil
from datetime import datetime
from datetime import timezone
import time

def FindGoal(frame, h, w):
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # lower mask (0-10)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    # join my masks
    mask = mask0 + mask1

    bbox = cv2.boundingRect(mask)
    contours, hierarchies = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    return contours

master = mavutil.mavlink_connection('udpin:localhost:14445')
print("waiting heartbeat")
master.wait_heartbeat()
print("confirmed")
master.mav.command_long_send(master.target_system, master.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

master.motors_armed_wait()


def set_rc_channel_pwm(channel_id, pwm=1500):
    if channel_id < 1 or channel_id > 18:
        print("mylls")
        return

    rc_channel_values = [65535 for _ in range(18)]
    rc_channel_values[channel_id - 1] = pwm
    master.mav.rc_channels_override_send(
        master.target_system,                # target_system
        master.target_component,             # target_component
        *rc_channel_values)


cap = Video(port=4777)
print("Testing Camera")

height, width = 0, 0
'''
while True:
    if not cap.frame_available(): continue
    vid = cap.frame()
    height, width = vid.shape[:2]
    print(f"Frame Size: Height: {height} | Width: {width}")
    cv2.imshow("vid", vid)
    if cv2.waitKey(26) in [ord('q'), 27]:
        break

print("----------------Camera Test Finished----------------")
print("Entering Main")
'''
coords = ()
while True:

    if not cap.frame_available():
        continue

    vid = cap.frame()
    height, width = vid.shape[:2]
    contours = FindGoal(vid, height, width)
    py = 0
    px = 0
    for i in contours:
        M = cv2.moments(i)
        if M['m00'] != 0:
            px = int(M['m10'] / M['m00'])
            py = int(M['m01'] / M['m00'])


    depth = 1500 + ((-20 / 27) * np.power(py, 1) + 400)
    lat = 1500 + ((5 / 12) * np.power(px, 1) - 400)

    ct = time.time()
    #check for x
    if not (495 <= py <= 595):
        set_rc_channel_pwm(3, 1500 + int(depth))
        print("Rechecking for py")

        if (495 <= py <= 595):
            set_rc_channel_pwm(3, 1500)
            print("Stop checking for py now")

    if not (630 <= px <= 1040):
        set_rc_channel_pwm(6, 1500 + int(lat))
        print("Rechecking for py")
        if (630 <= px <= 1040):
            set_rc_channel_pwm(6, 1500)

    if (495 <= py <= 595) and (630 <= px <= 1040):
        # while (495 <= py <= 595) and (630 <= px <= 1040):
        #     set_rc_channel_pwm(5, 1900)
        set_rc_channel_pwm(5, 1900)

    if not (495 <= py <= 595) and (630 <= px <= 1040):
        set_rc_channel_pwm(5, 1500)

    cv2.imshow("vid", vid)
    if not cap.frame_available():
        print("no frame avaliable ")
    if cv2.waitKey(1) in [ord('q'), 27]:
        time.sleep(0.1)
        set_rc_channel_pwm(3, 1500)
        set_rc_channel_pwm(6, 1500)
        set_rc_channel_pwm(5, 1500)
        break

cap.release()
cv2.destoryAllWindows()
