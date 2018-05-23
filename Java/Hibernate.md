## Hibernate

对每个实体类配置对应的.hbm.xml文件：

```xml
<?xml version="1.0"?>
<!DOCTYPE hibernate-mapping PUBLIC
        "-//Hibernate/Hibernate Mapping DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-mapping-3.0.dtd">
 
<hibernate-mapping package="com.hello">
    <class name="Product" table="product_">
        <id name="id" column="id">
            <generator class="native">
            </generator>
        </id>
        <property name="name" />
        <property name="price" />
    </class>
</hibernate-mapping>
```

对整个Hibernate进行配置：

```xml
<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE hibernate-configuration PUBLIC
       "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
"http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">
 
<hibernate-configuration>
    <session-factory>
        <property name="connection.driver_class">com.mysql.jdbc.Driver</property>
        <property name="connection.url">jdbc:mysql://localhost:3306/test?characterEncoding=UTF-8</property>
        <property name="connection.username">root</property>
        <property name="connection.password">123456</property>
        <property name="dialect">org.hibernate.dialect.MySQLDialect</property>
        <property name="current_session_context_class">thread</property>
        <property name="show_sql">true</property>
        <property name="hbm2ddl.auto">update</property>
        <mapping resource="com/Product.hbm.xml" />
    </session-factory>
</hibernate-configuration>
```

```java
SessionFactory sf = new Configuration().configure().buildSessionFactory();
Session s = sf.openSession();
s.beginTransaction();

Product p = new Product();
p.setName("iPhone X");
p.setPrice(8848);
s.save(p);

s.getTransaction().commit();
s.close();
sf.close();
```

#### 基础操作

**获取**

Hibernate根据id获取对象。 除了id之外，还需要传递一个类对象，用于确定获取哪个类型的对象。

```java
Product p =(Product) s.get(Product.class, 6);
```

**删除**

```java
s.delete(p);
```

**修改**

```java
p.setName("iPhone-modified");
s.update(p);
```

**HQL**

