import cv2
import threading
import queue
import os
import datetime
import time
class Camera():
    def __init__(self):
        # 准备相关文件路径
        if not os.path.exists(r'D:\Underwater_Video'):
            os.makedirs(r'D:\Underwater_Video')
        if not os.path.exists(r'D:\Underwater_Frame'):
            os.makedirs(r'D:\Underwater_Frame')
        today = str(datetime.date.today())  # 获取今天的日期并转换成字符串
        self.today_video = r'D:\Underwater_Video' + '\\' + today  # 存放今天的录像
        self.today_frame = r'D:\Underwater_Frame' + '\\' + today  # 存放今天的取帧图片
        if not os.path.exists(self.today_video):
            os.mkdir(self.today_video)
        if not os.path.exists(self.today_frame):
            os.mkdir(self.today_frame)
        # 设置基本参数
        self.camera_path = 'rtsp://admin:123456@192.168.1.2/h264/ch1/sub/av_stream'                             # 摄像头链接
        self.cap = cv2.VideoCapture(self.camera_path)                                                           # 打开摄像头
        self.frame = None                                                                                       # 暂存读出来的帧
        self.ret = False
        self.size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 确定帧的大小
        self.frame_s = self.cap.get(cv2.CAP_PROP_FPS)                                                            # 帧率
        self.time_frame = self.frame_s * 60 * 60                                                                  # 每段视频1小时
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')                                                            # 视频格式
        self.Q1 = queue.Queue()                                                                                  # 用来暂存帧的队列
        self.video_num = 1                                                                                       # 当前正在录制第几段视频
        self.opencamera = threading.Thread(target=self.OpenCamera, args=())
        self.opencamera.start()
        time.sleep(3)
        self.video = threading.Thread(target=self.Video, args=())
        self.video.start()

    def OpenCamera(self):                                                                                       # 开摄像头取帧
        while True:
            self.ret, self.frame = self.cap.read()
            while self.ret:
                self.Q1.put(self.frame)
                self.ret, self.frame = self.cap.read()

    def Video(self):
        interval = 30                                                                             # 间隔多少帧存图
        i = 0
        filename = self.today_video + '\\' + str(self.video_num) + ".mp4"                         # 保存的视频文件
        video_writer = cv2.VideoWriter(filename, self.fourcc, self.frame_s, self.size, True)
        while True:
            while self.Q1.empty():
                continue
            while not self.Q1.empty():
                frame = self.Q1.get()
                i += 1
                frame = cv2.putText(frame, time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime(time.time())), (5, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)  # 打上时间戳
                video_writer.write(frame)
                if i % self.time_frame == 0:
                    video_writer.release()
                    self.video_num += 1                                                         # 开始录制第几段视频
                    filename = self.today_video + '\\' + str(self.video_num) + ".mp4"           # 保存的视频文件
                    video_writer = cv2.VideoWriter(filename, self.fourcc, self.frame_s, self.size, True)
                    break
                if i % interval == 0:
                    image_path = self.today_frame + '\\' + str(i / interval) + '.jpg'
                    print(image_path + '\n')
                    cv2.imwrite(image_path, frame)                      # save photo