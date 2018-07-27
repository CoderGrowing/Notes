# JSP 和 Servlet

## 一、容器

### 1. 什么是容器

由于 servlet 没有 main() 方法，它们会受控于另一个 Java 应用，这个 Java 应用就是容器。当 Web 服务器得到指向 servlet 请求时，并不将请求交给 servlet，而是将请求交给容器，由容器调用该 servlet 的方法，如 doGet()。

### 2. 容器提供了什么

- 通信支持：无需建立套接字、监听端口等
- 生命周期管理：控制 Servlet 的生与死
- 多线程支持：自动的我每个 Servlet 请求创建一个新的 Java 线程
- JSP 支持：将 JSP 翻译为 Java

### 3. 工作流程

1. 容器拿到对 servlet 的请求后，创建 `HttpServletResponse` 和 `HttpServletRequest` 对象
2. 容器根据请求 URL 找到对应的 servlet，为这个请求分配一个线程并将这两个对象交给 servlet
3. 容器调用 servlet 的 `service()` 方法，根据请求的不同 `service()` 方法会调用 `doGet()`或者 `doPost()`
4. `doGet()` 方法生成动态页面，并将页面写入响应对象
5. 线程结束，容器将响应对象转化为 HTTP 相应，并发给客户，删除请求和响应对象

## 二、Servlet

### 1. Servlet 是什么

Servlet 其实就是一个接口，定义了五个方法。

![](https://pic2.zhimg.com/80/v2-85bf84640fbc6b6e195b9c5b513b918f_hd.jpg)

### 2. Servlet 的生命周期

- init()：servlet 实例创建后，在提供服务（调用 doGet() 等方法之前）需要执行 init() 方法
- service()：第一个请求到来时，容器分配新的线程，调用 service()
- doGet() 或者 doPost()：service 方法根据请求的方式来调用

每一个**请求**都在一个单独的线程中运行。

### 3. ServletConfig

```java
public interface ServletConfig {
    String getServletName();			   // 不常用
    
    ServletContext getServletContext();     // 访问 ServletContext
   
    String getInitParameter(String var1);	// 得到初始化参数
    
    Enumeration<String> getInitParameterNames();
}
```

**每个 servlet 都有一个 ServletConfig 对象**，用于向 servlet 传递部署信息、初始化参数（部署描述文件中配置）、访问 ServletContext 等。

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

在 Servlet 代码中可以使用 ServletConfig 来获取参数：

```java
getServletConfig().getInitParameter("ParamName");
```

### 4. ServletContxt

**每个 Web 应用对应一个 ServletContext**，用于访问 Web 应用参数（部署描述文件中配置）。

```xml
<context-param>
    <param-name>ParamName</param-name>
    <param-value>Value</param-value>
</context-param>
```

上下文参数利用 ServletContext 获取：

```java
getServletContext().getInitParameter("ParamName");
```

上下文参数对于整个 Web 应用可用。

## 三、请求和响应

容器得到对 Servlet 的请求时，会创建 `HttpServletRequest`和 `HttpServletResponse` 对象，分别代表请求和响应，并将这两个对象传递给 Servlet。`HttpServletResponse`和 `HttpServletRequest` 是两个接口，由容器来实现。

### 1. HttpServletRequest

HttpServletRequest 中的方法与 HTTP 有关，用于获取请求信息。常用方法：

```java
String getContextPath();
Cookie[] getCookies();
String getHeader();
String getQueryString();
HttpSession getSession();
……
```

### 2. HttpServletResponse

用于设置响应信息。

```java
void addCookie();
void addHeader(String name, String value);
void sendError(int Code);
……
```

### 3. 请求分派和重定向

**重定向**（sendRedirect）让浏览器完成工作：将请求重定向到其他 URL，浏览器显示的 URL 会变。注意，**不能在写到响应之后再调用 `sendRedirect()`**。

**请求分派**在服务器端完成工作，要求服务器上的某个对象来处理请求。浏览器上的 URL 不变。

```java
RequestDispatcher view = request.getRequestDispathcer("some.jsp");
view.forward(request, response);
```

### 4. GET 和 POST

- POST 有一个消息体，GET 只有请求头
- GET 幂等（还有 PUT、HEAD)，POST 不幂等（幂等，反复做一件事情而没有副作用）

### 5. 线程安全

- 上下文属性非线程安全（对上下文使用 synchronized）
- HttpSession 非线程安全（对 HttpSession 使用 synchronized）
- SingleThreadModel：用来保护实例变量，**保证不会在该 servlet 的服务方法中并发执行两个线程**。（已被废弃）
- 带来了并发请求的问题：多个请求时 servlet 如何处理，排队 / 通过一个池发送请求。选择池的话 servlet 无法保证单例
- 请求属性和局部变量是线程安全的

