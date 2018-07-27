# Spring 之 IoC与 AOP

## 1. 什么是 IoC

IoC 即 Inversion of Control，中文译作“**控制反转**”，也叫作**依赖注入**（Dependency Injection）。

既然叫做“控制反转”，那么是反转了什么呢？反转的就是**依赖对象的创建方式**。正常情况下我们自己回去利用 `new` 关键字新建对象。但在 IoC 的设计理念下，这个新建过程转交给了 Spring 的容器，即我们需要对象时，只需通知容器一下即可获得我们所需的对象，而具体的新建过程由容器操控。

首先来看一个不依靠依赖注入的例子：

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

DamselRescuingKnight 在构造函数中**自行创建**了 RescueDamselQuest，它们两个紧紧地耦合在了一起。如此固然能够发挥作用，但也同样限制了骑士能做的事情。

为了解耦，我们将创建的过程交给其他类来处理，在构造函数中传入 Quest 即可：

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

不同于之前的 DamselRescuingKnight，BraveKnight 在构造时将探险任务作为参数传入，从而能够完成更多的任务。

```java
public class Dispatcher {
    public void dispatch() {
        // 指定探险任务
        Quest quest = new SomeQuest();
        
        // 将探险任务注入
        BraveKnight knight = new BraveKnight(quest);
    }
}
```

但即便如此，探险任务的初始化仍需要我们来完成，只是这些工作转到了另一个类中去。那么可不可以有一个“第三方”的机构，帮助我们完成初始化和装配工作呢？ Spring 就扮演了这样的一个角色。

我们只需要提供给 Spring 类的信息，这样当我们需要时，Spring 就可以创建类并交还给我们。由此，创建实例化类的工作由 new 的方式变成了 Spring 容器创建，实现了“控制反转”。

## 2. 装配 Bean

为了让 Spring 替我们管理应用程序中的 Bean，我们必须告诉 Spring 如何去管理，以及 Bean 之间的依赖关系等。创建应用对象之间协作关系的行为被称为**装配（wiring）**。这也是依赖注入的本质。

Spring 提供了两种注入依赖的配置供我们使用，即基于注解的配置和基于 XML 的配置。而依赖注入的方式有三种，分别是**构造方法注入**（constructor injection）、**setter 方法注入**（setter injection）以及**接口注入**（interface injection）。对于这三种方式我们分别来看下如何使用 Spring 来进行依赖注入。

### 2. 1. 可选的装配方案

Spring 主要提供了三种装配机制：

- 隐式的 bean 自动发现和自动装配机制
- 显式的利用 Java 进行配置
- 显式的利用 XML 进行配置

推荐尽可能的使用自动装配机制，必须要显式配置时，尽量采用 Java 配置的方式。

#### 2.1.1 自动化装配

Spring 从两个角度实现自动化装配：

- **组件扫描（component scanning）**：Spring 会自动发现应用上下文中所创建的 bean
- **自动装配（autowiring）**：Spring 自动满足 bean 之间的依赖

以 CD 机为例。CD 播放器需要插入（注入）CD 才能进行播放。在 Java 中定义 CD 这个概念：

```java
package soundsystem;

public interface CompactDisc {
    void play();
}
```

将 CD 定义为接口，定义了 CD 播放机对 CD 能进行的操作，将 CD 播放器的实现和 CD 间的耦合降到了最低。

CD 的具体实现：

```java
package soundsystem;

@Component     // 通过注解将类声明为组件
public class SgtPeppers implements CompactDisc {
    private String title = "Sgt. Pepper's Lonely Hearts Club Band";
    private String artist = "The Beatles";

    @Override
    public void play() {
        System.out.println("Playing " + title + " by" + artist);
    }
}
```

**启用组件扫描**

Spring 默认是不会扫描组件的，需要在配置类中将其启用：

```java
package soundsystem;

@Configuration		    // 声明为配置类
@ComponentScan          // 启用组件扫描
public class CDPlayerConfig {}
```

如果用 xml 的方式启用组件扫描的话：

```xml
<context:component-scan base-package="soundsystem" />
```

**为扫描的 bean 命名**

Spring 应用上下文中所有的 bean 都会有一个给定的 ID。如果我们不显示指定的话，它会将“类名的首字母小写”后的名称作为 bean 的 ID。

