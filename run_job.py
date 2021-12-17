
from apscheduler.schedulers.blocking import BlockingScheduler

from action_run import ActionRun

"""
运行此脚本可以在计划任务里执行录制好的脚本
"""
if __name__ == '__main__':
    print("开始")
    mc = ActionRun()
    scheduler = BlockingScheduler(timezone='Asia/Shanghai')
    # scheduler.add_job(self.goto_click, 'interval', max_instances=1, seconds=10)
    # 在每天22和23点的25分，运行一次 job 方法 args是要执行的job方法的参数，没有参数不用写
    # scheduler.add_job(self.goto_click, 'cron', hour='22-23', minute='25', args=['job2'])
    # 在每天23点的25分，运行一次 job 方法
    scheduler.add_job(mc.start, 'cron', hour='22', minute='13')
    scheduler.start()  # 阻塞式
