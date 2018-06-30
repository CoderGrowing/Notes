# Java 基础

## 一、 基本数据类型

### 八种基本数据类型

Java 共有 8 中基本数据类型，分别为：

- byte（1 字节）
- short（2 字节）
- int（4 字节）
- long（8 字节）
- float（4 字节）
- double（8 字节）
- char（2 字节）
- boolean（1bit）

### 基本数据类型默认值

当基本类型的变量作为类的成员时，即使不进行初始化 Java 也会给它一个初始值。但这个规则并不适用于局部变量。

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

### 几个特殊值

Java 中的浮点数运算遵循 IEEE 754 标准，有三个表示溢出和出错情况的三个特殊的浮点数值：

- Double.POSITIVE_INFINITY：正无穷
- Double.NAGATIVE_INFINITY：负无穷
- Double.NaN：Not a Number，不是一个数值需要注意的是，NaN != NaN，检测一个值是否是 NaN 需要使用 Double.isNaN 方法。

### 自动装箱 / 拆箱

基本类型都有对应的包装类型，基本类型与其对应的包装类型之间的赋值使用自动装箱与拆箱完成。

```java
Integer x = 2;     // 装箱
int y = x;         // 拆箱
```

编译器在进行自动装箱过程中调用 `valueOf()` 方法，new Integer(123) 与 Integer.valueOf(123) 的区别在于，**new Integer(123) 每次都会新建一个对象，而 Integer.valueOf(123) 可能会使用缓存对象，因此多次使用 Integer.valueOf(123) 会取得同一个对象的引用。**

因此多个 Integer 实例使用自动装箱来创建并且值相同，那么就会引用相同的对象。

```java
Integer m = 123;
Integer n = 123;
System.out.println(m == n); // true
```

valueOf() 方法的实现比较简单，就是先判断值是否在缓存池中，如果在的话就直接使用缓存池的内容。在 Java 8 中，Integer 缓存池的大小默认为 -128\~127。

Java 还将一些其它基本类型的值放在缓冲池中，包含以下这些：

- boolean values true and false
- all byte values
- short values between -128 and 127
- int values between -128 and 127
- char in the range \u0000 to \u007F

因此在使用这些基本类型对应的包装类型时，就可以直接使用缓冲池中的对象。

## 二、条件控制与循环

### for-each

Java 从 SE5 开始引入了更为简便的 for 循环语句，即 for-each，形式如下：

```java
int[] t = new int[]{1, 2, 3, 4, 5};

for (int i: t) {
    System.out.print(t + " ");
}
```

### label

标签机制类似于 goto 语句，它可以跳出层循环直接到达目的代码处。

```java
labeldemo:
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 10; j++) {
        if (something happened)
            break;        // 跳出内层循环
        else if (another thing happened)
            break labeldemo;     // 直接跳转到 labeldemo 处，但不进入循环，向下继续执行
        else
            continue labeldemo;    // 跳转到 labeldemo 处，继续执行循环
    }
}
```

需要注意的是，label 和循环语句之间不能有其他任何语句。

### Switch

从 Java 7 开始，可以在 switch 条件判断语句中使用 String 对象。

```java
String s = "a";
switch (s) {
    case "a":
        System.out.println("aaa");
        break;
    case "b":
        System.out.println("bbb");
        break;
}
```

**switch 不支持 long 类型**，是因为 swicth 的设计初衷是为那些只需要对少数的几个值进行等值判断，如果值过于复杂，那么还是用 if 比较合适。

## 三、类

### 1. Object 通用方法

```java
public final native Class<?> getClass()

public native int hashCode()

public boolean equals(Object obj)

protected native Object clone() throws CloneNotSupportedException

public String toString()

public final native void notify()

public final native void notifyAll()

public final native void wait(long timeout) throws InterruptedException

public final void wait(long timeout, int nanos) throws InterruptedException

public final void wait() throws InterruptedException

protected void finalize() throws Throwable {}
```

#### 1.1 hashCode()

hasCode() 返回散列值，而 equals() 是用来判断两个实例是否等价。**等价的两个实例散列值一定要相同，但是散列值相同的两个实例不一定等价**。

**在覆盖 equals() 方法时应当总是覆盖 hashCode() 方法，保证等价的两个实例散列值也相等**。

#### 1.2 Clone()

