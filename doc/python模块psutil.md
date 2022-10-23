# 一、psutil简介

一种跨平台库，作用：用于获取系统进程，cpu、内存、磁盘等资源利用率等性能指标，
常常用于系统监控，性能分析和对资源进程的管理。

# 二、CPU

获取cpu完整信息，相关方法如下：

```python
print(f"cpu详细信息 ： {psutil.cpu_times()}")
print(f"cpu分配在单个用户程序上的执行时间（时间片）： {psutil.cpu_times().user}")
# print(f"cpu分配在单个用户程序上的io等待时间(iowait属性针对linux系统)：{psutil.cpu_times().iowait}")
print(f"获取cpu逻辑个数： {psutil.cpu_count()}")
print(f"获取cpu物理个数： {psutil.cpu_count(logical=False)}")
# print(f"获取平均系统负载(元组的形式返回最近1、5和15分钟内的平均系统负载)：{psutil.getloadavg()}")
print(f"获取cpu使用率： {psutil.cpu_percent()}")
print(f"获取cpu使用率,interval不为0时指定的是计算cpu使用率的时间间隔,\n不为0时,则阻塞时显示interval执行的时间内的平均利用率： {psutil.cpu_percent(interval=1)}")
print(f"获取cpu使用率,percpu指定是选择总的使用率或者每个cpu的使用率,为True时显示所有物理核心的利用率： {psutil.cpu_percent(percpu=True)}")
print("=====1.指定计算cpu使用率的时间间隔1s内平均使用率,打印10次===")
# print(f'{[psutil.cpu_percent(interval=1) for i in range(10)]}')
print('=========================done=======================')
print("=====2.模拟top命令的CPU使用率，每秒刷新一次，累计10次===")
# print(f'{[psutil.cpu_percent(interval=1,percpu=True) for i in range(10)]}')
print('=========================done=======================')
print(f"获取cpu统计信息(输出上下文切换，中断，软中断和系统调用次数)： {psutil.cpu_stats()}")
print(f"获取cpu频率： {psutil.cpu_freq()}")
print(f"获取cpu耗时比例： {psutil.cpu_times_percent()}")

```

输出:

![image-20221023213104946](python模块psutil.assets/image-20221023213104946.png)

# 三、Memory

```python
print('=========================Memory=======================')
print(
    f"获取内存使用情况(含total总内存，available还可以使用的内存, percent实际已经使用的内存占比, used已经使用的内存，free剩余内存, (单位为字节))：\n {psutil.virtual_memory()}")
print(f"获取系统交换内存(swap)统计信息： {psutil.swap_memory()}\n")

# Disks (磁盘的利用率, io等)
print('=========================Disks=======================')
print(f"获取磁盘分区信息： {psutil.disk_partitions()}")
print(f"获取路径所在磁盘的使用情况： {psutil.disk_usage('d:')}")
print("""获取io统计信息：
        read_count(读IO数)
        write_count(写IO数)
        read_bytes(读IO字节数)
        write_bytes(写IO字节数)
        read_time(磁盘读时间)
        write_time(磁盘写时间)\n"""
      f"{psutil.disk_io_counters()}")
print(f"获取单个分区的io和读写信息： {psutil.disk_io_counters(perdisk=True)}\n")
```



# 四、Network

```python
print('=========================Network=======================')
print("""获取网卡io统计信息：
        收发字节数
        收发包的数量
        出错的情况
        删包情况\n"""
      f"{psutil.net_io_counters()}")

print(f"\n获取网络接口信息(网卡的配置信息，包括IP地址和mac地址、子网掩码和广播地址)：\n {psutil.net_if_addrs()} \n")
print(f"获取网络接口状态信息(网卡的详细信息，包括是否启动、通信类型、传输速度与mtu)：\n {psutil.net_if_stats()}")
print(f"\n获取当前网络连接信息：\n {psutil.net_connections()}")
```



# 五、Other system info

```python
# print(f"\n获取硬件的信息(linux,macos)：\n {psutil.sensors_temperatures()}")
# print(f"\n获取电池状态(linux)：\n {psutil.sensors_fans()}")
print(f"\n获取风扇速度：\n {psutil.sensors_battery()}")
# print(f"\n获取硬件温度(linux,macos)：\n {psutil.sensors_temperatures()}")
```



# 六、Process management

```python
print(f"\n获取系统全部进程：\n {psutil.pids()}")
print(f"\n查看系统单个进程Process(pid)：\n {psutil.Process(0)}")
print(f'\n获取单个进程对象的其他属性：')
print(""" p = psutil.Process(pid)
进程名 : p.name()
进程的bin路径 : p.exe()
进程的工作目录绝对路径 : p.cwd()
进程启动的命令行 : p.cmdline()
父进程ID : p.ppid()
父进程 : p.parent()
子进程列表 : p.children()
进程的子进程个数 : p.num_threads()
进程状态 : p.status()
进程创建时间 : p.create_time()
进程uid信息 :  p.uids()
进程的gid信息 : p.gids()
进程使用cpu时间信息,包括user,system两个cpu信息 : p.cpu_times()
get进程cpu亲和度 : p.cpu_affinity()
进程内存利用率 : p.memory_percent()
进程使用的内存rss,vms信息  : p.memory_info()
进程的IO信息,包括读写IO数字及参数 : p.io_counters()
进程相关网络连接 : p.connections()
进程开启的线程数 : p.num_threads()
所有线程信息 : p.threads()
进程终端 : p.terminal()
进程打开的文件 : p.open_files()
进程环境变量 : p.environ()
发送SIGTEAM信号结束进程 : p.terminate()
发送SIGKILL信号结束进程 : p.kill()
进程是否在运行  : p.is_running()
进程打开的文件个数 :  p.num_fds()
判断进程是否正在运行 : p.is_running()
""")
```



跟踪某个应用程序进程，常使用psutil的Popen方法，结合管道PIPE进行处理。
