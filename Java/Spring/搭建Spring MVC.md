# 搭建 Spring MVC

### 1. 配置 DispatcherServlet

DispatcherServlet 是 Spring MVC 的核心，所有的请求第一站都是 DispatcherServlet。

在 Spring MVC 中需要配置 DispatcherServlet 只需要扩展 `AbstractAnnotationConfigDispatcherServletInitializer` 类即可。扩展了该类的子类会自动配置 DispatcherServlet 和 Spring 应用上下文。

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

扩展这个类需要重写三个方法。第一个方法是 `getServletMappings`，它会将一个或多个路径映射到 DispatcherServlet 上。如果映射的是“ / ”的话，表明是默认的 Servlet，会处理所有请求。