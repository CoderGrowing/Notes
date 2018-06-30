# Java 函数式

## 一、行为参数化

Java 8  中函数变成了一等公民，即函数也可以像值那样进行传递。通过将函数作为参数传递，我们可以高度定制代码的行为，这种方式叫做**行为参数化**。

假设我们有一堆苹果，我们需要筛选出绿色的来，代码可以这样写：

```java
public static List<Apple> filterGreenApple(List<Apple> inventory) {
    List<Apple> result = new ArrayList<>();

    for (Apple apple : inventory)
        if ("green".equals(apple.getColor()))
            result.add(apple);
    return result;
}
```

那如果我现在有想要筛选出红色的呢？或者我想筛选出重量大于 200g 的？很简单，我们可以将代码复制一份，然后修改 if 中的判断条件……

等等！这样做对么？我们已经违反了 DRY 原则！此时行为参数化可以帮助我们解决这个问题：

首先定义一个接口表示标准的选择：

```java
public interface ApplePredicate {
    boolean test (Apple apple);
}
```

然后再根据需求给出接口的具体实现，例如我们需要筛选出绿色苹果：

```java
public AppleGreenColorPredicate implements ApplePredicate {
    public boolean test(Apple apple) {
        return "green".equals(apple.getColor());
    }
}
```

这时候我们就可以按照需求来筛选苹果啦 ~

```java
static List<Apple> filterApples(List<Apple> inventory, ApplePredicate<Apple> p) {
    List<Apple> result = new ArrayList<>();

    for (Apple apple : inventory)
        if (p.test(apple))
            result.add(apple);

    return result;
}

// 调用
filterApples(inventory, new AppleGreenColorPredicate());
```

行为参数化体现了『策略设计模式』，我们定义一簇算法，然后在运行时选择需要的算法。

## 二、Lambda

Lambda 表达式可以理解为可传递的匿名函数：它没有名称，但它有参数列表、函数主体和返回类型。

### 1. 语法

```java
(int a, int b) -> a + b;
```

Lambda 表达式的第一部分是**参数列表**，上例中的参数为两个 int 型的参数 a 和 b。第二部分是**箭头**，箭头将参数列表和主体分开。第三部分就是**主体**了，Lambda 主体完成函数的功能并返回值。

需要注意在 Lambda 表达式中并不需要显式的使用 return 语句来返回值， return 已经隐含在 Lambda 表达式中了。当然，如果你习惯使用 return 也可以。

### 2. 使用

#### 2.1 函数式接口

Lambda 表达式可以在函数式接口上使用。**函数式接口**就是只定义了**一个**抽象方法的接口。

```java
public interface Adder {
    int add(int a, int b);
}    // 是函数式接口

public interface AnotherAdder extends Adder {
    int add(double a, double b);
}    // 不是函数式接口，因为它定义了两个抽象方法 ( 从 Adder 那继承了一个 )
```

Lambda 表达式允许我们以内联的形式为函数式接口的抽象方法提供实现，并把整个表达式作为函数式接口的实例，类似于匿名内部类。下面看一个使用 Lambda 表达式和匿名内部类完成相同功能的例子：

```java
Runnable r1 = new Runnable() {
    public void run() {
        System.out.println("I am running!");
    }
};  // 使用匿名内部类

Runnable r2 = () -> System.out.println("I am running!");  // 使用 Lambda 表达式
```

利用 Lambda 表达式还可以简化我们之前写的那个筛选绿苹果的程序：

```java
static List<Apple> filterApples(List<Apple> inventory, ApplePredicate<Apple> p) {
    List<Apple> result = new ArrayList<>();

    for (Apple apple : inventory)
        if (p.test(apple))
            result.add(apple);

    return result;
}

// 调用
filterApples(inventory, (Apple apple) -> "green".equals(apple.getColor()));
```

## 三、流

Java 8 中新增了流 API，它允许我们以声明性的方式处理数据集合（通过查询语句来表达，而不需要再编写实现）。使用流 API 是站在比集合更高的层面上看待问题的。

### 1. 流与集合

流与集合之间的差异在于什么时候进行运算。集合是已经存储了数据结构中所有的值，而流则是什么时候需要什么时候再进行计算。（类比 Python 中的生成器和迭代器）。

- 流只能遍历一次
- 流进行的是内部迭代，而集合进行的是外部迭代

### 2. 筛选与切片

#### 2.1 筛选元素 

filter 方法会接收一个谓词，并返回所有符合谓词的元素的流。

```java
List<Integer> evenList = list.stream()
    					   .filter(i -> i % 2 == 0)
    					   .collect(toList);
```

#### 2.2 去除重复元素

distinct 方法返回一个没有重复元素的流（根据 hashCode 和 equals 方法确定）。

