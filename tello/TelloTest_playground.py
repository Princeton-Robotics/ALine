from djitellopy import Tello
from simple_pid import PID
import cv2
import pygame
from pygame.locals import *
import numpy as np
import time
import math
import sys

# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 10
# x pixel length
X_SCREENLENGTH = 960
# y pixel length
Y_SCREENLENGTH = 720
class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame.
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([960, 720])

        # Init Tello object that interacts with the Tello drone.
        self.tello = Tello()

        # Drone velocities between -100~100.
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        # Create update timer.
        pygame.time.set_timer(USEREVENT + 1, 50)

    def run(self):

        if not self.tello.connect():
            print("Tello not connected")
            return

        if not self.tello.set_speed(self.speed):
            print("Not set speed to lowest possible")
            return

        # In case streaming is on. This happens when we quit this program without the escape key.
        if not self.tello.streamoff():
            print("Could not stop video stream")
            return

        if not self.tello.streamon():
            print("Could not start video stream")
            return

        frame_read = self.tello.get_frame_read()
        # Display the video stream.
        should_stop = False
        while not should_stop:

            for event in pygame.event.get():
                if event.type == USEREVENT + 1:
                    self.update()
                elif event.type == QUIT:
                    should_stop = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                frame_read.stop()
                break

            self.screen.fill([0, 0, 0])
            frame = cv2.cvtColor(draw_segments(frame_read.frame), cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = np.flipud(frame)
            frame = pygame.surfarray.make_surface(frame)
            # get_centered_on_line(frame_read.frame)
            self.screen.blit(frame, (0, 0))
            pygame.display.update()

            # Separate feed with line recognition overlay.
            # draw_segments(frame_read.frame)

            time.sleep(1 / FPS)
        # Call it always before finishing. I deallocate resources.
        self.tello.end()

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw counter clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity, self.up_down_velocity,
                                       self.yaw_velocity)


def get_frame_error(x1, y1, x2, y2):
    length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    sin_angle = (x2 - x1) / length
    sign = (y2 - y1)/(abs(y2-y1))
    if y2==y1:
        mid = get_midpoint(x1, y1, x2, y2)
        direction = mid/abs(mid)
        return math.pi/2 * direction
    return -np.arcsin(sin_angle)*sign

def get_midpoint(x1, y1, x2, y2):
    midx = (x1 + x2)/2
    # midy = (y1 + y2)/2
    return midx

def get_coordinates(image):
    img = image

    # if the images is invalid, return
    if img is None:
        return

    kernel = np.array((
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ))

    to_filter = img[:, :, 2] - img[:, :, 1] - img[:, :, 0]

    line_img = cv2.filter2D(to_filter, -1, kernel)

    th, dst = cv2.threshold(line_img, 100, 255, cv2.THRESH_BINARY)

    rho = 1
    theta = np.pi / 180
    threshold = 70
    min_len = 70
    max_gap = 200

    # Find all the line segments in the image, returned in an array.
    lines = cv2.HoughLinesP(dst, rho, theta, threshold, np.array([]), min_len, max_gap)

    return lines
def draw_segments(image):
    """
    Grab the latest stream from the drone and draw it in a second opencv window with some text to show that it
    is being processed
    :param image:
    :return:
    """

    img = image
    lines = get_coordinates(image)
    # if the images is invalid, return
    if img is None:
        return
    get_centered_on_line(image)
    # displays the lines on the image
    if lines is None:
        print("no line found")
    else:
        line = lines[0]
        for x1, y1, x2, y2 in line:
            # error = get_error(x1, y1, x2, y2)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 5)
            # display coordinates for debugging
            display_values(get_frame_error(x1, y1, x2, y2), x1, y1, x2, y2, image)
    # cv2.imshow('segment', img)
            midx =int(get_midpoint(x1, y1, x2, y2))
            midy = int((y2+y1)/2)
            scrnx =int(X_SCREENLENGTH/2)
            scrny = int(Y_SCREENLENGTH/2)
            cv2.circle(img,(midx,midy), 10, (0, 0, 255), -1)
            cv2.circle(img,(scrnx,scrny), 10, (0, 0, 255), -1)
            cv2.line(img, (midx, midy), (scrnx, scrny), (0, 255, 0), 5)
    cv2.waitKey(500)
    return img
# crops the image and looks at a a horizontal slice of the screen
# finds the center of mass and takes the difference from the center of the screen
# should returns a percentage from the center of the screen.
# currently displaying an image

# def get_centered_on_line(image):
#     return
    # x = X_SCREENLENGTH
    # y = Y_SCREENLENGTH
    # h = 50
    # # crop the image
    # # random values here cuz running low on time
    # crop_img = image[480:520, 300]
    # # isolate the red ( can be further optimized since repeating stuff in finding lines)
    # toFilter = crop_img[:,:,2] - crop_img[:,:,1] - crop_img[:,:,0]
    # ret,thresh1 = cv2.threshold(toFilter, 75,255, cv2.THRESH_BINARY_INV)
    # M = cv2.moments(thresh1)

    # if(M["m00"] != 0):
    #     cX = int(M["m10"] / M["m00"])
    #     cY = int(M["m01"] / M["m00"])
    # else:
    #     cX =0
    #     cY =0
    # cv2.circle(thresh1, (cX, cY), 5, (0, 0, 255), -1)
    # cv2.imshow('get_centered_on_line', thresh1)


#arg 0 = frame error (angle control)
#arg 1 - 4 = coordinates detected
def display_values(frame_error, X1, Y1, X2, Y2, image):
    # Create a black image
    img = np.zeros((512,512,3), np.uint8)

    # Write some Text

    font                   = cv2.FONT_HERSHEY_SIMPLEX
    x_coord = 10
    y_coord = 40
    fontScale              = .75
    fontColor              = (255,255,255)
    lineType               = 0

    cv2.putText(img,'frame error ' + str(frame_error), (x_coord, y_coord), font, fontScale, fontColor, lineType)
    cv2.putText(img,'coordinates: '+ '1: ' + str(X1) + ', '+str(Y1) +'    1: ' + str(X2) + ', '+str(Y2), (x_coord, y_coord+40) , font, fontScale, fontColor, lineType)
    
    cv2.putText(img,'midpoint' + str(get_midpoint(X1, Y1, X2, Y2)), (x_coord, y_coord+80), font, fontScale, fontColor, lineType)
    # cv2.putText(img,'y diff ' + str(Y2 - Y1), (x_coord, y_coord+80), font, fontScale, fontColor, lineType)
    #Display the image

    cv2.waitKey(100)

# def pid_angle_control(frame_error):

# def pid_center_control():

def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
