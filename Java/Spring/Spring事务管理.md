## Spring事务管理

#### PlatformTransationManager

org.springframework.transactino.PlatformTransactionManager是Spring事务抽象架构的核心接口，主要作用是为应用程序提供事务界定的统一方式。

```java
public interface PlatformTransactionManager {
    TransactionStatus getTransaction(TransactionDefinition var1) throws TransactionException;
    void commit(TransactionStatus var1) throws TransactionException;
    void rollback(TransactionStatus var1) throws TransactionException;
}
```



#### TransactionDefinition

org.springframework.transactino.TransactionDefinition定义了有哪些事务属性可以指定，包括：

- 事务的隔离级别
- 事务的传播行为
- 事务的超时时间
- 是否为只读事务

**隔离级别**

TransactionDefinition定义了五个常量提供可选择的隔离级别：

- ISOLATION_DEFAULT：使用数据库默认隔离级别，通常为 Read Committed
- ISOLATION_READ_UNCOMMITTED：对象 Read Uncommitted级别，无法避免脏读，不可重复读和幻读
- ISOLATION_READ_COMMITTED，对应Read Committed，可以避免脏读，但无法避免不可重复读和幻读
- ISOLATION_REPEATABLE_READ：对应Repeatable read隔离级别，不能避免幻读
- ISOLATION_SERIALIZABLE：对应Serializable隔离级别，可以避免所有，但并发效率最低

**传播行为**

- PROPAGATION_REQUIRED：如果当前没有事务，则新建一个事务；如果已经存在一个事务，则加入到这个事务中。通常为默认的事务传播行为。
- PROPAGATION_SUPPORTS：支持当前事务。如果当前没有事务，则以非事务方式执行
- PROPAGATION_MANDATORY：使用当前的事务。如果当前没有事务，则抛出异常
- PROPAGATION_REOUIRES_NEW：新建事务。如果当前存在事务，则把当前事务挂起

- PROPAGATION_NOT_SUPPORTED：以非事务方式执行操作。如果当前存在事务，则把当前事务挂起 
- PROPAGATION_NEVER以非事务方式执行。如果当前存在事务，则抛出异常
- PROPAGATION_NESTED如果当前存在事务，则在嵌套事务内执行；如果当前没有事务，则执行与 PROPAGATION_REQUIRED类似的操作

