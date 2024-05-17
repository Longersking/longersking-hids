import psutil
import time
# 定义一个专门用于获取系统信息的类
class Monitor(object):
    # 单位换算
    def byte_to_gb(self,data):
        return round(data / (1024 ** 3),2)
    # 获取cpu信息
    def cpu(self):
        # percpu :True获取每个cpu的使用率，False获取平均率
        # 1.平均  2、单独  3、物理核心数 4.逻辑cpu核心数
        data = dict(
            percent_avg = psutil.cpu_percent(interval=0,percpu=False),
            percent_per = psutil.cpu_percent(interval=0,percpu=False),
            num_physic = psutil.cpu_count(logical=False),
            num_logic = psutil.cpu_count(logical=True)
        )
        return data

    # 获取内存信息
    # 总量 GB
    # 剩余量 GB
    # 使用率 %
    def mem(self):
        #内存信息
        info = psutil.virtual_memory()
        data = dict(
            total = self.byte_to_gb(info.total),
            used = self.byte_to_gb(info.used),
            free = self.byte_to_gb(info.free),
            percent = info.percent
        )
        return data

    def swap_memory(self):
        # 交换内存区
        info = psutil.swap_memory()
        data = dict(
            total=self.byte_to_gb(info.total),
            used=self.byte_to_gb(info.used),
            free=self.byte_to_gb(info.free),
            percent=self.byte_to_gb(info.percent)
        )
        return data


if __name__ == '__main__':
    test = Monitor()
    # for v in range(1,11):
    #     print(test.cpu())
    #     time.sleep(1)
    # print(test.mem())
    print(test.swap_memory())