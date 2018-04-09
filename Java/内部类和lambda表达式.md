# 内部类和lambda表达式

### 1. lambda表达式

lambda表达式是一个可传递的代码块，可以在以后执行一次或多次。它起到的是一个匿名函数的作用。之所以叫匿名函数，是因为lambda表达式没有名称。

试考虑以下的一个比较器代码：

```java
class LengthComparator implements Comparator<String> {
    public int compare(String first, String second) {
        return first.length() - second.length(;
    }
}
```

使用这个比较器时，需要将比较器对象通过参数传给Arrays.sort方法：

```java
Arrays.sort(strings, new LengthComparator());
```

此次将代码块作为参数传递给了调用方。类似这样的调用可以用lambda表达式简化代码：

```java
(String first, String second)
	-> first.length() - second.length()
```

上面是lambda表达式的一种形式：参数（括号括起来）、箭头和一个表达式。如果所需要进行的计算在一个表达式内无法完成，可以像写方法那样，将代码放入花括号内。

```java
(String first, String second) ->
{
    if(first.length() < second.length()) return -1;
    else if (first.length > second.length) return 1;
    else   return 0;
}
```

注意参数的括号是必须的，即使无参时也需要提供空括号。

#### 1.1 函数式接口

对于只有一个抽象方法的接口，需要这种接口的对象时，就可以提供一个lambda表达式。这种接口称为**函数式接口（functional interface）**。

java.util.function包中定义了很多通用的函数式接口，例如BiFunction<T, U, R>，它描述了参数类型为T和U而返回值为R的函数。

```java
BiFunction<String, String, Integer> comp = 
    (first, second) -> first.length() - second.length();
```

另外java.util.function包中还有一个有用的Predicate接口：

```java
public interface Predicate<T> {
    boolean test(T t);
}
```

ArrayList类有一个removeIf方法，参数就是一个Predicate。利用这个方法可以移除特定的元素：

```java
list.removeIf(e -> e == null);
```

#### 1.2 方法引用

假如想要将字符串排序，而不考虑字母的大小写，可以传递以下的表达式：

```java
Arrays.sort(strings, String::compareToIgnoreCase)
```

这样的表达式被称为**方法引用（method reference）**，它等价于lambda表达式(x, y) -> x.compareToIgnoreCase(y)。

用::操作符分隔方法名和类名，主要有三种情况：

- object::instanceMethod
- Class::staticMethod
- Class::instanceMethod

在前两种情况下，方法引用等价于提供方法参数的lambda表达式，第三种情况，第一个参数会成为方法的目标。