# Spring MVC的请求过程

Spring MVC的整个流程如下图所示：

首先，请求的第一站是DispatcherServlet。DispatcherServlet在此充当一个前端控制器（front controller）的角色。所有的请求都经由DispatcherServlet，它将请求转发到其他组件再做相应的处理。此处的DispatherServlet是一个单实例的Servlet。

DispatcherServlet的任务是将请求发送到控制器（controller）。控制器是一个用于处理请求的Spring组件，通常存在多个控制器，所以DispatcherServlet需要知道将请求发送给哪个控制器。所以DispatcherServlet会去查询处理器映射（handler mapping），来确定下一站在哪。处理器映射会根据请求携带的URL进行决定。

找到了合适的控制器后，DispatcherServlet会将请求发送给控制器。控制器完成处理后，通常会产生一些信息，这些信息被称为模型（model）。信息的可视化处理需要发送给一个视图（view），通常是JSP。

控制器将模型数据打包，并标识出用于渲染输出的视图名，然后将其发送给DispatcherServlet。DispatcherServlet接收到后，使用视图解析器（view resolver）将逻辑的视图名匹配为一个特定的视图实现。最后，视图将模型数据渲染，输出，并返回给客户端。

![](http://oqag5mdvp.bkt.clouddn.com/201804161409_586.jpg)