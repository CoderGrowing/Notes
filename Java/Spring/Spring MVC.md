# Spring MVC

## 1. Spring MVC 的请求过程

每当用户在 Web 浏览器中点击 URL 或者提交表单的时候，请求就开始工作了。在 Spring MVC 应用中，请求会经过很多站点。

首先，请求的第一站是 DispatcherServlet。DispatcherServlet 在此充当一个前端控制器（front controller）的角色。所有的请求都经由 DispatcherServlet，它将请求转发给具体的控制器来处理。

DispatcherServlet 的任务是将请求发送到控制器（controller）。控制器是一个用于处理请求的 Spring 组件，通常存在多个控制器，所以 DispatcherServlet 需要知道将请求发送给哪个控制器。DispatcherServlet 会去查询处理器映射（handler mapping），来确定下一站在哪。处理器映射会根据请求携带的 URL 进行决定。

找到了合适的控制器后，DispatcherServlet 会将请求发送给控制器。控制器完成处理后，通常会产生一些信息，这些信息被称为模型（model）。信息的可视化处理需要发送给一个视图（view），通常是 JSP。

控制器将模型数据打包，并标识出用于渲染输出的视图名，然后将其发送给 DispatcherServlet。DispatcherServlet 接收到后，使用视图解析器（view resolver）将逻辑的视图名匹配为一个特定的视图实现。最后，视图将模型数据渲染，输出，并返回给客户端。

![](http://oqag5mdvp.bkt.clouddn.com/201804161409_586.jpg)

## 2. 搭建 Spring MVC

### 2.1 使用 Java 搭建

从 Spring MVC 的请求过程可以看出 DispatcherServlet 在 Spring MVC 中扮演了一个十分重要的角色。所以搭建Spring MVC 的第一步就是配置 DispatcherServlet。

配置 DispatcherServlet 只需要扩展`AbstractAnnotationConfigDispatcherServletInitializer` 类即可。扩展了该类的子类会自动配置 DispatcherServlet 和 Spring 应用上下文。

```java
public class SpittrWebAppInitializer  extends AbstractAnnotationConfigDispatcherServletInitializer{

    @Override
    protected String[] getServletMappings() {
        return new String[] {"/"};
    }

    @Override
    protected Class<?>[] getRootConfigClasses() {
        return new Class<?>[] { RootConfig.class };
    }

    @Override
    protected Class<?>[] getServletConfigClasses() {
        return new Class<?>[] { WebConfig.class};
    }
}
```

扩展这个类需要重写三个方法。第一个方法是 `getServletMappings`，它会将一个或多个路径映射到 DispatcherServlet 上。如果映射的是“ / ”的话，表明是默认的 Servlet，会处理所有请求。而另外两个方法则与 Spring 程序的应用上下文有关。

当DispatcherServlet 启动时，它会创建 Spring 应用上下文，并且加载配置文件或配置类中的Bean。在上述代码中，我们要求 DispatcherServlet 加载应用上下文时使用定义在 WebConfig 配置类中的 Bean。

而在 Spring Web 应用中通常会有两个应用上下文，一个是我们通过配置定义的，另一个则是由 ContextLoaderListener 创建的。DispatcherServlet 负责加载包含 Web 组件的 Bean，如控制器、视图解析器等。而 ContextLoaderListener 负责加载其他的 Bean，如中间层和数据层组件。

AbstractAnnotationConfigDispatcherServletInitializer 类会同时创建 DispatcherServlet 和 ContextLoaderListener。getServletConfigClasses() 方法返回的带有@Configuration 注解的类用来定义DispatcherServlet 应用上下文中的Bean，getRootConfigClasses() 方法返回的带有该注解的类用来配置ContextLoaderListener 创建的应用上下文中的Bean。

WebConfig 类定义如下：

```java
@Configuration
@EnableWebMvc
@ComponentScan("spittr.web")
public class WebConfig extends WebMvcConfigurerAdapter {
	// 定义视图解析器
    @Bean
    public ViewResolver viewResolver() {
        InternalResourceViewResolver resolver = new InternalResourceViewResolver();
        resolver.setPrefix("/WEB-INF/views/");
        resolver.setSuffix(".jsp");
        return resolver;
    }
	// 配置静态资源的处理
    @Override
    public void configureDefaultServletHandling(DefaultServletHandlerConfigurer configurer) {
        configurer.enable();
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        super.addResourceHandlers(registry);
    }
}
```

通过调用 DefaultServletHandlerConfigure 的 enable() 方法，我们要求 DispatcherServlet 将对静态资源的处理转发到 Servlet 容器默认的 Servlet 上，而不是使用 DispatcherServlet。

RootConfig类的定义如下：

```java
@Configuration
@Import(DataConfig.class)
@ComponentScan(basePackages = {"spittr"},
        excludeFilters = {
                @Filter(type = FilterType.CUSTOM, value = WebPackage.class)
        })
public class RootConfig {
    public static class WebPackage extends RegexPatternTypeFilter {
        public WebPackage() {
            super(Pattern.compile("spittr\\.web"));
        }
    }
}
```

### 2.2 使用 XML 配置文件搭建

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

那么对应的配置文件就应该为：/WEB-INF/dispatcher-servlet.xml。即 servlet-name 的值再加上 "-servlet.xml"。同样，DispatcherServlet 配置文件也可以自定义：

```xml
<servlet>
	<servlet-name>dispatcher</servlet-name>
    <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
    <init-param>
        <param-name>contextConfigLocation</param-name>
        <param-value>WEB-INF/test.xml</param-value>
    </init-param>
</servlet>
```

DispatcherServlet 启动后加载配置文件，并构建相应的 WebApplicationContext，该 WebApplicationContext 将之前通过 ContextLoaderListener 加载的顶层 WebApplicationContext 作为父容器。

## 3. 使用 Spring MVC







