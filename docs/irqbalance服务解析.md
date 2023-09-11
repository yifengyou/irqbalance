# irqbalance服务解析

```
# systemctl cat irqbalance
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

其中

1. ConditionVirtualization=!container 

表示服务只在非容器化的虚拟化环境中启动，如果系统运行在一个容器中，比如Docker或者LXC，那么服务不会启动。

2. ConditionCPUs=>1

表示服务只在有多于一个CPU核心的系统中启动，如果系统只有一个CPU核心，那么服务不会启动。

3. ReadWritePaths

```ReadWritePaths=```是systemd的service文件中的一个字段，它的作用是指定一个或多个目录或文件，这些目录或文件在执行服务进程时可以被读写。
这个字段可以用来限制服务进程对文件系统的访问权限，提高安全性。

例如，如果一个服务只需要读写/var/lib/foo目录，那么可以设置ReadWritePaths=/var/lib/foo，这样服务进程就不能修改其他目录或文件了。

```ReadWritePaths=```的值必须是绝对路径，可以使用冒号分隔多个路径。

```ReadWritePaths=```是ProtectSystem=, ProtectHome=, ReadOnlyPaths=, InaccessiblePaths=等字段的补充，它们都可以用来控制服务进程的文件系统视图

4. RestrictAddressFamilies=AF_UNIX 

表示服务进程只能使用Unix域套接字进行网络通信，不能使用其他类型的套接字，比如IPv4或IPv6。这个字段可以用来限制服务进程的网络访问权限，提高安全性。

5. RuntimeDirectory=irqbalance/

表示服务进程启动时，会在/run目录下创建一个名为irqbalance的子目录，并将其作为服务进程的工作目录。
服务进程可以在这个目录下存储一些运行时的数据或状态信息。当服务进程停止时，这个目录会被自动删除。这个字段可以用来简化服务进程的文件系统视图，避免污染其他目录。

与代码中定义一致：

```
irqbalance.h:168:#define SOCKET_TMPFS "/run/irqbalance"
ui/irqbalance-ui.h:11:#define SOCKET_TMPFS "/run/irqbalance"
```

6. EnvironmentFile=-/etc/sysconfig/irqbalance 
   
这个字段的作用是从/etc/sysconfig/irqbalance文件中读取环境变量，并将它们设置给服务进程。
这个文件可以包含一些服务进程需要的配置参数，比如IRQBALANCE_ONESHOT，IRQBALANCE_BANNED_CPUS等。

这个字段前面的```-```符号的意义是，如果这个文件不存在或者不可读，那么systemd不会报错，而是忽略这个字段。这样可以避免一些不必要的失败。

如果没有-符号，那么systemd会检查文件的存在和可读性，如果不满足，那么服务进程就无法启动



## 配置文件

```
# irqbalance is a daemon process that distributes interrupts across
# CPUS on SMP systems. The default is to rebalance once every 10
# seconds. This is the environment file that is specified to systemd via the
# EnvironmentFile key in the service unit file (or via whatever method the init
# system you're using has.
#
# ONESHOT=yes
# after starting, wait for a minute, then look at the interrupt
# load and balance it once; after balancing exit and do not change
# it again.
#IRQBALANCE_ONESHOT=

#
# IRQBALANCE_BANNED_CPUS
# 64 bit bitmask which allows you to indicate which cpu's should
# be skipped when reblancing irqs. Cpu numbers which have their
# corresponding bits set to one in this mask will not have any
# irq's assigned to them on rebalance
#
#IRQBALANCE_BANNED_CPUS=

#
# IRQBALANCE_ARGS
# append any args here to the irqbalance daemon as documented in the man page
#
#IRQBALANCE_ARGS=

```

* IRQBALANCE_ONESHOT：设置为1时，表示irqbalance服务只运行一次，然后退出。默认为0，表示irqbalance服务会周期性地运行。
* IRQBALANCE_BANNED_CPUS：设置一个或多个要禁止平衡的CPU核心的十六进制掩码，例如```IRQBALANCE_BANNED_CPUS=0000ff00```表示将8~15这8个CPU核心从守护进程中脱离出来。
* IRQBALANCE_IRQS：设置一些要禁止平衡的中断号，用逗号分隔，例如```IRQBALANCE_IRQS=44,45```表示禁止平衡44和45这两个中断。
* IRQBALANCE_ARGS：设置一些额外的参数给irqbalance服务，例如IRQBALANCE_ARGS="–powerthresh=10"表示设置多少个CPU可以空闲后进入省电模式。
* IRQBALANCE_BANNED_INTERRUPTS：设置一些要禁止平衡的中断号，用空格分隔，例如IRQBALANCE_BANNED_INTERRUPTS="44 45"表示禁止平衡44和45这两个中断。这个字段已经被IRQBALANCE_IRQS替代，不建议使用。



---