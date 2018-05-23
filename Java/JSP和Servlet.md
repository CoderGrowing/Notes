## JSP和Servlet

### 容器

#### 什么是容器

由于servlet没有main()方法，它们会受控于另一个Java应用，这个Java应用就是容器。当Web服务器得到指向servlet请求时，并不将请求交给servlet，而是将请求交给容器，由容器调用该servlet的方法，如doGet()。

#### 容器提供了什么

- 通信支持：无需建立套接字、监听端口等
- 生命周期管理：控制Servlet的生与死
- 多线程支持：自动的我每个Servlet请求创建一个新的Java线程
- JSP支持：将JSP翻译为Java

#### 工作流程

1. 容器拿到对servlet的请求后，创建HttpServletResponse和HttpServletRequest对象
2. 容器根据请求URL找到对应的servlet，为这个请求分配一个线程并将这两个对象交给servlet
3. 容器调用servlet的service()方法，根据请求的不同service()方法会调用doGet()或者doPost()
4. doGet()方法生成动态页面，并将页面写入响应对象
5. 线程结束，容器将响应对象转化为HTTP相应，并发给客户，删除请求和响应对象

### Servlet

#### Servlet是什么

Servlet其实就是一个接口，定义了五个方法。

![](https://pic2.zhimg.com/80/v2-85bf84640fbc6b6e195b9c5b513b918f_hd.jpg)

#### 生命周期

- init()：servlet实例创建后，在提供服务（调用doGet()等方法之前）需要执行init()方法
- service()：第一个请求到来时，容器分配新的线程，调用service()
- doGet()或者doPost()：service方法根据请求的方式来调用

每一个请求都在一个单独的线程中运行。

#### ServletConfig

```java
public interface ServletConfig {
    String getServletName();			   // 不常用
    
    ServletContext getServletContext();     // 访问ServletContext
    
    String getInitParameter(String var1);	// 得到初始化参数
    
    Enumeration<String> getInitParameterNames();
}
```

**每个servlet都有一个ServletConfig对象**，用于向servlet传递部署信息、初始化参数（部署描述文件中配置）、访问ServletContext等。

```xml
<servlet>
	<servlet-name>MyServlet</servlet-name>
    <servlet-class>Test</servlet-class>
    
    <init-param>
    	<param-name>ParamName</param-name>
        <param-value>Value</param-value>
    </init-param>
</servlet>
```

在Servlet代码中可以使用ServletConfig来获取参数：

```java
getServletConfig().getInitParameter("ParamName");
```

#### ServletContxt

**每个Web应用对应一个ServletContext**，用于访问Web应用参数（部署描述文件中配置）。

```xml
<context-param>
    <param-name>ParamName</param-name>
    <param-value>Value</param-value>
</context-param>
```

上下文参数利用ServletContext获取：

```java
getServletContext().getInitParameter("ParamName");
```

上下文参数对于整个Web应用可用。

### 请求和响应

容器得到对Servlet的请求时，会创建HttpServletResponse和HttpServletRequest对象，分别代表请求和响应。并将这两个对象传递个Servlet。HttpServletResponse和HttpServletRequest是两个接口，由容器来实现。

#### HttpServletRequest

HttpServletRequest中的方法与HTTP有关，用于获取请求信息。常用方法：

```java
String getContextPath();
Cookie[] getCookies();
String getHeader();
String getQueryString();
HttpSession getSession();
……
```

#### HttpServletResponse

用于设置响应信息。

```java
void addCookie();
void addHeader(String name, String value);
void sendError(int Code);
……
```

#### 请求分派和重定向

**重定向**（sendRedirect）让浏览器完成工作：将请求重

定向到其他URL，浏览器显示的URL会变

**请求分派**在服务器端完成工作，要求服务器上的某个对象来处理请求。浏览器上的URL不变。

```java
RequestDispatcher view = request.getRequestDispathcer("some.jsp");
view.forward(request, response);
```

#### GET和POST

- POST有一个消息体，GET只有请求头
- GET幂等（还有PUT、HEAD)，POST不幂等

#### 线程安全

- 上下文属性非线程安全（对上下文使用synchronized）
- HttpSession非线程安全（对HttpSession使用synchronized）
- SingleThreadModel：用来保护实例变量，**保证不会在该servlet的服务方法中并发执行两个线程**。（已被废弃）
- 带来了并发请求的问题：多个请求时servlet如何处理，排队/通过一个池发送请求。选择池的话servlet无法保证单例
- 请求属性和局部变量是线程安全的

