import sys
import time

from action_run import ActionRun

"""
运行此脚本可以立即执行录制好的脚本
你也可以在windows的计划任务里有计划地执行此脚本
"""
if __name__ == '__main__':

    mc = ActionRun()
    mc.start()
    print('执行完毕')
