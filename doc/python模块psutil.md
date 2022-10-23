# 一、psutil简介

一种跨平台库，作用：用于获取系统进程，cpu、内存、磁盘等资源利用率等性能指标，
常常用于系统监控，性能分析和对资源进程的管理。

# 二、CPU

获取cpu完整信息，相关方法如下：

```python
print(f"cpu详细信息：{psutil.cpu_times()}")
print(f"cpu分配在单个用户程序上的执行时间（时间片）：{psutil.cpu_times().user}")
# print(f"cpu分配在单个用户程序上的io等待时间(iowait属性针对linux系统)：{psutil.cpu_times().iowait}")
print(f"获取cpu逻辑个数：{psutil.cpu_count()}")
print(f"获取cpu物理个数：{psutil.cpu_count(logical=False)}")
# print(f"获取平均系统负载(元组的形式返回最近1、5和15分钟内的平均系统负载)：{psutil.getloadavg()}")
print(f"获取cpu使用率：{psutil.cpu_percent()}")

```







