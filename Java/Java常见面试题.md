## Java常见面试题及答案

### 1. StringBuilder和StringBuffer

**为何要用到StringBuilder或StringBuffer**

有时候需要用多个较短的字符构建字符串。因为字符串时不可变的，所以每次连接字符串都会构建新的String对象，既耗时也浪费空间。此时可以采用StringBuffer或者StringBuilder来解决这个问题。

```java
StringBuilder builder = new StringBuilder();
builder.append("hello, ");
builder.append("world.");
```

构建完成后，调用`toString()`方法就可以得到一个String对象：

```java
String resultString = builder.toString();
```

**StringBuilder和StringBuffer的区别**

StringBuffer的效率较低，但允许多线程执行添加或删除字符的操作。

StringBuilder类是JDK5.0引入的StringBuffer改进版，它的效率高，但无法并发操作。它们两个的API是相同的。

**常用方法**

下面拿StringBuilder当做例子来说明常用API：

- `StringBuilder`：构建一个空的StringBuilder
- `length()`：返回StringBuilder中的代码单元数量
- `append(char c)`：添加一个代码单元并返回this
- `append(String str)`：添加一个字符串并返回this
- `setCharAt(int i, char c)`：将第i个代码单元设置为c
- `toString()`：构建字符串

### 2. String为何不可变，如何实现的不可变

### 3.

