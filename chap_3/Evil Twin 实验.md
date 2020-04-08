# Evil Twin实验

## 实验目的

* 理解 `Evil Twin` 攻击原理并了解使用常见工具进行 `Evil Twin` 攻击的基本方法；

## 实验环境

- 可以开启监听模式、AP 模式和数据帧注入功能的 USB 无线网卡；
- Kali 虚拟机；
- python scapy；
- aircrack-ng系列软件；
- Wireshark；
- 搭建 **被攻击网络** 所需要使用到的「无线 AP」或「无线路由器」；

sudo airmon-ng stop wlan0mon

rfkill ubblock

## 实验过程

* 按照老师给的实验步骤进行AP配置https://c4pr1c3.github.io/cuc-mis/chap0x03/exp.html

<img src="image\1.png" />

* 在.conf文件中进行配置，修改ssid与密码进行伪装，与自己搭建的无线网络一致，进行隐藏（**这里由于无法辨认，对ssid进行了一些修改**）

<img src="image\10.png" />

* 更改apache服务器的index.html，导入已写入的网页，开启服务

  ```
  /etc/init.d/apache2 start
  ```

  结果如图

<img src="image\20.png" />

* 查看本机ip设置，如下图所示

<img src="image\21.png" />

* 测试其他主机能否访问，结果成功，如图

<img src="image\22.png" />

* 更改dnsmasq配置文件内容，由于客户连入此网络时dns服务器也为搭建的虚拟机，故可设置dns文件使taobao.com的地址为指定ip（此处为虚拟机自己搭建的网页ip）

<img src="image\23.png" />

* 使用手机连入此网络，使用safari浏览器（已提前清空缓存）访问淘宝，可以看到访问taobao.com时，显示的是用户登录界面（自己搭建的html），若用户输入身份信息即可窃取

<img src="image\24.png" />

* 查看抓包数据，过滤条件为`dns`，发现dns服务器（虚拟机：10.10.10.1）在手机（10.10.10.162）访问taobao.com时返回的ip为192.168.56.103，即虚拟机的ip地址，说明实现了DNS 欺骗

<img src="image\25.png" />

## 遇到的问题

* 启动hostapd（调试模式启动）时报错

<img src="image\0.png" />

编辑时误将命令也写入.conf文件，修改后继续报错`nl80211: Could not configure driver mode`

<img src="image\2.png" />

使用 `airmon-ng check kill`，重试即可

* 其他主机无法访问攻击者主机搭建的服务器

解决办法：关闭防火墙，在虚拟机中增加网卡2:host-only

> Host-Only模式其实就是NAT模式去除了虚拟NAT设备，然后使用VMware Network Adapter VMnet1虚拟网卡连接VMnet1虚拟交换机来与虚拟机通信的，Host-Only模式将虚拟机与外网隔开，使得虚拟机成为一个独立的系统，只与主机相互通讯。

## 参考资料

1.https://blog.csdn.net/f8qg7f9yd02pe/article/details/87927697 （**Evil-Twin 框架：一个用于提升 WiFi 安全性的工具 | Linux 中国**）

