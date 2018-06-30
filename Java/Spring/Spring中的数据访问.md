## Spring 中的数据访问

几乎所有的企业级应用都需要数据库的支持，Spring 当然也提供了数据访问的功能。为了避免持久化的逻辑分散到各个组件中，最好将数据访问的功能放到一个或多个专注此项任务的组件中。这样的组件通常称为数据访问对象（data access object,DAO）或者 Repository。

### 配置数据源

无论使用何种方式访问数据库，数据源的配置都是我们要进行的第一步。Spring 提供了多种配置数据源的方式，如 JDBC 驱动程序定义的数据源；连接池的数据源等。

#### 连接池数据访问

**使用 XML 配置**

```xml
<bean id="dataSource" 
      class="org.apache.commons.dbcp.BasicDataSource"
      destroy-method="close"
      p:driverClassName="org.h2.Driver"
      p:url="jdbc:h2:tcp://localhost/~/dbname"
      p:username="test"
      p:password="yes"/>
```

可以将配置在外部配置文件中实现，引入外部属性文件：

```xml
<context:property-placeholder location="classpath:jdbc.properties"  />
```

假设 jdbc.properties 文件内容如下：

```
jdbc.driverClassName=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/sampledb?useUnicode=true&characterEncoding=UTF-8
jdbc.username=root
jdbc.password=1234
```

此时可在 XML 配置文件中引用 jdbc.properties 文件的内容：

```xml
<bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource"
      destroy-method="close"
      p:driverClassName="${jdbc.driverClassName}"
      …… />
```

**使用 Java 配置**

```java
@Bean
public BasicDataSource dataSource() {
    BasicDataSource ds = new BasicDataSource();
    ds.setDriverClassName("org.h2.Driver");
    ds.setUrl("jdbc:h2:tcp://localhost/~/test");
    // other config
    return ds;
}
```

