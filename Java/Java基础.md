## Java基础

### 基本数据类型

#### 八种基本数据类型

Java共有8中基本数据类型，分别为：

byte（1字节）、short（2字节）、int（4字节）、long（8字节）

float（4字节）、double（8字节）

char（2字节）和boolean。

#### 基本数据类型默认值

当基本类型的变量作为类的成员时，即使不进行初始化Java也会给它一个初始值。但这个规则并不适用于局部变量。

| 基本类型 | 默认值         |
| -------- | -------------- |
| boolean  | false          |
| char     | '\u0000'(null) |
| byte     | (byte)0        |
| short    | (short)0       |
| int      | 0              |
| long     | 0L             |
| float    | 0.0f           |
| double   | 0.0d           |

#### 几个特殊值

Java中的浮点数运算遵循IEEE 754标准，有三个表示溢出和出错情况的三个特殊的浮点数值：

- Double.POSITIVE_INFINITY：正无穷
- Double.NAGATIVE_INFINITY：负无穷
- Double.NaN：Not a Number，不是一个数值需要注意的是，NaN != NaN，检测一个值是否是NaN需要使用Double.isNaN方法。

**for-each**

Java从SE5开始引入了更为简便的for循环语句，即for-each，形式如下：

```java
int[] t = new int[]{1, 2, 3, 4, 5};

for (int i: t) {
    System.out.print(t + " ");
}
```

**label**

标签机制类似于goto语句，它可以跳出层循环直接到达目的代码处。

```java
labeldemo:
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 10; j++) {
        if (something happened)
            break;        // 跳出内层循环
        else if (another thing happened)
            break labeldemo;     // 直接跳转到labeldemo处，但不进入循环，向下继续执行
        else
            continue labeldemo;    // 跳转到labeldemo处，继续执行循环
    }
}
```

需要注意的是，label和循环语句之间不能有其他任何语句。

#### 类的初始化

Java和C++采用相同的初始化方法，即构造器函数和类同名。Java会自动为类创建一个默认的无参构造器。但当你已经创建了构造器，无论是有参还是无参的，Java都不会再去创建默认构造器。

#### this和static

this关键字其实有点类似于Python中的self，只不过self需要显示的传入，this不需要。

```java
class Demo {
    void peel(int i) {
        // do something
    }
}
public class TestThis {
    public static void main(String[] args) {
        Demo d1 = new Demo();
        Demo d2 = new Demo();
        d1.peel(1);
        d2.peel(2);
    }
}
```

如上述代码，peel()方法怎么知道是d1还是d2在调用它呢？原因在于编译器将“所操作对象的引用”作为第一个参数传给了peel()方法，实际的调用类似于：`Demo.peel(d1, 1)`。

在方法内部想要获得当前对象的引用时，就需要用到this关键字。this就表示“调用方法的那个对象”的引用。