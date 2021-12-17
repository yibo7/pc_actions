
import pyautogui

# 是否开启保护措施，避免失控
pyautogui.FAILSAFE = False
# 为所有的PyAutoGUI函数增加延迟。默认延迟时间是0.1秒。但需要实现双击的时候不能这样设置
# pyautogui.PAUSE = 0.5
'''
本示例演示如何通过图片定位的试操作鼠标
注意，要使用pyautogui的图片识别及截图功能，还要安装Pillow
'''
if __name__ == '__main__':
    # 获取当前屏幕分辨率
    screenWidth, screenHeight = pyautogui.size()
    # 鼠标移到屏幕中央。
    x = screenWidth / 2
    y = screenHeight / 2
    y += 200
    pyautogui.moveTo(x, y, duration=1,)

    countNum = 0
    while True:
        pyautogui.sleep(10)
        # 按钮鼠标左键拖动
        # pyautogui.dragTo(x, y-700, duration=0.5)
        pos = pyautogui.locateCenterOnScreen('images/target.png') # , grayscale=True
        if pos:
            # pos = pyautogui.center(pos_helper) # 获取中间位置

            pyautogui.moveTo(pos, duration=1) # 移动鼠标到指定位置
            pyautogui.moveRel(307,-145, duration=1) # 从当前鼠标位置到指定位置
            pyautogui.click() # 左键点击一下
            # countNum +=1
            # print(f"一共划屏{countNum}次")
        else:
            print('没有找到目标')
