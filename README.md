# irqbalance

rocky 9.2 irqbalance 解析

```
Something I hope you know before go into the coding~
First, please watch or star this repo, I'll be more happy if you follow me.
Bug report, questions and discussion are welcome, you can post an issue or pull a request.
```


```
Name         : irqbalance
Epoch        : 2
Version      : 1.9.0
Release      : 3.el9
Architecture : x86_64
Size         : 124 k
Source       : irqbalance-1.9.0-3.el9.src.rpm
Repository   : @System
From repo    : minimal
Summary      : IRQ balancing daemon
URL          : https://github.com/Irqbalance/irqbalance
License      : GPLv2
Description  : irqbalance is a daemon that evenly distributes IRQ load across
             : multiple CPUs for enhanced performance.
File list    :
  /etc/sysconfig/irqbalance
  /usr/lib/.build-id
  /usr/lib/.build-id/55
  /usr/lib/.build-id/55/eebbe7c155ba9d5cf8d06995a6bcb77d06abc2
  /usr/lib/.build-id/d6
  /usr/lib/.build-id/d6/8be977fde08f734ac763d9b1aff46f359ea3b7
  /usr/lib/systemd/system/irqbalance.service
  /usr/sbin/irqbalance
  /usr/sbin/irqbalance-ui
  /usr/share/doc/irqbalance
  /usr/share/doc/irqbalance/AUTHORS
  /usr/share/doc/irqbalance/COPYING
  /usr/share/man/man1/irqbalance.1.gz

```




## 介绍

irqbalance这个服务的作用是帮助平衡系统中各个CPU的中断负载。中断是一种硬件设备通知CPU发生了某些事件的机制，比如网卡收到了数据包，或者键盘按下了某个键。
中断处理需要消耗CPU的时间和资源，如果所有的中断都由一个CPU来处理，那么会导致该CPU过载，而其他CPU空闲，这样就浪费了多核的优势，也影响了系统的性能。

irqbalance是一个后台程序，它会自动收集系统的信息，分析中断的来源和频率，然后根据系统的负载情况，将中断尽可能均匀地分配给各个CPU核心，以充分利用CPU的多核能力，提高性能。
irqbalance还会考虑CPU的缓存命中率和NUMA架构的内存访问延迟等因素，尽量将中断分配给最适合处理它的CPU。

irqbalance有一些参数可以用来调整它的行为，比如：

* –powerthresh：设置多少个CPU可以空闲后进入省电模式。在省电模式下，一个CPU不会参与中断处理，以避免被不必要地唤醒。
* –hintpolicy：设置如何处理内核对中断亲和性的提示。有效值有exact（总是应用提示），subset（将中断分配给提示的子集），或ignore（完全忽略提示）。
* –policyscript：设置一个脚本的位置，该脚本会对每个中断执行，并返回一些键值对来指导irqbalance如何管理该中断。比如ban（是否禁止该中断被平衡），balance_level（该中断的平衡级别），或numa_node（该中断所属的NUMA节点）。
* –banirq：设置一个或多个要禁止平衡的中断号。

```
# /usr/lib/systemd/system/irqbalance.service
[Unit]
Description=irqbalance daemon
Documentation=man:irqbalance(1)
Documentation=https://github.com/Irqbalance/irqbalance
ConditionVirtualization=!container
ConditionCPUs=>1

[Service]
EnvironmentFile=-/usr/lib/irqbalance/defaults.env
EnvironmentFile=-/etc/sysconfig/irqbalance
ExecStart=/usr/sbin/irqbalance --foreground $IRQBALANCE_ARGS
ReadOnlyPaths=/
ReadWritePaths=/proc/irq
RestrictAddressFamilies=AF_UNIX
RuntimeDirectory=irqbalance/

[Install]
WantedBy=multi-user.target
```

strace 查看，可以发现，周期行读取/proc/interrupts /proc/stat

```
openat(AT_FDCWD, "/proc/interrupts", O_RDONLY) = 6
newfstatat(6, "", {st_mode=S_IFREG|0444, st_size=0, ...}, AT_EMPTY_PATH) = 0
read(6, "           CPU0       CPU1      "..., 1024) = 1024
read(6, " acpi\n 12:          0          0"..., 1024) = 1024
read(6, "         0          0          0"..., 1024) = 1024
read(6, "30:          0          0       "..., 1024) = 1024
read(6, "        0          0          0 "..., 1024) = 1024
read(6, "        0          0          0 "..., 1024) = 1024
read(6, "_hcd\n 44:          0          0 "..., 1024) = 1024
read(6, "          0          0          "..., 1024) = 1024
read(6, "         0          0          0"..., 1024) = 1024
read(6, "-MSI 2097158-edge      virtio1-r"..., 1024) = 1024
read(6, "       0          0        464  "..., 1024) = 1024
read(6, "\n 67:          0          0     "..., 1024) = 1024
read(6, "   0          0          0      "..., 1024) = 1024
close(6)                                = 0
openat(AT_FDCWD, "/proc/stat", O_RDONLY) = 6
newfstatat(6, "", {st_mode=S_IFREG|0444, st_size=0, ...}, AT_EMPTY_PATH) = 0
read(6, "cpu  19320 510 14588 4275392 891"..., 1024) = 1024
read(6, "0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 "..., 1024) = 984
close(6)                                = 0
```


## 目录







---
