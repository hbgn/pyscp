""""
psutil模块
（一种跨平台库，作用：用于获取系统进程，cpu、内存、磁盘等资源利用率等性能指标，
常常用于系统监控，性能分析和资源进程管理）

一、需求背景
psutil学习整理，方法封装。
"""
import psutil

# cpu


# Memory


# Disks


# Network


# Sensors


# Other system info


# Process management



import psutil
import datetime


class Monitor:

    # 获取cpu的信息
    def cpu(self):
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),
            percent_per=psutil.cpu_percent(interval=0, percpu=True),
            num_p=psutil.cpu_count(logical=False),  # 核心数量
            num_l=psutil.cpu_count(logical=True)
        )
        return data

    # 获取内存的信息
    def mem(self):
        data = dict(
            total=round(psutil.virtual_memory().total / 1024 / 1024, 2),
            used=round(psutil.virtual_memory().used / 1024 / 1024, 2),
        )
        return data

    # 获取网卡信息(适配器名称，ipv4，收发数据流)
    def net(self):
        address = psutil.net_if_addrs()  # ip
        address_info = {
            k: [
                dict(
                    family=data.family.name,
                    addr=data.address,
                    netmask=data.netmask,
                    broadcast=data.broadcast,
                )
                for data in v if data.family.name == 'AF_INET'
            ][0]
            for k, v in address.items()
        }
        io = psutil.net_io_counters(pernic=True)
        rs_data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **address_info[k]
            )
            for k, v in io.items()
        ]
        return rs_data

    def dt(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