```java
List<Integer> noDupList = list.stream()
    					   .distinct()
    					   .collect(toList);
```

#### 2.3 截短流

limit(n) 方法可以将流截短，返回长度为 n 的流。

#### 2.4 跳过元素

skip(n) 方法返回一个扔掉了前 n 个元素的流。如果流的长度不足 n，则返回一个空流。limit(n) 方法和 skip(n) 方法是互补的。

### 3. 映射

#### 3.1 对流中的每一个元素应用函数

流支持 map 方法，接收一个函数作为参数，将函数应用到流中的每个元素上，并将其映射为一个新的元素。

```java
List<String> dishNames = menu.stream()
    					   .map(Dish::getName)
    					   .collect(toList());
```

将 Dish::getName 方法应用到每一个元素上并返回元素的名称。

#### 3.2 将流扁平化

流还支持一个 flatMap 方法，利用它可以将流扁平化。

假设我们有一个单词数组：

```java
String[] words = new String[] {"Hello", "World"};
```

我们需要返回一个不重复的字母的列表，即 ["H", "e", "l", "o", "W", "r", d]，利用 map 方法我们可以这样做：

```java
Stream<String> streamWords = Arrays.stream(words);
streamWords.stream()
     .map(s -> s.split(""));  
     .distinct()
     .collect(toList());
// [['H', 'e', 'l', 'l', 'o'], ['W', 'o', 'r', 'l', 'd']]
```

得到的结果却不是我们想要的，因为 map 方法在这返回的结果是 `Stream<String [] >` 类型的。此时就需要用 flatMap 方法将流扁平化：

```java
streamWords.stream()
           .map(w -> w.split(""))
           .flatMap(Arrays::stream)  // 将各个生成流扁平化为单个流
           .distinct()
           .collect(toList());
```

flatMap 方法可以将一个流中的每个值都变成一个流，最后将所有的流都连接起来。

### 4. 查找和匹配

#### 4.1 匹配

**anyMatch **

anyMatch 方法可以检查流中是否有一个元素能匹配给定的谓词。

```java
if (menu.stream().anyMatch(Dish::isVegetarian)) // doSomething
```

**allMatch**

allMatch 方法可以检查一个流中是否所有元素都能匹配给定的谓词。

```java
if (menu.stream().allMatch(Dish::isVegetarian)) // doSomething
```

**noneMatch**

noneMatch 方法可以检查一个流中是否所有的元素都不匹配给定的谓词。

```java
if (menu.stream().noneMatch(Dish::isVegetarian)) // doSomething
```

#### 4.2 查找

**findAny**

findAny 方法返回当前流中的任意元素。

```java
Optional<Dish> dish = 
    menu.stream().filter(Dish::isVegetable).findAny();  // 返回任意一道素食
```

**findFirst**

findFirst 方法可以返回流中的第一个元素，不过只有当流是有序流的时候才有意义。

```java
Optional<Dish> dish = 
    menu.stream().filter(Dish::isVegetable).findFirst();  // 返回第一道素食
```

### 5. 归约

有时候我们需要从流中的所有数据结合起来得到一个值，比如得到卡路里最高的一道菜肴。这样从流的所有数据中得到一个值的操作叫做**归约**。

**reduce**

reduce 接收两个参数：

- 初始值
- 一个 `BinaryOperator<T>` 将两个元素结合起来产生一个新值。如利用 reduce 来求数组中所有元素的和：

```java
int sum = numbers.stream().reduce(0, Integer::sum);
```

另外，reduce 还有一个重载的变体，它不接受初始值，但是会返回一个 Optional 对象：

```java
Optional<Integer> sum = numbers.stream().reduce(Integer::sum);
```

### 6. 数值流

对数值的操作时非常常见的，Stream API 特别为数值操作提供了**原始类型流特化**来专门支持处理数值流的方法。

Java 8 引入了三种原始类型特化流：IntStream、DoubleStream 和 LongStream 分别对应 int、long 和 double。

**映射到数值流**

将流映射到数值流的常用方法有 mapToInt、mapToDouble 和 mapToLong。

```java
int calories = menu.stream()    // 返回一个 Stream<Dish>
       			  .mapToInt(Dish::getCalories)  // 返回一个 IntStream
    			  .sum();
```

**转化为对象流**

有了原始类型的流进行操作后，有时还需要转化为非特化的对象流进行操作，此时可以用 boxed 方法：

```java
IntStream intStream = menu.stream().mapToInt(Dish::getCalories);
Stream<Integer> stream = intStream.boxed;   // 将数值流转化为 Stream
```

**数值范围**

range 和 rangeClosed 是两个可以用于 IntStream 和 LongStream 的静态方法，用于生成一个数值范围。