**深拷贝与浅拷贝** 

- 浅拷贝：拷贝实例和原始实例的引用类型引用同一个对象；
- 深拷贝：拷贝实例和原始实例的引用类型引用不同对象。

使用 clone() 方法来拷贝一个对象即复杂又有风险，它会抛出异常，并且还需要类型转换。Effective Java 书上讲到，最好不要去使用 clone()，可以使用拷贝构造函数或者拷贝工厂来拷贝一个对象。

```java
public class CloneConstructorExample {
    private int[] arr;

    public CloneConstructorExample() {
        arr = new int[10];
        for (int i = 0; i < arr.length; i++) {
            arr[i] = i;
        }
    }

    public CloneConstructorExample(CloneConstructorExample original) {
        arr = new int[original.arr.length];
        for (int i = 0; i < original.arr.length; i++) {
            arr[i] = original.arr[i];
        }
    }

    public void set(int index, int value) {
        arr[index] = value;
    }

    public int get(int index) {
        return arr[index];
    }
}
```

```java
CloneConstructorExample e1 = new CloneConstructorExample();
CloneConstructorExample e2 = new CloneConstructorExample(e1);
e1.set(2, 222);
System.out.println(e2.get(2)); // 2
```

### 2. 访问权限

Java 中有三个访问权限修饰符：private、protected 以及 public，如果不加访问修饰符，表示包级可见。

可以对类或类中的成员（字段以及方法）加上访问修饰符。

- 成员可见表示其它类可以用这个类的实例访问到该成员；
- 类可见表示其它类可以用这个类创建对象。

protected 用于修饰成员，**表示在继承体系中成员对于子类可见，但是这个访问修饰符对于类没有意义**。

### 3. 抽象类与接口

#### 3.1 抽象类

抽象类和抽象方法都使用 abstract 进行声明。抽象类一般会包含抽象方法，**抽象方法一定位于抽象类中**。

抽象类和普通类最大的区别是，抽象类不能被实例化，需要继承抽象类才能实例化其子类。

#### 3.2 接口

接口是抽象类的延伸，在 Java 8 之前，它可以看成是一个完全抽象的类，也就是说它不能有任何的方法实现。

接口中的方法自动的属于 public，而实现接口时的方法可见域不能小于接口中定义的方法，所以实现接口的方法也一定是 public 的。而接口的字段默认都是 static 和 final 的。

**默认方法**

从 Java 8 开始，接口也可以拥有默认的方法实现，使用 default 修饰符标记：

```java
public interface Comparable<T> {
    default int compareTo(T other) { return 0; }
}
```

默认方法的作用由两个：一个是为不需要重写的方法提供默认实现，免去程序员每次重写的麻烦；二是“接口演化（interface evolution）”，将接口的新增方法提供默认实现可以保证旧的实现了该接口的方法可以正常编译、使用。

**默认方法冲突**

如果一个接口中将一个方法定义为默认方法，另一个超类或者另一个接口中也定义了同样的方法，Java 怎么处理这种冲突呢？

1. **超类优先**。如果超类提供了具体方法，同样的默认方法会被忽略
2. **接口冲突**。两个接口冲突的情况下，实现接口的类必须覆盖这个冲突的方法。

#### 3.3 比较

使用抽象类：

- 需要在几个相关的类中共享代码。
- 需要能控制继承来的方法和域的访问权限，而不是都为 public。
- 需要继承非静态（non-static）和非常量（non-final）字段。

使用接口：

- 需要让不相关的类都实现一个方法，例如不相关的类都可以实现 Compareable 接口中的 compareTo() 方法；
- 需要使用多重继承。

在很多情况下，接口优先于抽象类，因为接口没有抽象类严格的类层次结构要求，可以灵活地为一个类添加行为。并且从 Java 8 开始，接口也可以有默认的方法实现，使得修改接口的成本也变的很低。

### 4. super

- 访问父类的构造函数：可以使用 super() 函数访问父类的构造函数，从而完成一些初始化的工作。
- 访问父类的成员：如果子类覆盖了父类的中某个方法的实现，可以通过使用 super 关键字来引用父类的方法实现。

```java
public class SuperExample {
    protected int x;
    protected int y;

    public SuperExample(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public void func() {
        System.out.println("SuperExample.func()");
    }
}
```

