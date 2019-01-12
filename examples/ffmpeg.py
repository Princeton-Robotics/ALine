from ffpyplayer.player import MediaPlayer
import time
import numpy as np
import cv2

ff_opts={'protocol_whitelist':'file,crypto,udp,rtp'}
player = MediaPlayer('bebop.sdp', ff_opts=ff_opts)
val = ''
i = 0
while val != 'eof':
    frame, val = player.get_frame()
    if val != 'eof' and frame is not None:
        img, t = frame
        cv_im = np.asarray(np.asarray(img.to_bytearray())[0])
        print(cv_im.shape)
        cv_im_color = np.reshape(cv_im, [720, 1080, 3])
        cv_im_color = cv_im_color / 255
        # cv_im = cv2.cvtColor(cv_im_color, cv2.COLOR_RGB2GRAY)
        print(cv_im_color.shape)
        print(cv_im_color[0,0,0])
        print(cv_im_color[0,0,1])
        print(cv_im_color[0,0,2])
        cv2.imshow('image', cv_im_color)
        i = i + 1
        key = cv2.waitKey(42)