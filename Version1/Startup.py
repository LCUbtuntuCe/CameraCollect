import time
import pyautogui as pg

def Startup():              # 启动OTech
    time.sleep(10)          # 先延时10秒
    pg.size()               # 获得屏幕尺寸
    if pg.onScreen(200, 36):
        pg.moveTo(200,36)
        pg.click(duration=0.5)      # 点击“实时”
    if pg.onScreen(324, 37):
        pg.moveTo(324,37)
        pg.click(duration=0.5)      # 检查型号，确保接通侧扫声呐
        time.sleep(5)
    if pg.onScreen(1581, 201):
        pg.moveTo(1581,201)
        pg.click(duration=0.5)      # 设置存储
    if pg.onScreen(1377, 128):
        pg.moveTo(1377,128)
        pg.click(duration=0.5)      # 保存为XTF标准格式
    if pg.onScreen(397, 36):
        pg.moveTo(397,36)
        pg.click(duration=0.5)      # 启动扫描
    pg.moveTo(0,0)
    time.sleep(5)
