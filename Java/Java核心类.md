# Java 核心类

### 1. java.lang.Object

javal.lang.Object 是 Java 中最重要的类，其他的所有类都是隐式从它继承而来。它提供了下面几个通用方法：

- `protected Object clone()`：创建并返回这个对象的一个副本，类实现这个方法以支持对象复制
- `public boolean equals(Object obj)`：将这个对象与传入对象比较，返回两个对象是否相等
- `protected void finalize()`：由垃圾回收期在一个即将回收的对象上调用
- `public final class getClass()`：返回这个对象的一个 java.lang.Class 对象
- `public int hashCode()`：返回这个对象的哈希值
- `public String toString()`：返回这个对象的描述
- 除此之外多线程应用中还有 `wait()`、`notify()` 和 `notifyAll()` 方法

### 2. java.lang.String

一个 String 对象表示一个字符串，也可以把一个 String 当做是一串 Unicode 字符。String 对象是不可变对象，一旦创建它的值就不能被更改。由于 String 对象太过常用，Java 提供了一种比 new 关键字更简便的方式创建 String 对象：`String s = "Hello, world"`。

需要注意的是，使用 new 关键字时，JVM 始终会创建一个新的实例。但使用上述方法创建时，若内存中已有该字面值时 JVM 并不会新建对象（类似 Python 的驻留机制）。

另外，比较两个字符串时，我们通常需要比较的是值，应采用 `s.equals(s1)` 方法。当 s 为 null 时表达式会出错，所以通常写为：`if(s != null && s.equals(s1))`

String 类的常见方法如下：

- `public char charAt(int index)`：返回指定索引处的字符
- `public boolean endsWith(string suffix)`：测试该字符串是否以 suffix 结尾，类似的还有 `startsWith()` 方法
- `public int indexOf(String substring)`：返回第一次遇到的指定子字符串的索引，没找到的话返回 -1
- `public int lastIndexOf(String substring)`：返回最后一次遇到子字符串的索引，没找到返回 -1
- `public int length()`：返回字符串的长度
- `public Boolean isEmpty()`：测试字符串是否为空串
- `public String[] split(String regEx)`：根据指定的正则表达式将字符串分解并返回分解后的数组
- `public char[] toCharArray()`：将字符串转化为一个字符数组
- `public String toLowerCase()`：将字符串转化为小写；类似的 `toUpperCase()`
- `public String trim()`：去掉字符串前后的空格，类似 Python 的 `strip()` 方法

### 3. java.lang.StringBuffer 和 java.lang.StringBuilder

由于 String 对象不可变，不便于对其进行修改。如果需要对字符串进行修改操作，可以使用 StringBuilder 或者 StringBuffer 对象，完成操作后再转换成为 String。

StringBuffer 是同步（synchronized）的，适用于多线程，但性能较差。如果在其他场景下运用，可以考虑使用 StringBuilder。它们的方法是相同的。

**构造器**

StringBuilder 类有 4 中构造器，分别为：无参、`StringBuilder(CharSequence seq)`、`StringBuilder(int capacity)` 和 `StringBuilder(String string)`。

如果创建时没有指定容量，默认容量为 16 个字符。超过后会自动变大。但申请额外的容量需要消耗时间，如果实现知道大小就应该配置足够大的容量。

**常用方法**

- `public int capaticy()` ：返回对象的容量
- `public int length()`：返回对象保存的字符串长度
- `public StringBuilder append(String string)`：将指定的 String 添加到所包含字符串的结尾处。该方法返回的是对象本身，可以连续调用：sb.append("s").append(2)
- `public StringBuilder insert(int offset, String string)`：在 offset 出插入 string，可连续调用
- `public String toString()`：返回 String 对象

### 包装类型

Java 中的基本类型（byte,int, char, short, long, boolean, double, float) 并不是对象。而我们经常会用到基本类型和对象的互相转换，由此就有了基本类型的包装类。将每种基本类型首字母大写即是包装类型的类名（Integer 和 Character 除外）。下面拿 `java.lang.Integer` 为例讲解这几个包装类型。

**java.lang.Integer**

Integer 类有两个构造器，分别传入 int 型和 String 类型，将其转换为 Integer 类型。如 `Integer i1 = new Integer("1")`。

Integer 具有无参的 `byteValue`、`doubleValue`、`floatValue`、`intValue`、`longValue` 和 `shortValue` 方法，将所包装的值转化为对应的基本类型。

最后，Integer 类还有一个静态方法 `parseInt()`，将 String 解析为 int。`public static int parseInt(String string)`。

**java.lang.Boolean**

该类同样有两个构造器，分别从 boolean 类型和 String 类型构造一个 Boolean 对象：

`public Boolean(boolean value)` 和 `public Boolean(String value)`。

将 Boolean 类型转化为 boolean 类型使用 `booleanValue()` 方法：`public boolean booleanValue()`。

**java.lang.Character**

该类只有一个构造器：`public Character(char value)`。

Character -> char：`public char charValue()`。

判断参数是否为数字：`public static boolean isDigit(char ch)`。

### 数组

数组是一种特殊的 Java 对象，创建数组时不会有类被实例化。

**声明数组**

`type[] arrayName;` 或者 `type arrayName[] `（通常用第一种方法）。

声明并不会分配空间，只有利用 new 关键字指定创建大小时数组才会被分配空间。声明的同时可以立即初始化：

`int [] nums = new int[10];`。

需要注意的是，同 C 语言不同，访问超出范围的数组成员会抛出异常。