想要指定 ID 的话：

```java
@Component("lonelyHeartsClub")    // 声明该类作为组件类 , 告诉 spring 要为这个类创建 bean, 通过括号参数指定 bean id
public class SgtPeppers implements CompactDisc {
```

**指定组件扫描的包**

默认规则下组件扫描会以配置类所在的包作为基础包来扫描组件。如果需要将配置类放在单独的包中就需要指定组件扫描的规则了：

```java
@Configuration
@ComponentScan("soundsystem")
```

**通过为 bean 添加注解实现自动装配**

```java
public interface MediaPlayer {
    void play();     // 定义 CD 播放机接口
}
```

实现具体的 CD 播放机，并使用 @Autowired 注解实现自动装配：

```java
public class CDPlayer implements MediaPlayer {
    private CompactDisc cd;
    
	@Autowired     // Autowired 注解进行自动装配
    public CDPlayer(CompactDisc cd) {
        this.cd = cd;
    }
    @Override
    public void play() {
        cd.play();
    }
}
```

在 Spring 创建 CDPlayer bean 的时候，会通过构造器实例化并传入一个可设置为 CompactDisc 的 bean。除了用在构造器上，@Autowired 注解还能用在 setter 方法上：

```java
@Autowired
public void setCd(CompactDisc compactDisc) {
    this.cd = compactDisc;
}
```

在 Spring 初始化 bean 之后，它会尽可能的满足 bean 的依赖，依赖是通过 @Autowired 的注解来声明的。

注：@Autowired 可以和 @Inject 互换。

#### 2.1.2  使用 Java 进行装配

让我们重新开始。

```java
package soundsystem;

@Configuration		    // 声明为配置类
public class CDPlayerConfig {}
```

我们去掉了 @ComponentScan 注解，换用 Java 的显式装配。

**声明简单地 bean**

在 JavaConfig 中声明 Bean：

```java
@Bean(name="lonelyHeartsClubBand")   // 注册为 Bean，并命名
public CompactDisc sgtPeppers() {
    return new SgtPeppers();
}
```

**利用 JavaConfig 实现注入**

当需要依赖其他 bean 的时候可以用 JavaConfig 实现依赖注入：

```java
@Bean
public CDPlayer cdPlayer() {
    return new CDPlayer(sgtPeppers());
}
```

更好的方式是选择传入 compactDisc 参数：

```java
@Bean
public CDPlayer cdPlayer(CompactDisc compactDisc) {
    return new CDPlayer(compactDisc);
}
```

#### 2.1.3 使用 XML 进行装配

使用 XML 声明 bean 时类似利用 Java 配置，需要用到 `<bean>` 元素：

```xml
<bean id="compactDisc" class="soudsystem.SgtPeppers" />
```

**使用构造器注入**

XML 为构造器注入提供了两种方式：

- `<constructor-arg>` 元素
- Spring3.0 引入的 c- 命名空间

**使用 constructor-arg 元素装配**

```xml
<bean id="cdPlayer" class="soundsystem.CDPlayer"
      <constructor-arg ref="compactDisc" />
</bean?
```

当 Spring 遇到这个 bean 元素时，它会创建一个 CDPlayer 实例。constructor-arg 元素告知 Spring 要为 ID 为 compactDisc 的 bean 引用传递到 CDPlayer 的构造器中。

**使用 c- 命名空间装配**

```xml
<bean id="cdPlayer" class="soundsystem.CDPlayer"
      c:cd-ref="compactDisc" />
```

属性以 "c:" 开头，为命名空间的前缀。之后的 "cd" 是构造器的参数名，"-ref" 则是一种约定，告诉 Spring 正在装配一个 bean 的引用。

上述命名方式需要引用构造器的参数名称，如果名称一旦修改，会造成不便。除了此种命名方式，我们还可以利用参数的位置信息命名：

```xml
<bean id = "cdPlayer" class="soundsystem.CDPlayer"
      c:_0-ref="compactDisc" />
```

**装配字面量**

```java
package soundsystem;

@Component 
public class BlankDisc implements CompactDisc {
    private String title;
    private String artist;

    public BlankDisc(String title, String artist) {
        this.title = title;
        this.artist = artist;
    }
}
```

对于上述实现如何装配硬编码的唱片标题和艺术家名称呢？