```java
IntStream hunderNumbers = IntStream.rangeClosed(1, 100);
```

这两个方法都是接收两个参数：第一个参数是起始值，第二个参数为结束值。range 方法不包含结束值，而 rangeClosed 方法包含结束值。

## 四 . 并行数据处理

### 1.1 并行流

流的出现让并行处理变得容易，只需要将 Stream 替换为为 parallelStream 即可使用并行流。同样，现有的流也可以通过 parallel 方法来转换为并行流：

```java
stream.parallel()
      .filter(...)
      .reduce();
```

那么，并行流内部是如何实现的？并行流用到的线程是从哪里来的呢？

**并行流的内部实现**

并行流内部使用了默认的 ForkJoinPool，默认的线程数量就是你所用计算机处理器的数量，这个值可以通过 `Runtime.getRuntime().availableProcessors()` 获取。

我们可以通过修改系统属性 java.util.concurrent.ForkJoinPool.common.parallelism 来改变线程池大小。

**并行流的性能问题**

并行流就一定比顺序流效率高么？并不见得。一些具有依赖关系的操作很难将其并行化，尝试并行反而会增加系统开销。考虑使用并行流之前应当先考虑问题是否适合使用并行流进行解决。以下是几点建议：

- 测量。通过测量来确定到底是并行还是顺序流的速度更快
- 留意自动装箱 / 拆箱。自动装 / 拆箱会大大降低性能，应当尽量使用原始类型流
- 数据量很小时，不应使用并行流
- 依赖元素顺序的操作并行代价很大
- 考虑操作背后的数据结构是否容易拆分，像 ArrayList 的查分效率就远远大于 LinkedList

### 1.2 分支 / 合并框架

分支 / 合并框架的目的是以递归方式将可以并行的任务拆分为更小的任务，然后将每个子任务的结果合并起来生成整体结果。它是 ExecutorService 接口的一个实现。它把子任务分配给线程池（ForkJoinPool）中的工作线程。

#### 1.2.1 RecursiveTask

为了将任务提交给线程池，我们需要用到 `RecursiveTask<R>`，其中 R 是并行化任务产生的结果类型。要定义 RecursiveTask 只需要实现它唯一的抽象方法 compute：

```java
protected abstract R compute();
```

这个方法定义了将任务拆分为子任务的逻辑，以及无法拆分时生成单任务的逻辑。

**工作窃取**

在使用多线程并发解决任务的时候经常会碰到一些线程忙碌而一些线程闲置的情况，造成资源的浪费。分支 / 合并框架使用了一种叫做工作窃取（work stealing）的技术来解决这个问题。

起始任务会被大致均匀的分配到 ForkJoinPool 中的所有线程上，每个线程都为分配给它的任务保存一个双向链式队列，每完成一个任务就从队列头取下一个任务执行。

当某个线程早早执行完自己的任务后，它会随机选择一个其他的线程，从该线程的队列尾部“偷走”一个任务，从而避免资源的浪费。

也因此，任务应该划分为多个小任务，而不是少数几个大任务。

#### 7.3 Spliterator

Spliterator 是 Java 8 中加入的一个新接口，用于遍历数据源中的元素。它类似于 Iterator，但它是为并发执行而设计的。

```java
public interface Spliterator<T> {
    boolean tryAdvance(Consumer<? super T> action);
    Spliterator<T> trySplit();
    long estimateSize();
    int characteristics();
}
```

在使用 Spliterator 的过程中，它会不断地将 Stream 拆分为多个部分。拆分是一个递归的调用过程，对原始的 Spliterator 调用 trySplit 方法，得到两个 Spliterator，然后再对这两个 Spliterator 调用 trySplit 方法，得到四个 Spliterator …直到 trySplit 方法返回 null 表示无法再进行分割。

tryAdvance 方法类似于普通的 Iterator，它会按顺序一个一个的使用 Spliterator 中的元素，如果还有元素需要遍历就返回 true。

最后 characteristics 方法返回 Spliterator 本身特性集的编码。

### 8. 创建流

**由值创建流**

通过静态方法 Stream.of 可以通过值显式的创建一个流：

```java
Stream<String> stream = Stream.of("Java 8", "in", "Action");
```

还可以使用 Stream.empty 得到一个空流：

```java
Stream<String> emptyStream = Stream.empty();
```

**由数组创建流**

```java
int[] numbers = {1, 2, 3, 4, 5};
int sum = Arrays.stream(numbers).sum();
```

### 9. 收集数据

#### 9.1 收集器

```java

```

**预定义的收集器**

Java 内置了一部分常用的收集器，它们主要可以用来完成以下功能：

- 将流元素归约和汇总为一个值
- 元素分组
- 元素分区

#### 9.2 归约和汇总



## 六、Optional

## 七、异步

