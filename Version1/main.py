import cv2
import numpy as np
import threading
import os
import time
import datetime
import queue
import camera_func

def implement():
	if not os.path.exists(r'D:\Underwater_Video'):
		os.makedirs(r'D:\Underwater_Video')
	if not os.path.exists(r'D:\Underwater_Frame'):
		os.makedirs(r'D:\Underwater_Frame')
	today = str(datetime.date.today())      # 获取今天的日期并转换成字符串
	today_video = r'D:\Underwater_Video' + '\\' + today        # 存放今天的录像
	today_frame = r'D:\Underwater_Frame' + '\\' + today         # 存放今天的取帧图片
	os.mkdir(today_video)
	os.mkdir(today_frame)
	i = 1
	while True:
		if not func.OpenCamera():
			break
		filename = func.Video(today_video, i)
		func.frame(filename, today_frame, i)
		i = i + 1

if __name__ == '__main__':  # the main of the program
    Implement = threading.Thread(target=implement, daemon=True)  # create a new thread
    Implement.start()
    Implement.join()
    print("\n Finished the task!  \n")