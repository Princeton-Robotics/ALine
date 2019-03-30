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
        return (x2 - x1) / length


def draw_segments(image):
    """
    Grab the latest stream from the drone and draw it in a second opencv window with some text to show that it
    is being processed
    :param image:
    :return:
    """

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
    max_gap = 70

    # Find all the line segments in the image, returned in an array.
    lines = cv2.HoughLinesP(dst, rho, theta, threshold, np.array([]), min_len, max_gap)

    # Overlay the first (longest) line on the original image.
    if lines is None:
        print("no line found")
    else:
        line = lines[0]
        for x1, y1, x2, y2 in line:
            # error = get_error(x1, y1, x2, y2)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 5)

    # cv2.imshow('segment', img)
    # cv2.waitKey(100)

    return img


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()
