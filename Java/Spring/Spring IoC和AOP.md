# Spring IoC和AOP

### 1. 为何Spring

Spring可以做很多事情。但归根结底，Spring最根本的使命只有一个：**简化Java开发**。

不同于重量级的EJB（企业级JavaBean，Enterprise JavaBean），Spring是基于POJO（Plain Ordinary Java Object，简单Java对象）的。那么Spring是如何做到降低开发复杂型的呢？

- 基于POJO的轻量级和最小侵入式编程
- 通过依赖注入和面向接口实现松耦合
- 基于切面和惯例进行声明式编程
- 通过切面和模板减少样板式代码

或许Spring中最重要的概念就是IoC（控制反转）和AOP（面向切面编程）。下面我们就来看看这两个重要的思想。

### 2. IoC

IoC即Inversion of Control，中文译作“控制反转”，也叫作依赖注入（Dependency Injection）。

既然叫做“控制反转”，那么是反转了什么呢？其实反转的就是**依赖对象的创建方式**。正常情况下我们自己回去利用`new`关键字新建对象。但在IoC的设计理念下，这个新建过程转交给了Spring的容器，即我们需要对象时，只需通知容器一下即可获得我们所需的对象，而具体的新建过程由容器操控。

那这个“通知容器”的动作是怎么实现的呢？有三种依赖注入的方式，即构造方法注入（constructor
injection）、setter方法注入（setter injection）以及接口注入（interface injection）。

先看一个耦合的骑士探险的例子：

```java
public class DamselRescuingKnight implements Knight {
    private RescueDamselQuest quest;

    public DamselRescuingKnight() {
    	this.quest = new RescueDamselQuest();
    }
    public void embarkOnQuest() {
    	quest.embark();
    }
}
```

DamselRescuingKnight在构造函数中自行创建了RescueDamselQuest，它们两个紧紧地耦合在了一起。如此固然能够发挥作用，但也同样限制了骑士能做的事情。

**耦合具有两面性。**一方面耦合的代码难以测试、难以理解、难以复用，但一定程度的耦合又是必须的——完全不耦合的代码什么也做不了。尽管如此，我们应该最大程度的解耦合。下面是一个例子：

```java
public class BraveKnight implements Knight {
    private Quest quest;

    public BraveKnight(Quest quest) {
    	this.quest = quest;
    }
    public void embarkOnQuest() {
    	quest.embark();
    }
}
```

不同于之前的DamselRescuingKnight，BraveKnight在构造时将探险任务作为参数传入，从而能够完成更多的任务。这就是依赖注入的方式之一，构造器注入。

### 3. AOP

AOP即Aspect Oriented Programming，面向切面编程。

#### 3.1 AOP术语

**通知（Advice）**

切面的工作被称为通知。通知定义了切面是什么以及何时使用。除了描述切面要完成的工作之外，通知还解决了何时执行这个工作的问题。

Spring内置了五种类型的通知：

- 前置通知（@Before）：在目标方法被调用之前调用通知功能
- 后置通知（@After）：在目标方法被调用之后（不关心方法的输出是什么）
- 返回通知（@AfterReturn）：在目标方法成功执行之后调用通知
- 异常通知（@AfterThrow）：在目标方法抛出异常后调用通知
- 环绕通知（@Around）：包裹了被通知的方法，调用之前、之后执行

**连接点（Join Point）**

我们的应用可能有很多个时机应用通知，这些时机被称为连接点。连接点是在应用执行过程中能够插入切面的一个点。

**切点（Pointcut）**

通知定义了“何时”和“什么”，切点定义了“何处”。

**切面（Aspect）**

切面是通知和切点的集合，它是什么、它在何处完成什么功能

**引入（Introduction）**

引入允许我们向现有的类添加新方法和树形。在不修改现有类的前提下引入新的功能

**织入（Weaving）**

织入是把切面应用到目标对象并创建新的代理对象的过程。切面在指定的连接点被织入到目标对象中。在目标对象的生命周期中有多个点可以进行织入：

- 编译器：切面在目标类编译时被织入，需要特殊的编译器
- 类加载期：切面在目标类加载到JVM时被织入，需要特殊的类加载器
- 运行期：Spring AOP就是以这种方式织入切面的





