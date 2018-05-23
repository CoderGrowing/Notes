## SQL基础

### 1. 基本类型

- char(n)：固定长度的字符串，用户指定长度n，全称character
- varchar(n)：可变长度字符串，用户指定最大长度n，全称character varying
- int：整数类型，全称integer
- smallint：小整数类型
- numeric(p, d)：定点数，精度由用户指定，p位数字加上d位小数
- real, double  precision：浮点数与双精度浮点数，精度与机器有关
- float(n)：精度至少为n的浮点数

### 2. 基本模式定义

#### 2.1 创建表

`create table`命令用来创建表

```sql
create table department
	(dept_name varchar(20),
    building varchar(15),
     budget numeric(12, 2),
     primary key(dept_name));
     
create table course
	(course_id varchar(7),
    title varchar(50),
    dept_name varchar(20),
    credits numeric(2, 0),
    primary key(course_id)
    foreign key(dept_name) references department);
```

`create table`命令支持的完整性约束：

- primary key(A1, A2, ... Am)：primary key表述属性A1, A2,... Am构成了关系的主键。主键的值必须非空而且唯一
- foreign key(A1, A2... Am)：references：外键，表示关系在属性(A1, A2, ... Am)上的取值必须对应于关系s中某元组在主键属性上的取值
- not null：不允许空值

#### 2.2 插入数据

```sql
insert into department values('ExampleName', 'ExampleBuild', '200000.0')
```

#### 2.3 删除

```sql
delete from department;   --: 删除department关系中所有元组，但保留department模式
drop table department;    --: 删除department关系，同时删除模式
```

#### 2.4 增加属性

```sql
alter table department add floors int    --: 在关系department中增加属性floors，域为int
```

#### 2.5 更新

```sql
update instructor set salary = salary * 1.05;
```

```sql
update instructor set salary = salary * 1.05
where salary < 7000;
```

```sql
update instructor
set salary = case
	when salary <= 10000 then salary * 1.05
	else salary * 1.03
```

### 3. 查询

查询的基本结构由select、from和where三个字句构成。

#### 3.1 单关系查询

例如找出所有老师的名字这样的要求：

```sql
select name from instructor;       --: 在关系instructor中找出所有教师的名字
select distinct name from instructor    --: 找出所有名字，去除重复
```

SQL查询结果默认保留重复的值，如果想要指定删除重复，使用关键字`distinct`：

```sql
select distinct dept_name from instrucor;
```

使用关键字`all`显式指明不去除重复：

```sql
select all dept_name from instrtuctor
```

#### 3.2 多关系查询

```sql
select name, instructor.dept_name, buliding
from instructor, department
where instructor.dept_name = department.dept_name
```

通常而言，一个SQL语句查询的含义可以理解如下：

1. 为from子句中列出的关系产生笛卡儿积
2. 在步骤1的结果上应用 where子句中指定的谓词
3. 对于步骤2结果中的每个元组，输出 select子句中指定的属性（或表达式的结果）

需要注意，实际上SQL并不是这样执行的，这样只是有助于理解。

#### 3.3 自然连接

例如我们需要完成这样的查询：从instructor表和teachers表中组合信息找出教师名和课程标识，匹配条件是instructor.ID等于teachers.ID。我们可以这样完成SQL语句：

```sql
select name, course_is
from instructor, teachers
where teachers.ID = instructor.ID
```

这种匹配的条件非常常见，为了简化工作，SQL支持一种被称为**自然连接**的运算。自然连接只考虑那些在两个关系模式中都出现的属性上取值相同的元组对。利用自然连接上述SQL语句可以改写为：

```sql
select name course_id
from instructor natural join teachers
```

当查询条件为“列出教师的名字以及他们所教授的课程名称”时，查询语句可以这么写：

```sql
select name, title
from instructor natural join teachers, course
where teacher.course_id = course.course_id
```

好像又出现了类似的匹配条件，那可以继续用自然连接改写么？

```sql
select name, title
from instructor natural join teachers natural join course
```

这两条SQL语句等价么？答案是否定的。第二条语句的找出的是三个关系中所有属性取值均相同的结果。为了避免这种情况，SQL提供了joion...using运算来给定属性名列表：

```sql
select name, title from (instructor natural join teachers) join course using (course_id)
```

### 3. 运算

#### 3.1 更名运算

as子句可以将查询结果重命名。

```sql
select T.name, S.course_id
from instructor as T, teachers as S
where T.ID = s.ID
```

上述SQL语句说明了更名的一种好处：将长关系名换为短关系名。除此之外，更名运算还可以用在需要比较同一个关系中的元组的情况。

```sql
select distinct T.name
from instructor as T, instructor as S
where T.salary > S.salary and S.dept_name = 'Biology'
```

#### 3.2 字符串运算

SQL使用一对单引号标识字符串，如'Tom'，当字符串中有单引号时用两个单引号字符来转义，如'it''s mine.'。

在字符串上可以用like操作符进行模式匹配：

- %：匹配任意子串
- _：匹配任意一个字符

例如'test%'匹配任意以test开头的字符串、'___'匹配任意三位字符的字符串……

```sql
select dept_name
from department
where building like '%Watson%'
```

此外，SQL还允许我们自定义转义字符，利用escape关键字：

```sql
like 'ab\%cd%' escape '\'   --;定义\为转义字符
```

#### 3.3 显示顺序

利用order by子句可以让查询结果中元组按照顺序显示。默认为升序排序，如果需要指定顺序，desc表示降序，asc表示升序。

```sql
select *
from instructor
order by salary desc, name asc;
```

#### 3.4 集合运算

SQL用union、intersect和except运算进行数学上的交并差运算。例：

```sql
(select course_id
from section
where semester = 'Fall' and year = '2009')
union
(select course_id
from section
where semester = 'Spring' and year = '2010')
```

找出2009年秋季或2010年春季开课的所有课程。注意union操作自动去除重复。如果想保留重复，需要使用union all。交、差操作类似。

#### 3.5 空值

空值表示为null。在SQL中空值比较特殊，涉及到空值的问题也比较多。为此，SQL定义了一种全新的布尔值：unknown。例如"1 < null"的值就为unknown。具体规则如下：

- and: true and unknoun的结果是 unknown， false and unknown结果是 false， unknoun and unknown的结果是 unknoun。
- or: true or unknown的结果是true， false or unknown结果是 aunknown，， unknown or unknown结果是 unknown
- not: not unknoun的结果是 unknown

### 4. 聚集函数

SQL提供了五个固有聚集函数：

- 平均值：avg
- 最小值：min
- 最大值：max
- 总和：sum
- 计数：count


sum和avg的输入必须为数字，其他运算符还可以作用在其他类型集合上，如字符串。

```sql
select avg(salary)
from instructor
where dept_name = 'Comp. Sci.'
```

#### 4.1 分组聚集

SQL中可以使用group by子句进行分组聚集，将输出数据按照指定的规则分组。

```sql
select dept_name, avg(salary)
from instructor
group by dept_name
```

需要注意的是，出现在select语句中但是没有被聚集的属性只能是出现在group by子句中的属性。例如下面的例子就是错误的：

```sql
select dept_name, ID, avg(salary)
from instructor
group by dept_name
```

ID出现在了select子句中，但却没有被聚集且非group by子句内容，所以此条查询是错误的。

#### 4.2 having子句

having子句中的谓词在形成分组后才起作用，因此可以使用聚集函数。

```sql
select dept_name avg(salary) as avg_salary
from instrucor
group by dept_name
having avg(salary) > 42000
```

