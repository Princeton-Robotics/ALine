from djitellopy import Tello
import cv2
import pygame
from pygame.locals import *
import numpy as np
import time
import math

# Speed of the drone
S = 60
# Frames per second of the pygame window display
FPS = 40


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

            # Separate feed with line recognition overlay.
            draw_second_picture(frame_read.frame)

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


def draw_second_picture(image):
    """
    Grab the latest stream from the drone and draw it in a second opencv window with some text to show that it
    is being processed
    :param image:
    :return:
    """

    img = image

    # if the images is invalid, return
    if (img is None):
        return

    # put the roll and pitch at the top of the screen
    # cv2.putText(img, 'demo text', (50, 50), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
    # cv2.imshow("MarkerStream", img)
    # cv2.waitKey(1000)

    kernal = np.array((
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1]
    ))

    toFilter = img[:, :, 2] - img[:, :, 1] - img[:, :, 0]

    lines = cv2.filter2D(toFilter, -1, kernal)

    th, dst = cv2.threshold(lines, 100, 255, cv2.THRESH_BINARY)

    lines = cv2.HoughLines(dst, 1, np.pi / 180, 70)

    cv2.imshow('dst', dst)

    # if (lines == None):
    # print("no line found")
    # else:

    # height: 480 width: 856

    height, width, channels = img.shape
    centerX = width / 2
    centerY = height / 2

    if (lines is None):
        print("no line found")
    else:
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # cv2.putText(img, 'r: ' + str(rho), (50, 50), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
            # cv2.putText(img, 'theta: ' + str(theta), (50, 75), font, 1, (255, 0, 255), 2, cv2.LINE_AA)
            dTheta = -min(theta, 2 * math.pi - theta)

    cv2.imshow('houghlines3.jpg', img)
    cv2.waitKey(100)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