```xml
<bean id = "compactDisc" class="soundsystem.BlankDisc">
    <constructor-arg value="Some Strings" />
    <constructor-arg value="other strings" />
</bean>
```

使用 c- 命名空间：

```xml
<bean id = "compactDisc" class="soundsystem.BlankDisc"
    c:_title="Some Strings"
    c:_artist="other strings" />
```

`c:_title`、`c_artist` 同样可以用 `c:_0` 和 `c_1` 来替换。

##### 设置属性

依赖注入除了使用构造器注入之外还可以使用 setter 方法注入。对于**可选性的依赖**，更应该选择使用 setter 方法注入的形式。

```java
public class CDPlayer implements MediaPlayer {
    private CompactDisc compactDisc;
    
	@Autowired     // Autowired 注解进行自动装配
    public void setCompactDisc(CompactDisc compactDisc) {
        this.compactDisc = compactDisc;
    }
    @Override
    public void play() {
        compactDisc.play();
    }
}
```

上述 Java 代码中并没有用到构造器，而是使用了 setter 方法进行依赖注入。使用 XML 进行注入：

```xml
<bean id="cdPlayer" class="soundsystem.CDPlayer">
    <property name="compactDisc" ref="compactDisc" />
</bean>
```

property 元素为属性的 setter 方法提供的功能和 constructor-arg 元素为构造器提供的功能是一样的。

与 c- 命名空间类似，Spring 提供了 p- 命名空间作为 property 元素的替代方案：

```xml
<bean id="cdPlayer" class"soundsystem.CDPlayer"
      p:compactDisc-ref="compactDisc" />
```

**装配字面量**

借助 `<property>` 元素的 value 属性可以装配字面量：

```xml
<property name="artist" value="The Beatles" />
<property name="tracks">
    <list>
        <value> Sgt. Pepper's Lonely Hearts Club Band </value>
        <value>Another track.</value>
    </list>
</property>
```

### 2. 2. 高级装配



### 2. 3. Bean 的作用域

默认情况下 Spring 应用上下文中所有的 Bean 都是以单例的形式创建的，也就是说不管一个 Bean 被注入多少次，每次注入的都是同一个实例。

但有时候这种行为不符合我们的要求，我们可以自定义 Bean 的作用域：

- 单例（Singleton）：在整个应用中只有一个 Bean 的实例
- 原型（Prototype）：每次注入或者通过 Spring 应用上下文获取时都会创建一个新的 Bean 实例
- 会话（Session）：在 Web 应用中，为每个会话创建一个 Bean 实例
- 请求（Request）：在 Web应用中，为每个请求创建一个Bean实例。

为了指定我们要选择的作用域，需要用到@Scope注解：

```java
@Component
@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)
public class Test{}
```

xml方式：

```xml
<bean id="test" class="Test" scope="prototype" />
```

## 3. AOP

AOP 即 Aspect Oriented Programming，面向切面编程。

### 3.1 AOP 术语

**通知（Advice）**

切面的工作被称为通知。通知定义了切面是什么以及何时使用。除了描述切面要完成的工作之外，通知还解决了何时执行这个工作的问题。

Spring 内置了五种类型的通知：

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
- 类加载期：切面在目标类加载到 JVM 时被织入，需要特殊的类加载器
- 运行期：Spring AOP 就是以这种方式织入切面的

### 3.2 切点

- **arg()**：限制连接点匹配参数为指定类型的执行方法
- **@args()**：限制连接点匹配参数由指定注解的执行方法
- **execution()**：用于匹配是连接点的执行方法
- **this()**：限制连接点匹配 AOP 代理的 bean 引用为指定类型的类
- **target**：限制连接点匹配目标对象为指定类型的类
- **@target()**：限制连接点匹配特定的执行对象，这些对象对应的类要具有指定类型的注解

#### 3.2.1 编写切点

假设这样一个场景：正在开一场音乐会，开始前人们要关闭手机，保持安静；而后演出进行，观众鼓掌；若演出砸了，观众要求退票。首先定义一个表演接口：

```java
public interface Performance {
    public void perform();
}
```

从演出的角度来看，观众很重要。但对于演出本身的功能而言，它并不是核心。它是一个独立的关注点，因此，观众作为一个切面。

