# Mybatis

## 配置

### 1. 使用 XML 配置 Mybatis

```xml
<configuration>
    <properties resource="application.properties">
        <property name="username" value="db_user"/>
        <property name="password" value="verysecurepwd"/>
    </properties>
    <settings>
        <setting name="cacheEnabled" value="true"/>
    </settings>
    <typeAliases>
        <typeAlias alias="Tutor" type="com.mybatis3.domain.Tutor"/>
        <package name="com.mybatis3.domain"/>
    </typeAliases>
    <typeHandlers>
        <typeHandler handler="com.mybatis3.typehandlers. PhoneTypeHandler"/>
        <package name="com.mybatis3.typehandlers"/>
    </typeHandlers>
    
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="${jdbc.driverClassName}"/>
                <property name="url" value="${jdbc.url}"/>
                <property name="username" value="${jdbc.username}"/>
                <property name="password" value="${jdbc.password}"/>
            </dataSource>
        </environment>
        <environment id="production">
            <transactionManager type="MANAGED"/>
            <dataSource type="JNDI">
                <property name="data_source" value="java:comp/jdbc/MyBatisDemoDS"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <mapper resource="com/mybatis3/mappers/StudentMapper.xml"/>
        <mapper url="file:///D:/mybatisdemo/mappers/TutorMapper.xml"/>
        <mapper class="com.mybatis3.mappers.TutorMapper"/>
    </mappers>
</configuration>
```

#### 1.1 environment

MyBatis 支持配置多个 dataSource 环境，可以将应用部署到不同的环境上，如开发环境、生产环境等。开发时将默认的配置环境设置为 development，上线时只需要修改为 production 即可。

如果应用需要多个数据库，需要将每个数据库配置为单独的环境，并且为每个数据库创建一个 SqlSessionFactory。创建SqlSessionFactory时指定数据源的 id 就好。

```java
SqlSessionFactory devSqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStre
am, "development");
```

**dataSource**

dataSource 元素被用来配置数据库连接属性。 dataSource 的类型可以配置成其内置类型之一，如 POOLED，JNDI，UNPOOLED。

- UNPOOLED：MyBatis 会为每一个数据库操作创建一个新的连接，并关闭它。该方式适用于只有小规模数量并发用户的简单应用程序上。
- POOLED：MyBatis 会创建一个数据库连接池，连接池中的一个连接将会被用作数据库操作。一旦数据库操作完成，MyBatis 会将此连接返回给连接池。在开发或测试环境中，经常使用此种方式。
- JNDI：MyBatis 从在应用服务器向配置好的 JNDI 数据源 dataSource 获取数据库 连接。在生产环境中，优先考虑这种方式。 

**事务管理器 TransactionManager** 

MyBatis 支持两种类型的事务管理器： JDBC and MANAGED。

JDBC 事务管理器被用作当应用程序负责管理数据库连接的生命周期（提交、回退等等）的时候。当你将 TransactionManager 属性设置成 JDBC，MyBatis 内部将使用 JdbcTransactionFactory 类创建 TransactionManager。例如，部署到 Apache Tomcat 的应用程序，需要应用程序自己管理事务。 

MANAGED 事务管理器是当由应用服务器负责管理数据库连接生命周期的时候使用。当MyBatis 内部使用 ManagedTransactionFactory 类 创建事务管理器TransactionManager。例如，当一个JavaEE的应用程序部署在类似 JBoss，WebLogic， GlassFish 应用服务器上时，它们会使用 EJB 进行应用服务器的事务管理能力。在这些管理环境中，你 可以使用 MANAGED 事务管理器。 

#### 1.2 属性 properties

在 mybatis-config.xml 文件中，可以为属性使用 application.properties 文件中定义的占位符： 

```properties
jdbc.driverClassName=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/mybatisdemo
jdbc.username=root
jdbc.password=admin
```

#### 1.3  类型别名 typeAliases 

定义映射关系的时候我们需要使用类的全限定名，使用 typeAliases 可以为类起一个别名，避免写长长的全限定名。

```xml
<typeAliases>
	<typeAlias alias="Student" type="com.mybatis3.domain.Student" />
	<typeAlias alias="Tutor" type="com.mybatis3.domain.Tutor" />
</typeAliases>
```

可以不用为每一个 JavaBean 单独定义别名, 只需要提供需要取别名的 JavaBean 所在的包，MyBatis 会自动扫描包内定义的 JavaBeans，然后分别为 JavaBean 注册一个小写字母开头的非完全限定的类名形式的别名。

```xml
<typeAliases>
	<package name="com.mybatis3.domain" />
</typeAliases>
```

另外，还可以利用注解来起别名：

```java
@Alias("student")
public class Student {}
```

@Alias 注解将会覆盖配置文件中的定义。 

#### 1.4 类型处理器 typeHandlers 

Mybatis 内部使用 JDBC 完成数据库操作，当 MyBatis 将一个 Java 对象作为输入参数执行 INSERT 语句操作时，它会创建一个 PreparedStatement 对象，并且 使用 setXXX()方式对占位符设置相应的参数值。例如，我们需要执行如下的 SQL 语句：

```xml
<insert id="insertStudent" parameterType="Student">
	INSERT INTO STUDENTS(STUD_ID,NAME,EMAIL,DOB)
	VALUES(#{studId},#{name},#{email},#{dob})
</insert>
```

 Mybatis 首先生成以下的 Java 代码：

```java
PreparedStatement pstmt = connection.prepareStatement = 
    ("INSERT INTO STUDENTS(STUD_ID,NAME,EMAIL,DOB) VALUES(?,?,?,?)");
```

然后，Mybatis 需要检查 Student 对象的各个属性的类型，然后使用合适 setXXX 方法去设置参数值。这里 studId 是 integer 类型，所以会使用 setInt()方法，而 name 和 email 是 String 类型，所以会使用 setString() 方法。那 Mybatis 是怎么知道它们的类型的呢？MyBatis 是通过使用类型处理器（type handlers）来决定这么做的。 

MyBatis 对于以下的类型使用内建的类型处理器：所有的基本数据类型、基本类型的包裹类型、byte[]、 java.util.Date、java.sql.Date、java,sql.Time、java.sql.Timestamp、java 枚举类型等。

那当我们自定义了数据类型，Mybatis 该怎么存储呢？这时需要我们自定义一个类型处理器：

定义后，需要在 mybatis-config.xml 文件中注册它：

```xml
<typeHandlers>
	<typeHandler handler="com.mybatis3.typehandlers. PhoneTypeHandler" />
</typeHandlers>
```

#### 1.5 全局设置 settings