```java
public class SuperExtendExample extends SuperExample {
    private int z;

    public SuperExtendExample(int x, int y, int z) {
        super(x, y);
        this.z = z;
    }

    @Override
    public void func() {
        super.func();
        System.out.println("SuperExtendExample.func()");
    }
}
```

```java
SuperExample e = new SuperExtendExample(1, 2, 3);
e.func();
```

```html
SuperExample.func()
SuperExtendExample.func()
```

> [Using the Keyword super](https://docs.oracle.com/javase/tutorial/java/IandI/super.html)

### 5. 内部类

内部类是定义在另一个类中的类。那么为什么需要使用内部类？

- 内部类可以访问该类所在作用域中的数据（包括私有的数据）
- 内部类可以对同一个包中的其他类隐藏起来

## 四、final 和 static

### final

final 可以作用在数据、方法和类上，分别起到不同的效果：

**1. 数据**

声明数据为常量，可以是编译时常量，也可以是在运行时被初始化后不能被改变的常量。

- 对于基本类型，final 使数值不变；
- **对于引用类型，final 使引用不变，也就不能引用其它对象，但是被引用的对象本身是可以修改的**。

```java
final int x = 1;
// x = 2;  // cannot assign value to final variable 'x'
final A y = new A();
y.a = 1;
```

**2. 方法**

声明方法不能被子类覆盖。

**private 方法隐式地被指定为 final**，如果在子类中定义的方法和基类中的一个 private 方法签名相同，此时子类的方法不是覆盖基类方法，而是在子类中定义了一个新的方法。

**3. 类**

声明类无法被继承。

### static

**1. 静态变量** 

静态变量在内存中只存在一份，只在类初始化时赋值一次。

- 静态变量：类所有的实例都共享静态变量，可以直接通过类名来访问它；
- 实例变量：每创建一个实例就会产生一个实例变量，它与该实例同生共死。

```java
public class A {
    private int x;        // 实例变量
    public static int y;  // 静态变量
}
```

**2. 静态方法** 

静态方法在类加载的时候就存在了，它不依赖于任何实例，所以静态方法必须有实现，也就是说它不能是抽象方法（abstract）。

**3. 静态语句块** 

静态语句块在类初始化时运行一次。

**4. 静态内部类** 

内部类的一种，静态内部类不依赖外部类，且不能访问外部类的非静态的变量和方法。

**5. 静态导包** 

```java
import static com.xxx.ClassName.*
```

在使用静态变量和方法时不用再指明 ClassName，从而简化代码，但可读性大大降低。

**6. 变量赋值顺序** 

静态变量的赋值和静态语句块的运行优先于实例变量的赋值和普通语句块的运行，静态变量的赋值和静态语句块的运行哪个先执行取决于它们在代码中的顺序。存在继承的情况下，初始化顺序为：

- 父类（静态变量、静态语句块）
- 子类（静态变量、静态语句块）
- 父类（实例变量、普通语句块）
- 父类（构造函数）
- 子类（实例变量、普通语句块）
- 子类（构造函数）

## 五、反射

利用反射 (reflect) 可以在运行时分析类的能力、构建新的类，类似于动态语言中的元编程。

**Class 类**

在程序的运行期间，Java 运行时系统始终为所有的对象维护一个被称为运行时的类型标识，这个信息跟踪着每个对象所属的类。保存这些信息的类是 Class 类，Object 类中的 getClass() 方法会返回一个 Class 类型的实例。

```java
GetClass testGetClass = new GetClass();
Class aClass = testGetClass.getClass();
System.out.println(aClass.getName()); // GetClass
```

此时通过 aClass 即可获取 GetClass 类的相关信息。

鉴于历史原因，getName 方法在应用于数组类型的时候会返回一个很奇怪的名字：

- Double[].class.getName()：返回 `[Ljava.lang.Double;`
- int[].class.getName()：返回 `[I`

## 六、异常

### 1. 异常分类

Java 中所有的异常类都继承自 `Throwable`，它有两个直接子类：`Error` 和 `Exception`。

其中 `Error` 类用来表示系统错误，由 Java 虚拟机抛出。通常我们进行程序设计时主要关注的是 `Exception` 类。`Exception` 类有两个分支：`RuntimeException` 和其他异常。由程序导致的错误属于 `RuntimeException`，而由于 I/O 错误等原因导致的异常属于其他异常。

Java 语言规范将派生于 `Error` 和 `RuntimeException` 类的异常称为**非受查（unchecked）异常**，将其他异常称之为**受查（checked）异常**。编译器将核查是否为所有的受查异常提供了异常处理器。

`Exception` 类的几个常用方法：

- `public String toString()`：返回这个异常的描述
- `public void printStackTrace()`：输出 Exception 对象的异常描述，后面是一个栈跟踪，找到代码哪里出了问题。

### 2. 抛出异常

遇到了无法处理的情况，Java 的方法应当抛出一个异常。在出错的地方，利用 `throw` 抛出指定的异常。另外，在可能抛出异常的方法中，可以在声明首部利用 `throws` 说明本方法可能抛出的异常类型：

```java
method() throws SomeExceptino {
    if (an error occurs) {
        throw new SomeException;
    }
}
```

那么什么时候应当在方法声明处声明可能要抛出的异常呢？先来看看什么时候应当抛出异常 :

- 调用一个抛出受查异常的方法，如 FileInputStream 构造器时

- 程序运行过程中发现错误，并且利用 throw 语句抛出一个受查异常
- 程序出现错误，如访问不存在的下标时会抛出 ArrayIndexOutOfBoundsException 异常
- Java 虚拟机和运行时库出现的内部错误

如果出现前两种情况之一，则必须告诉调用这个方法的程序员这里有可能抛出异常。即，**一个方法必须声明所有可能抛出的受查异常**，而对于非受查异常，应该想办法去解决，而不是说明这些错误可能出现。

如果在子类中覆盖了超类的一个方法，那么子类方法中声明的受查异常不能比超类中声明的异常更通用。如果超类中方法没有抛出任何异常，那么子类中的方法同样不能抛出任何受查异常。

### 4. 捕获异常

想要捕获一个异常，必须使用 try...catch 语句块：

```java
try {
    code here;
} catch (Exception e) {
    handler for this Exception
}
```

捕获多个异常：`try...catch(exception1)...catch(exception2)`
或者是：`try...catch(exception1 | exception2 e)`（多种异常处理方法相同时使用）。

**finally 子句**

finally 子句的用处在于确保资源的正常关闭。在 try...catch 块后使用 finally 子句可以执行无论发生异常与否都需要执行的动作。

注意，当 finally 子句中包含 return 语句时，在方法返回前 finally 子句就会执行，所以它会覆盖原方法的 return 语句。

**try-with-resources**

对于以下代码模式：

```java
open a resource
try {
    work with resource
} finally {
    close the resource
}
```

如果资源实现了 AutoCloseable 接口，那么资源可以自动关闭，我们可以写出更为简洁的代码：

```java
try (Resource res=...) {
    work with resources
}
```

Java 会保证无论什么情况下资源都会被关闭。

### 5. 自定义异常

用户自定义异常需要从 java.lang.Exception 类继承。

```java
public class InputInvalidException extends Exception {
    public String toString() {
        System.out.println("Your input are invalid.")
    }
}
```

### 6. 断言

assert 在 Java 中有两种形式：

- assert 条件 ;
- assert 条件 : 表达式 ;

例如想要断言 x 为非负值：

```java
assert x >= 0;
assert x >=0 : x；
```

默认情况下的 assert 是被禁用的，可以在运行程序时加入 `-enableassertions` 或者 `-ea` 选项启用。

## 七、泛型

- 泛型可以使我们在编译时而不是在运行时检测出错误
- 泛型类型必须是引用类型，不能使用 int、double 这样的基本类型，但在泛型类型中添加元素时，基本类型会自动装箱，不会出现错误
- 泛型可以有多个参数，形式如下：`<E1, E2, E3>`
- 泛型类型的构造方法不用表示为泛型，即 `public GenericStack<E>()` 是错误的

### 1. 定义泛型类

我们可以为类或者接口定义泛型。

```java
public class GenericStack<E> {
    private java.util.ArrayList<E> list = new java.util.ArrayList<>();

    public int getSize() {
        return list.size();
    }

    public E peek() {
        return list.get(getSize() - 1);       // 返回最后一个元素
    }

    public void push(E o) {
        list.add(o);
    }

    // 移除并返回最后一个元素
    public E pop() {
        E o = list.get(getSize() - 1);
        list.remove(getSize() - 1);
        return o;
    }

    public boolean isEmpty() {
        return list.isEmpty();
    }

    @Override
    public String toString() {
        return "stack: " + list.toString();
    }    
}
```

### 2. 定义泛型方法

```java
public class GenericMethodDemo {
    public static void main(String[] args) {
        Integer[] integers = {1, 2, 3, 4, 5};
        String[] strings = {"London", "Paris", "New York"};

        GenericMethodDemo.<Integer>print(integers);
        GenericMethodDemo.<String>print(strings);
    }

    // 定义泛型方法
    public static <E> void print(E[] list) {
        for (int i = 0; i < list.length; i++) {
            System.out.print(list[i] + " ");
        }
        System.out.println();
    }
}
```

实例代码中我们调用泛型方法时传入了实际类型，其实简单调用 `print(integers)` 或者 `print(strings)` 也可以，编译器会自动发现类型。

需要注意的是，当我们定义泛型类时，泛型类型是放在类名之后的，如 `GenericStack<E>`，而当我们定义泛型方法时，泛型类型是放在方法返回类型之前的，如 `<E> void print (E[] list)`

### 3. 几种泛型类型

**受限泛型类型**

```java
public static <E extends SomeClass> boolean equal(E obj1, E obj2) {
    return obj1.getArea() == obj2.getArea();
}
```

如上述代码所示，泛型类型被指定为了另一种类型的子类型，这种的泛型被称为受限泛型 (bound)。

**原始类型**

定义泛型后可以不指定具体类型，例如：

```java
GenericStack stack = new GenericStack();
// 大致等价于
GenericStack<Object> stack = new GenericStack<Object>();
```

这样不指定具体类型的泛型被称为原始类型 (raw type)。它是不安全的，不推荐使用。

**通配泛型**

```java
package Generic;

public class WildCardNeed {
    public static void main(String[] args) {
        GenericStack<Integer> intStack = new GenericStack<>();
        intStack.push(1);
        intStack.push(2);
        System.out.println("The max number is: " + max(intStack));
    }

    public static double max(GenericStack<Number> stack) {
        double max = stack.pop().doubleValue();

        while (!stack.isEmpty()) {
            double value = stack.pop().doubleValue();
            if (value > max) 
                max = value;
        }
        return max;
    }
}
```

如上述代码所展示的那样，第 8 行代码会出现编译错误。尽管 Integer 是 Number 的子类型，但 `GenericStack<Integer>` 并不是 `GenericStack<Number>` 的子类型。

为了避免这个问题，可以使用通配泛型类型。通配泛型类型有三种形式：`?`、`? extend T` 或者 `?super T`，其中 T 是泛型类型。

第一种的 `?` 被称为**非受限通配（unbounded wildcard）**，第二种形式 `? extends T` 被称为**受限通配（bounded wildcard）**，表示 T 或者 T 的一个子类型。第三种形式 `? super T` 被称为**下限通配（lower-bounded wildcard）**，表示 T 或者 T 的一个父类型。

了解了这个，上述例子只需要修改一行代码就可以解决错误

```java
// line 11
public static double max(GenericStack<? extends Number> stack)
```

### 4. 类型消除

泛型是利用一种叫做类型消除（type erasure）的技术来实现的。在编译时编译器检查泛型有没有被正确使用，一旦确认安全后，泛型会被转化为原始类型。

```java
ArrayList<String> list = new ArrayList<>();
list.add("test");
String state = list.get(0);

// 类型消除
ArrayList list = new ArrayList<>();
list.add("test");
String state = (String) list.get(0);
```

需要注意的是，不管具体的类型是什么，泛型类是被所有实例所共享的。如：

```java
ArrayList<String> list1 = new ArrayList<>();
ArrayList<Integer> list2 = new ArrayList<>();
```

尽管在编译时是两种类型，但加载到 JVM 中时只有一个 ArrayList 类会被加载，在运行时使用 `ArrayList<String>` 类毫无意义。由此，泛型的使用有一些限制：

- 不能使用 `new T()`，即 `T obj = new T()` 是错误的，数组同理
- 在静态上下文中不允许类的参数是泛型类型
- 异常类不能是泛型的

## 八、集合框架

Java 中的集合是能够存放其他对象的一种对象，它相当于一个容器，提供了保存、删除、修改其中元素的方法。容器主要包括 Collection 和 Map 两种，Collection 又包含了 List、Set 以及 Queue。

### 1. Collection 接口

![](http://oqag5mdvp.bkt.clouddn.com/201806031630_176.png)

**Collection 接口允许对象集中存放在一起**。它提供了很多有用的方法，例如：

- `add()`：添加元素
- `addAll()`：添加另一个 Collection 的所有成员
- `clear()`：删除所有元素
- `size()`：返回元素数量
- `isEmpty()`：测试该集合是否包含元素
- `remove(Object o)`：移除某元素
- `removeAll(Collecton <?> c)`：移除 c 中的所有元素
- `contains(Object o)`：测试是否包含 o
- `containsAll(Collection<?> c)`：测试是否包含 c 中的所有元素

### 2. List

List 接口继承自 Collection 接口，它定义了一个允许重复的有序集合，增加了面向位置的操作。List 接口定义的方法如下：

- `get(int index)`：返回指定索引处的元素
- `indexOf(Object element)`：返回指定元素的索引（匹配第一个）
- `lastIndexOf(Object element)`：返回最后一个匹配元素的索引
- `set(int index, Object element)`：设置某个索引处的元素
- `subList(int fromIndex, int toIndex)`：返回从 fromIndex 到 toIndex-1 的子线性表
- `listIterator()`：返回针对该线性表元素的迭代器
- `listIterator(int startIndex)`：返回从 startIndex 开始的元素迭代器

#### ArrayList

ArrayList 是 List 接口的一个具体实现，它用数组存储元素，需要用下标访问元素时，ArrayList 是一个很好地选择。 

- 构造器：默认的无参构造器初始容量为 10，随着元素添加进去不断扩大。事先知道容量的话可以指定容量大小，`public ArrayList(int initialCapacity)`。
- `trimToSize()`：将该 ArrayList 实例的容量裁剪到当前大小

#### LinkedList

LinkedList 使用的链表来实现 List 接口，方便进行元素的插入删除。

- `addFirst(E element)`：添加元素到首部，对应的方法是 `addLast()`
- `getFirst()`：返回第一个元素，对应的还有 `getLast()`
- `removeFirst()`：移除第一个元素，对应的还有还有 `removeLast()`

### 3. Set

Set 类似于 List，但 Set 不允许重复。Set 接口有三个具体类：散列类 HashSet、链式散列集 LinkedHashSet 和树形集 TreeSet。

#### 3.1 HashSet

HashSet 类可以用来存储各不相同的任何元素。考虑到效率的因素，添加到 HashSet 中的对象必须以一种正确分散散列码的方式来实现 hashCode 方法。如果两个对象相等，则散列码必须相同。

实例化 HashSet 时可以使用无参构造方法，默认的 HashSet 大小为 16，负载系数为 0.75。

负载系数指定了当集合多大时应该翻倍（大小 16，系数 0.75，则 16 * 0.75 = 12，当元素达到 12 个时大小翻倍）。如果事先知道元素个数可以指定容量和负载系数。

#### 3.2 LinkedHashSet

LinkedHashSet 从 HashSet 继承，它用链表扩展了 HashSet 类，从而可以按照插入集合的顺序提取。构造方法类似于 HashSet。

#### 3.3 TreeSet

TreeSet 实现了 SortedSet 接口，SortedSet 是 Set 的一个子接口。SortedSet 接口保证了集合中的元素是有序的，而且还提供了 `first()` 和 `last()` 方法，分别返回第一个和最后一个元素。以及 `headSet(toElement)` 方法和 `tailSet(fromElement)` 方法返回集合中小于 toElement 和大于等于 fromElement 的那一部分。

另外，TreeSet 还实现了 NavigableSet 接口，该接口是 SortedSet 的子接口。它提供了导航方法 `lower(e)`、`floor(e)`、`ceiling(e)` 和 `higher(e)` 分别返回小于、小于等于、大于或等于以及大于一个给定元素的元素。如果没有这样的元素，返回 null。方法 `pollFirst()` 和 `pollLast()` 分别会删除并返回第一个、最后一个元素。

只要一个对象是可以比较的，就可以添加到 TreeSet 中来。

```java
import java.util.HashSet;
import java.util.Set;
import java.util.TreeSet;

public class TestTreeSet {
    public static void main(String[] args) {
        Set<String> set = new HashSet<>();

        set.add("London");
        set.add("Paris");
        set.add("New York");
        set.add("London");
        set.add("San Francisco");
        set.add("Beijing");

        TreeSet<String> treeSet = new TreeSet<>(set);
        System.out.println("Sorted tree set: " + treeSet);

        System.out.println("first: " + treeSet.first());
        System.out.println("last: " + treeSet.last());
        System.out.println("headSet(\"New York\"): " + treeSet.headSet("New York"));
        System.out.println("tailSet(\"New York\"): " + treeSet.tailSet("New York"));

        System.out.println("lower P: " + treeSet.lower("P"));      // 小于
        System.out.println("higher P: " + treeSet.higher("P"));     // 大于
        System.out.println("floor P: " + treeSet.floor("P"));      // 小于或等于
        System.out.println("ceiling P: " + treeSet.ceiling("P"));    // 大于或等于

        System.out.println("pollFirst " + treeSet.pollFirst());
        System.out.println("pollLast: " + treeSet.pollLast());
    }
}
```

### 4. Queue

LinkedList 也实现了 Queue 接口。Queue 支持 FIFO（先进先出）的原则。常用方法如下：

- `offer`：类似 add 方法，但它在添加元素有可能失败时调用。若添加失败，返回 false，add 添加失败时则返回异常。
- `remove`：删除并返回 Queue 最前端的那个元素，若 Queue 为空时抛出异常
- `poll`：同 remove，但 Queue 为空时返回 null
- `element`：返回但不删除 Queue 最前端的元素，若 Queue 为空抛出异常
- `peek`：同 element，但 Queue 为空时它返回 null

### 5. Map

![](http://oqag5mdvp.bkt.clouddn.com/201806031639_592.png)

Map 是保存键 / 值对的地方，键不允许重复，每个键只能映射到一个值。Map 的常用实现有三种：散列映射表 HashMap、链式散列映射表 LinkedHashMap 和树形散列表 TreeMap。它们的结构和 Set 的三种实现类似。

- 添加一个键值对：`public void put (Object key, Object value)`。需要注意的是，键和值都不能是基本类型，但类似 `put(1, 100)` 这样的调用是合法的。因为在调用之前进行了自动装箱。
- 添加一个 Map：`public putAll(Map map)`。
- 删除所有键和值：`clear()`
- 键值数量：`size()`
- 是否为空：`isEmpty`
- 取一个值：get(key)
- 获取所有键：keySet() 方法，返回一个 Set 类型
- 获取所有值：values() 方法，返回一个 Collection
- 是否包含一个键：containsKey(Object key)
- 是否包含一个值：containsValue(Object value)

```java
import java.util.HashMap;
import java.util.Map;

public class TestMap {
    public static void main(String[] args) {
        Map<String, Integer> hashMap = new HashMap<>();

        hashMap.put("Smith", 30);
        hashMap.put("Lin", 25);
        hashMap.put("Tom", 28);

        System.out.println(hashMap);
        System.out.println("The age of Tom is: " + hashMap.get("Tom"));
    }
}
```

## 注解

### 1. 用途

注解是插入到源代码中使用其他工具可以进行处理的标签，注解并不会改变程序的编译方法。

### 2. 语法

**定义注解**

注解是由注解接口来定义的：

```java
// 语法
modifiers @interface AnnotationName {
    elementDeclaration;
}

// 实例
public @interface BugReport{
    String assignedTo() default "none";
    int severity();
}
```

**使用注解**

```java
@BugReport(assignedTo="Harry", severity=10)

// 当元素的名字为特殊值『value』时可以不指定名称
public @interface ActionListenerFor {
    String value;
}

@ActionListenerFor("default")
```

所有的注解接口都隐式的继承自 java.lang.annotation.Annotation。注解元素的类型可以为下列之一：

- 基本类型
- String
- Class
- enum 类型
- 注解类型
- 由前面所述类型构成的数组

需要注意的是，由于注解是由编译器计算而来的，因此所有的元素值都必须是编译期常量。

### 3. 标准注解

- @Deprecated：用于标注过时的项
- @SuppressWarnings：阻止给定类型的警告信息
- @