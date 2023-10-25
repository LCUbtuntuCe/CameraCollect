import cv2
import numpy as np
import threading
import os
import time
import datetime

def frame(today_video, today_frame, i):   #transfer every video to many photos
	print("\ntransfer every video to many photos\n")
	Source_video = today_video + '\\'+'{}.mp4'.format(str(i))    # 要取帧的视频
	frame_folder = today_frame + '\\'+'{}\\'.format(str(i))
	os.mkdir(frame_folder)					# 新建的小文件夹
	num_photo = 0
	interval = 15						#每隔15帧取一次
	cap = cv2.VideoCapture(Source_video)			#读取视频
	if cap.isOpened:
		ret, frame = cap.read()				# attain a photo
		while ret :
			num_photo = num_photo + 1
			if num_photo % interval == 0 :
				image_path = frame_folder+str(num_photo/interval) +'.jpg'
				print(image_path+'\n')
				cv2.imwrite(image_path, frame)		# save photo
			ret, frame = cap.read()				# attain a photo
		if not ret and not num_photo:
			print('\nFailed to get frame from {}.mp4\n'.format(str(i)))
	cap.release()

def video_download(today_video, i):  # capture video
	print('\ncapture video about 10 minutes\n')
	camera_path = 'rtsp://admin:123456@192.168.1.2/h264/ch1/sub/av_stream'			# 摄像头链接
	cap=cv2.VideoCapture(camera_path)
	if not cap.isOpened:
		exit(1)
	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) # watch out
	frame_s = cap.get(cv2.CAP_PROP_FPS)  				# Using this camera, how many frames in every second.
	time_frame = frame_s*60*10 			#设置保存时间为10分钟一保存
	num = 0
	filename = today_video + '\\' + str(i) + ".mp4"
	video_writer = cv2.VideoWriter(filename, fourcc, frame_s, size, True)
	ret, frame = cap.read()
	frame = cv2.putText(frame, time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())), (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
	while ret:
		video_writer.write(frame)
		ret, frame = cap.read()
		frame = cv2.putText(frame, time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())), (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
		num = num + 1
		if num == time_frame :
			video_writer.release()
			num = 0
			break
	cap.release()

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
		video_download(today_video, i)
		frame(today_video, today_frame, i)
		i = i + 1

if __name__ == '__main__':  # the main of the program
	Implement = threading.Thread(target=implement, daemon=True)  # create a new thread
	Implement.start()
	i = 0
	while True:					     # check the thread
		if not Implement.is_alive():
			break
	print("\n Finished the task!  \n")