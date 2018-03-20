# Java中的OOP

1. 继承关键字：extends，所有类都默认继承自Object类
2. 接口：interface
3. Java不允许多继承，但允许实现多个接口
4. 将类设置成final可以防止被继承
5. 关键字`instanceof`可以检验某对象是否为某种指定的类型

### 1. 域和可访问性

- 默认：没有任何权限修饰符的方法都是默认级别的，即同一个包内的类可以访问
- public：公开属性，任何类均可访问
- protect：保护方法，子类可访问
- private：私有方法，只有类自身可以访问

### 2. 构造器

- 如果子类没有构造器，编译器会隐式添加一个无参构造器

- 实例化子类时，编译器会先调用父类的构造器，即子类实例化时，所有的父类都会实例化

- 调用父类构造器：使用关键字`super`可以显示调用父类的构造器，但`super`必须是构造器中的第一条语句。如：`super(argus)`。

- `super`表示的是当前对象的直接超类的一个实例。所以利用`super`还可以调用父类的方法。

  `System.out.println(super.toString())`。调用父类中的方法不需要写在第一行

### 3. 类型转换

```java
Child child = new Chile();
Parent parent = child();       // 向上转换，父类引用指向子类

Child child = (Child) parent;   // 向下转换，只有父类引用指向子类时可用，否则报错
```