### 四、会话

HTTP 的连接是无状态的，Web 服务器无法区分两次请求是否来自同一个客户。为了保留同一个客户的信息，引入了会话的概念。

### 1. 如何标识

客户的第一次请求，生成一个唯一的 ID，并返回给客户，客户在以后的每次请求都中发回这个会话 ID

### 2. 如何实现

cookies，发送 cookie 或从请求得到会话 ID 都由容器进行，只需要

```java
HttpSession session = request.getSession();
```

**判断会话已经存在 / 刚刚创建**

`session.isNew()`

**不接受 cookies 的处理办法：URL 重写**

如果客户端不接受 cookie，可以利用 URL 重写来完成会话的功能，将请求的 URL 加上一个标识 ID，如 `http://www.baidu.com;JSESSIONID=123456`。

对于 Servlet 来说，URL 重写需要用 `response.encodeURL(\'/BeerTest.do\')` 来实现，容器自己判断 cookies 是否可用，不可用利用 URL 重写来完成功能。

### 3. 使用会话

```java
Cookie cookie = new Cookie("username", name);   // 新建一个 Cookie
cookie.
```



### 4. 删除会话

当一个会话超时后服务器将其自动删除。我们只需要配置会话的超时时间。

利用配置文件进行配置：

```xml
<session-config>
	<session-timeout>15</session-timeout>
</session-config>
```

利用 Servlet 来进行配置：

```java
session.setMaxInactiveInterval(20 * 60);
```

需要注意配置文件中的单位为分钟，Servlet 中的为秒。

## 四、JSP

### 1. JSP 会成为 Servlet

**JSP 最终会被容器翻译为一个 Servlet。**

对应的 servlet 方法

- **jspinit()**：由 init 方法调用
- **JSPDestroy()**：由 servlet 的 destroy 方法调用
- **_jspService()**：由 service() 方法调用，JSP 中写的 Java 代码会放在其中，无法覆盖

### 2. JSP 中的元素

- **scriptlet**：即放在 \<%\...%\> 标记中的 java 代码
- **指令**：共有三个，taglib、page 和 include \<%@ page \...%\>
  - taglib：定义 JSP 可以使用的标记库，如 JSTL。
  - page：定义页面特有的属性，如字符编码、页面响应的内容类型等。一共有 13 个属性。
  - include：定义在转换时增加到当前页面的文本和代码
- **声明**：<% int i = 0; %\> 声明类变量：\<%! int i = 0; %\>
- **Java 表达式**：<%= i %\> 表达式会被作为 out.print() 的参数，所以不加分号
- **EL 表达式**
- **动作：**<jsp:include ....>
- **注释：**<%\--JSP\--%\>

### 3. JSP 中的隐式对象

- **out**
- **request**：HttpServletRequest
- **response**：HttpServletResponse
- **session**：HttpSession
- **application**：ServletContext
- **config**：ServletConfig
- **exception**
- **pageContext**：页面作用域，封装了其他隐式对象，所以如果提供一个 pageContext 引用就可以利用这个引用得到其他作用域的属性
- **page**

### 4. useBean

```jsp
<jsp:useBean id="person" class="com.test.Person" scope="request" />
Her name is: <jsp:getProperty name="person" property="name" />
```

在 JSP 中应当尽量避免使用 Java 语句，如果不使用 useBean 上述代码会变为：

```jsp
<% Person p = (Person) request.getAttribute("person"); %>
<%= p.getName() %>
```



## 五、EL

EL 是表达式语言（Expression Language）的简写，EL 的出现是为了将 Java 代码从 JSP 中驱逐出去。

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

JSTL（JSP 标准标记库，JSP Standard Tag Library）打包了一组常用的定制标记。

### 过滤器

过滤器可以在请求被 servlet 处理之前进行处理。

**生命周期**

- init()：在 init 方法中完成所有初始化任务。
- doFilter()：真正的处理在这个方法中完成。有三个参数：ServletRequest、ServletResponse 和 FilterChain。
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
<!-- 声明 URL 模式的过滤器映射 -->
<filter-mapping>
	<filter-name>BeerRequest</filter-name>
    <url-pattern>*.do</url-pattern>
</filter-mapping>

<filter-mapping>
	<filter-name>BeerRequest</filter-name>
    <servlet-name>AdviceServlet</servlet-name>
</filter-mapping>
```

