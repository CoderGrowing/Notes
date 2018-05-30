# Java常见面试题及答案

## 1. StringBuilder和StringBuffer

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

## 2. String为何不可变，如何实现的不可变

### 如何实现的不可变

利用final

### 为何要设置为不可变

**1. 可以缓存 hash 值** 

因为 String 的 hash 值经常被使用，例如 String 用做 HashMap 的 key。不可变的特性可以使得 hash 值也不可变，因此只需要进行一次计算。

**2. String Pool 的需要** 

如果一个 String 对象已经被创建过了，那么就会从 String Pool 中取得引用。只有 String 是不可变的，才可能使用 String Pool。

<div align="center"> <img src="D:/interview/pics/f76067a5-7d5f-4135-9549-8199c77d8f1c.jpg" width=""/> </div><br>

**3. 安全性** 

String 经常作为参数，String 不可变性可以保证参数不可变。例如在作为网络连接参数的情况下如果 String 是可变的，那么在网络连接过程中，String 被改变，改变 String 对象的那一方以为现在连接的是其它主机，而实际情况却不一定是。

**4. 线程安全** 

String 不可变性天生具备线程安全，可以在多个线程中安全地使用。

> [Why String is immutable in Java?](https://www.programcreek.com/2013/04/why-string-is-immutable-in-java/)

## 3.

