import cv2
import numpy as np
import threading
import os
import time
import datetime
import queue

Q1 = queue.Queue()      # 暂时存放读取的帧，用于组成视频
size = (0,0)
frame_s = 0

def OpenCamera():
    global size
    global frame_s
    print('\ncapture video about 10 minutes\n')
    camera_path = 'rtsp://admin:123456@192.168.1.2/h264/ch1/sub/av_stream'  # 摄像头链接
    cap = cv2.VideoCapture(camera_path)
    if not cap.isOpened:
        return False
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))    # 确定帧的大小
    frame_s = cap.get(cv2.CAP_PROP_FPS)                                                         # Using this camera, how many frames in every second.
    time_frame = frame_s * 60 * 10                                                              # 设置保存时间为10分钟一保存
    num = 0
    ret, frame = cap.read()
    while ret:
        Q1.put(frame)
        num = num + 1
        if num == time_frame:
            break
        ret, frame = cap.read()
    cap.release()
    return True

def Video(today_video, i):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')    # 确定格式
    filename = today_video + '\\' + str(i) + ".mp4" #保存的视频文件
    video_writer = cv2.VideoWriter(filename, fourcc, frame_s, size, True)
    while not Q1.empty():
        frame = Q1.get()
        frame = cv2.putText(frame, time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())), (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        video_writer.write(frame)
    video_writer.release()
    return filename

def frame(filename, today_frame, i):
    print("\ntransfer every video to many photos\n")
    frame_folder = today_frame + '\\' + '{}\\'.format(str(i))
    os.mkdir(frame_folder)  # 新建的小文件夹
    num_photo = 0
    interval = 15  # 每隔15帧取一次
    cap = cv2.VideoCapture(filename)  # 读取视频
    if cap.isOpened:
        ret, frame = cap.read()  # attain a photo
        while ret:
            num_photo = num_photo + 1
            if num_photo % interval == 0:
                image_path = frame_folder + str(num_photo / interval) + '.jpg'
                print(image_path + '\n')
                cv2.imwrite(image_path, frame)  # save photo
            ret, frame = cap.read()  # attain a photo
        if not ret and not num_photo:
            print('\nFailed to get frame from {}.mp4\n'.format(str(i)))
    cap.release()