```java
@Aspect    // 声明切面
public class Audience {

    // 声明切点，execution 是切点表达式
    @Before("execution(* concert.Perfermance.perform(..))")  
    public void silenceCellPhones() {
        System.out.println("Silencing cell phone");   // perform 执行前执行此方法
    }

    @Before("execution(* concert.Perfermance.perform(..))")
    public void takeSeats() {
        System.out.println("Taking seats");
    }

    @AfterReturning("execution(* concert.Perfermance.perform(..))")
    public void applause() {
        System.out.println("CLAP CLAP CLAP!!!");
    }

    @AfterThrowing
    public void demandRefund() {
        System.out.println("Demanding a refund");
    }
}
```

execution() 表示在方法执行时触发，括号内的星号表示返回值类型为任意值。星号之后为类的全限定名+方法名。最后一个括号和其中的两个点表示使用任意参数。

切点表达式中有大量重复，我们可以利用 @Pointcut 注解来解决这个问题：

```java
@Aspect
public class Audience {

    @Pointcut("execution(* concert.Perfermance.perform(..))")
    public void performance() {}

    @Before("performance()")
    public void silenceCellPhones() {
        System.out.println("Silencing cell phone");
    }

    @Before("performance()")
    public void takeSeats() {
        System.out.println("Taking seats");
    }

    @AfterReturning("performance()")
    public void applause() {
        System.out.println("CLAP CLAP CLAP!!!");
    }

    @AfterThrowing("performance()")
    public void demandRefund() {
        System.out.println("Demanding a refund");
    }
}
```

#### 3.2.2 启用自动切面代理

如果我们只是在普通的 POJO 上加了 @Aspect 注解的话，它仍就只会是一个普通的 bean，不会被视为切面。为了让 Spring 启用这个切面，需要进行自动代理配置：

```java
@Configuration
@EnableAspectJAutoProxy			// 启用自动代理
@ComponentScan
public class ConcertConfig {

    @Bean
    public Audience audience() {
        return new Audience();
    }
}
```

使用 XML 方式：

```xml
<aop:aspectj-autoproxy />
```

#### 3.2.3 环绕通知

环绕通知是最为强大的通知类型，它能够将被通知的目标方法完全包装起来，相当于同时编写前置通知和后置通知。

```java
@Aspect
public class Audience {
    @Pointcut("execution(* concert.Perfermance.perform(..))")
    public void performance() {}
    
    @Around("performance()")    // 创建环绕通知
    public void watchPerformance(ProceedingJoinPoint jp) {
        try {
            System.out.println("Silencing cell phones");
            System.out.println("Taking seats");
            jp.proceed();
            System.out.println("CLAP CLAP CLAP!!!");
        } catch (Throwable e) {
            System.out.println("Demanding a refund");
        }
    }
}
```

#### 3.2.4 通知中的参数

```java
@Pointcut (
	"execution (* soundsystem.CompactDisc.playTrack(int))" + "&& args(trackNumber)"
)
```

#### 3.2.5 引入新的功能

利用 AOP 还能完成类似 Ruby 中开放类的功能，即为一个类动态的引入本来并不存在的方法，看起来好像那个类本身就有这些方法。

![](http://on-img.com/chart_image/5b434242e4b09a67416194bc.png?_=1531134739591)



#### 8. 通过 XML 配置切面

| AOP 配置元素              | 用途                                                     |
| ------------------------- | -------------------------------------------------------- |
| `<aop:advisor>`           | 定义 AOP 通知                                            |
| `<aop:after>`             | 定义 AOP 后置通知（不管执行是否成功）                    |
| `<aop:after-returning>`   | 定义 AOP 返回通知                                        |
| `<aop:after-throwing>`    | 定义 AOP 异常通知                                        |
| `<aop:around>`            | 定义 AOP 环绕通知                                        |
| `<aop:aspect>`            | 定义一个切面                                             |
| `<aop:aspectj-autoproxy>` | 启用 @AspectJ 注解驱动的切面                             |
| `<aop:before>`            | 定义一个 AOP 前置通知                                    |
| `<aop:config>`            | 顶层的 AOP 配置元素，大多数的 `<aop:*>` 元素必须包含在内 |
| `<aop:declare-parents>`   | 以透明的方式为被通知的对象引入额外的接口                 |
| `<aop:pointcut>`          | 定义一个切点                                             |





