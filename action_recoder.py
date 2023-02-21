import json
import time
import pynput
from XsCore.XsJson import XsJson
from pynput import keyboard
from pynput.keyboard import Key
from pynput.mouse import Button

from action_run import ActionRun
from action_type import ActionType

"""
录制鼠标键盘的动态
1.按下f10清理所有动作并开始录制，再次按下f10结束录制并在10秒后回放所有动态
2.在录制的过程中按下空格键，代表将在此步输入文本，文本可以在录制完成的json文件里修改
3.按下f4清空所有录制好的动作
"""


class ActionRecoder:
    def __init__(self):
        self.last_time = 0
        self.step = 0
        self.actions = []
        self.is_recoding = False
        self.is_dragTo = False  # 是否切换到拖拽模式，拖拽动作的左键松开时会自动换回 False

    def time_span(self):
        """
        获取当前时间与上次时间的时间差，秒数
        :return:
        """
        currentT = time.time()
        ts = 0
        if self.last_time > 0:
            ts = currentT - self.last_time
        self.last_time = currentT
        return ts

    def update_action(self, x, y, at: int):
        ts = self.time_span()
        if len(self.actions) > 0:
            last = self.actions[-1]
            last['sleep'] = ts
        self.step += 1
        if at == ActionType.Input:
            self.actions.append({'id': self.step, 'type': at, 'pos': [x, y], 'sleep': 0, 'c': '请修改成你想要的内容'})
        else:
            self.actions.append({'id': self.step, 'type': at, 'pos': [x, y], 'sleep': 0, 'c': ''})

    def on_move(self, x, y):
        """
        鼠标移动时触发
        :param x: x坐标
        :param y: y坐标
        :return:
        """
        pass
        # print('Pointer moved to {0}'.format((x, y)))

    def on_click(self, x, y, button, is_press):
        """
        鼠标点击时触发
        :param x: x坐标
        :param y: y坐标
        :param button: 点击的鼠标键类型
        :param is_press: 是按下还是松开
        :return:
        """
        # print(f"鼠标{button}键在({x}, {y})处{'按下' if is_press else '松开'}")
        if self.is_recoding:
            if self.is_dragTo:  # 记录拖拽模式
                if not is_press and button == Button.left:
                    self.update_action(x, y, ActionType.dragTo)
                    self.is_dragTo = False
                    print("结束拖拽")
                elif button == Button.left and is_press:
                    print("开始拖拽")
                    self.update_action(x, y, ActionType.LeftClick)
            else:
                if button == Button.left and is_press:
                    self.update_action(x, y, ActionType.LeftClick)

                elif button == Button.right and is_press:
                    self.update_action(x, y, ActionType.RightClick)

                elif button == Button.middle and is_press:
                    self.update_action(x, y, ActionType.MiddleClick)

        # if not is_press:
        #     # Stop listener
        #     return False

    def on_scroll(self, x, y, dx, dy):
        """
        鼠标滚轮时触发
        :param x: 滚轮时鼠标的x坐标
        :param y: 滚轮时鼠标的y坐标
        :param dx:
        :param dy:
        :return:
        """
        pass
        # print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up',(x, y)))

    def on_press(self, key):
        """
        监听键盘的键按下
        :param key:
        :return:
        """
        try:
            # pass
            # print(f'键 {key.char} 按下')
            # print(f'键 {key} 按下')
            if key == Key.f10:
                self.is_recoding = not self.is_recoding
                if self.is_recoding:
                    self.actions.clear()
                    print("清空旧数据，开启记录")
                else:
                    self.save_action()
                    print("结束记录,开始回放操作")
                    for i in range(10, 0, -1):
                        time.sleep(1)  # 这里为了查看输出变化，实际使用不需要sleep
                        print(f'\r将在{i}秒后回放动作', end='', flush=True)
                    ActionRun().start()
                    print("\r动作回放完毕!")

            elif key == Key.space:  # key.char == i
                if self.is_recoding:
                    self.update_action(0, 0, ActionType.Input)
                    print("输入标记")
            elif key == Key.f4:
                self.actions.clear()
                print("已清空所有动作")
            elif key == Key.f8:  # 进入拖拽模式
                self.is_dragTo = True
                print("进入拖拽模式")

        except AttributeError:
            pass
            # print(f'无法识别的键 {key} 按下')

    def on_release(self, key):
        """
        监听键盘的键松开
        :param key:
        :return:
        """
        # print(f'{key} 松开')
        if key == Key.esc:
            # Stop listener
            print('退出键盘监听')
            return False

    def save_action(self):
        """
        将录制好的动作保存到json文件中
        :return:
        """
        js = XsJson('data/action.json')
        js.save(self.actions)

    def start(self):
        # 开始监听方法,这里是不要让主线程退出，所以采用了阻塞，否则还要在主线程加一个无限循环
        # with pynput.mouse.Listener(
        #         on_move=self.on_move,
        #         on_click=self.on_click,
        #         on_scroll=self.on_scroll) as listener:
        #     listener.join()

        print('开始监听鼠标')
        # 或者这样写不会造成阻塞
        listener = pynput.mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        listener.start()  # 非阻塞式

        print('开始监听键盘')
        print('按下【f10】开始或结束录制')
        print('按下【f8】切换到拖拽模式')
        print('按下【空格】记录输入')
        with keyboard.Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()  # 阻塞式
