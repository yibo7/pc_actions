import json

import XsCore
import pyautogui
import pyperclip
from XsCore.XsJson import XsJson

from action_type import ActionType


class ActionRun:
    def __init__(self):
        self.last_pos = []
        self.actions = []
        self.load_action()

    def load_action(self):
        js = XsJson('data/action.json')
        data = js.load()
        if data:
            self.actions = data
        else:
            print('没有可执行的动作')

    def start(self):
        # pyautogui.sleep(3)
        for act in self.actions:
            if act['type'] == ActionType.Input:
                content = act['c']
                pyperclip.copy(content)
                # print(f'输入内容：{ content}')
                # pyautogui.typewrite(content, 0.25)
                pyautogui.leftClick()
                # a = pyperclip.paste() 注意，pyperclip.paste只能将内容赋值给一个变量，不能实现真正的粘贴
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.sleep(1)
            else:
                if act['pos'] != self.last_pos:
                    pyautogui.moveTo(act['pos'], duration=0.5)
                    self.last_pos = act['pos']
                    pyautogui.sleep(act['sleep'])

                if act['type'] == ActionType.LeftClick:
                    pyautogui.leftClick()
                elif act['type'] == ActionType.RightClick:
                    pyautogui.rightClick()
                elif act['type'] == ActionType.MiddleClick:
                    pyautogui.middleClick()