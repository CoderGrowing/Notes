# Spring MVC 的关键组件

#### 配置

除了普通的 J2EE 程序会用到的 web.xml 文件之外，Spring MVC 程序还用到了两个额外的配置文件：dispatcher-servlet.xml 和 applicationContext.xml。

**ContextLoaderListener**

首先从 web.xml 出发，定义 ContextLoaderListener：

```xml
<context-param>
	<param-name>contextConfigLocation</param-name>
	<param-value>classpath:/applicationContext.xml</param-value>
</context-param>
<listener>
	<listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
</listener>
```

ContextLoaderListener 的职责在于启动 Web 容器时，根据 applicationContext.xml 文件的定义为整个的 Web 应用程序加载顶层的 WebApplicationContext（ROOT WebApplicationContext）。

 通过 `<context-parm>` 指定了配置文件的位置，通过 `<listener>` 元素指定了具体的 ContextLoaderListener 类。该顶层 WebApplicationContext 主要提供应用的中间层服务，如数据源定义、数据访问对象定义、服务对象定义等。

ContextLoaderListener 加载的 WebApplicationContext 默认配置路径为 /WEB-INF/applicationContext.xml。

**DispatcherServlet**

假设我们在 web.xml 文件中有如下的 DispatcherServlet 定义：

```xml
<servlet>
	<servlet-name>dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
</servlet>
```

那么对应的配置文件就应该为：/WEB-INF/dispatcher-servlet.xml。即 servlet-name 的值再加上 "-servlet.xml"。

DispatcherServlet 启动后加载配置文件，并构建相应的 WebApplicationContext，该 WebApplicationContext 将之前通过 ContextLoaderListener 加载的顶层 WebApplicationContext 作为父容器。

基于 Java 的配置：

```java
public class MyAppInitializer extends AbstractAnnotationConfigDispatcherServletInitializer {
    @Override
    protected Class<?>[] getRootConfigClasses() {    // 指定配置类
        return new Class<?>[] { RootConfig.class };
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[] { WebConfig.class };
    }
 
    @Override
    protected String[] getServletMappings() {     //  将 DispatcherServlet 映射到 /
        return new String[] { "/" };
    }
}
```





首先，请求的第一站是 DispatcherServlet。DispatcherServlet 在此充当一个前端控制器（front controller）的角色。所有的请求都经由 DispatcherServlet，它将请求转发到其他组件再做相应的处理。此处的 DispatherServlet 是一个单实例的 Servlet。

DispatcherServlet 的任务是将请求发送到控制器（controller）。控制器是一个用于处理请求的 Spring 组件，通常存在多个控制器，所以 DispatcherServlet 需要知道将请求发送给哪个控制器。所以 DispatcherServlet 会去查询处理器映射（handler mapping），来确定下一站在哪。处理器映射会根据请求携带的 URL 进行决定。

找到了合适的控制器后，DispatcherServlet 会将请求发送给控制器。控制器完成处理后，通常会产生一些信息，这些信息被称为模型（model）。信息的可视化处理需要发送给一个视图（view），通常是 JSP。

控制器将模型数据打包，并标识出用于渲染输出的视图名，然后将其发送给 DispatcherServlet。DispatcherServlet 接收到后，使用视图解析器（view resolver）将逻辑的视图名匹配为一个特定的视图实现。最后，视图将模型数据渲染，输出，并返回给客户端。

![](http://oqag5mdvp.bkt.clouddn.com/201804161409_586.jpg)