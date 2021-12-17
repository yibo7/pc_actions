from action_recoder import ActionRecoder
"""
运行此脚本可以录制动作

录制鼠标键盘的动态
1.按下f10清理所有动作并开始录制，再次按下f10结束录制并在10秒后回放所有动态
2.在录制的过程中按下空格键，代表将在此步输入文本，文本可以在录制完成的json文件里修改
3.按下f4清空所有录制好的动作
"""
if __name__ == '__main__':
    ma = ActionRecoder()
    ma.start()

