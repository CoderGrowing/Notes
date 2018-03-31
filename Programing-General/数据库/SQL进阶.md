# SQL进阶

## 1. 连接

### 1.1 连接条件

 on条件允许在参与连接的关系上设置通用的谓词，类似于where子句。

```sql
select * from student join takes on students.ID = takes.ID
-- 等价于
select * from student, takes where student.ID = takes.ID
```

既然可以翻译为对应的where条件，那on有什么作用呢？主要有两个优点：

第一，在外连接中on和where的表现是不同的；第二，在on中指定连接条件，where中指定其他的条件能使SQL语句更加清晰。

### 1.1 外连接

假设我们要显示一个所有学生的列表，并显示他们参加的课程信息：

```sql
select * from student natural join takes;
```

但这样的查询会出现一些问题。当学生没有选修任何课程的时候，它们的信息不会被输出。因为在takes表中没有ID信息与students表对应。

对于类似这样参与连接的关系可能丢失元组的情况，我们可以用外连接的方式来解决。外连接的方式大概是将信息只存在某一个表中的元组同样进行输出，存在的信息直接输出，在另一个表中没有的信息输出为null。

存在三种形式的外连接：

- 左外连接（left outer join）：只保留出现在左外连接运算之前的关系中的元组
- 右外连接（right outer join）：只保留出现在右外连接运算之后（右边）的关系中的元组
- 全外连接（full outer join）：保留出现在两个关系中的元组

对应的是，不保留未匹配元组的连接运算被称为内连接（inner join）。

对于上述的例子，可以利用左外连接修正结果：

```sql
select * from student natural left outer join takes;
```

**on和where的区别**

考虑下面的查询：

```sql
select *
from student left outer join takes on student.ID = takes.ID;
```

它的行为和上面的查询是相同的，只是ID属性会出现两次。如果我们把on用where子句替换掉呢？

```sql
select *
from student left outer join takes on TRUE
where student.ID = takes.ID
```

此时未选修任何课程的学生信息便不会展现出来，类似于没有使用外连接的情况。

## 2. 视图

数据库中让所有用户都能看到整个逻辑模型是不合理的，出于安全的考虑，我们应该给予不同权限的人群不同的查看范围。例如一个人只能查看老师的标识、姓名和系名，但无权查看工资，用SQL语句描述如下：

```sql
select ID, name, dept_name
from instructor;
```

我们可以将查询结果存储起来提供给用户。但一旦数据更新，这些结果就会过期。为了解决这个问题，SQL允许通过查询定义“虚关系”，即不预先计算存储，而是在使用虚关系时才通过查询被计算出来。虚关系不是逻辑模型的一部分，但对用户可见，被称为**“视图（view）”**

### 2.1 视图定义

视图定义的格式为：

```sql
create view view_name as query_expr
```

例如上述的教师信息定义为视图：

```sql
create view faculty as
select ID, name, dept_name
from instructor;
```

### 2.2 物化视图

某些数据库的实现允许存储视图关系，但它们保证如果用于定义视图的实际关系改变，视图也会跟着修改。这样的视图被称为物化视图。物化视图可以用于预先计算并保存表连接或聚集等耗时较多的操作的结果，这样，在执行查询时，就可以避免进行这些耗时的操作。

但当物化视图的关系被修改后，物化视图应当随时更新。

### 2.3 视图更新

视图名可出现在任何关系名可以出现的地方，