### 会话

HTTP的连接是无状态的，Web服务器无法区分两次请求是否来自同一个客户。为了保留同一个客户的信息，引入了会话的概念。

#### 如何标识

客户的第一次请求，生成一个唯一的ID，并返回给客户，客户在以后的每次请求都中发回这个会话ID

#### 如何实现

cookies，发送cookie/从请求得到会话ID都由容器进行，只需要

```java
HttpSession session = request.getSession();
```

#### 判断会话已经存在/刚刚创建

`session.isNew()`

#### 不接受cookies的处理办法：URL重写

如果客户端不接受cookie，可以利用URL重写来完成会话的功能，将请求的URL加上一个标识ID，如`http://www.baidu.com;JSESSIONID=123456`。

对于Servlet来说，URL重写需要用`response.encodeURL(\'/BeerTest.do\')`来实现，容器自己判断cookies是否可用，不可用利用URL重写来完成功能。

#### 删除会话

当一个会话超时后服务器将其自动删除。我们只需要配置会话的超时时间。

利用配置文件进行配置：

```xml
<session-config>
	<session-timeout>15</session-timeout>
</session-config>
```

利用Servlet来进行配置：

```java
session.setMaxInactiveInterval(20 * 60);
```

需要注意配置文件中的单位为分钟，Servlet中的为秒。

### JSP

**JSP最终会被容器翻译为一个Servlet。**

#### 对应的servlet方法

- **jspinit()**：由init方法调用
- **JSPDestroy()**：由servlet的destroy方法调用
- **_jspService()**：由service()方法调用，JSP中写的Java代码会放在其中，无法覆盖

#### JSP中的元素

- **scriptlet**：即放在\<%\...%\>标记中的java代码
- **指令**：共有三个，taglib、page和include \<%@ page \...%\>
- **声明**：<% int i = 0; %\> 声明类变量：\<!% int i = 0; %\>
- **Java表达式**：<%= i %\> 表达式会被作为out.print()的参数，所以不加分号
- **EL表达式**
- **动作：**<jsp:include ....>
- **注释：**<%\--JSP\--%\>

#### JSP中的隐式对象

- **out**
- **request**：HttpServletRequest
- **response**：HttpServletResponse
- **session**：HttpSession
- **application**：ServletContext
- **config**：ServletConfig
- **exception**
- **pageContext**：页面作用域，封装了其他隐式对象，所以如果提供一个pageContext引用就可以利用这个引用得到其他作用域的属性
- **page**

### EL

EL是表达式语言（Expression Language）的简写，EL的出现是为了将Java代码从JSP中驱逐出去。

#### 隐式对象

- **pageScope**
- **requestScope**
- **sessionScope**
- **applicationScope**
- **param**
- **paramValues**
- **header**
- **headerValues**
- **cookie**
- **initParam**
- **pageContext**

**param**

```html
<form action="someAction">
    <input type="text" name="name">
    <input type="password" name="password">
    <input type="submit">
</form>
```

得到请求中的参数：

```jsp
name is: ${param.name}
password is : ${param.password}
```

### JSTL

JSTL（JSP标准标记库，JSP Standard Tag Library）打包了一组常用的定制标记。

### 过滤器

过滤器可以在请求被servlet处理之前进行处理。

**生命周期**

- init()：在init方法中完成所有初始化任务。
- doFilter()：真正的处理在这个方法中完成。有三个参数：ServletRequest、ServletResponse和FilterChain。
- destroy()：完成销毁工作。

**声明过滤器**

```xml
<filter>
	<filter-name>BeerRequest</filter-name>
    <filter-class>com.example.web.BeerRequestFilter</filter-class>
    <init-param>
        <param-name>LogFileName</param-name>
        <param-value>UserLog.txt</param-value>
    </init-param>
</filter>
```

**声明对应的映射**

```xml
<!--声明URL模式的过滤器映射-->
<filter-mapping>
	<filter-name>BeerRequest</filter-name>
    <url-pattern>*.do</url-pattern>
</filter-mapping>

<filter-mapping>
	<filter-name>BeerRequest</filter-name>
    <servlet-name>AdviceServlet</servlet-name>
</filter-mapping>
```

