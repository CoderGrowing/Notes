## 装配Bean

不同于重量级的EJB（企业级JavaBean，Enterprise JavaBean），Spring是基于POJO（Plain Ordinary Java Object，简单Java对象）的。

Spring通过配置文件或注解来描述类和类之间的依赖关系，**自动完成类的初始化和依赖注入工作**。

```xml
<bean id="quest" class="SomeQuest" />
<bean id="knight" class="BraveKnight"
      p:quest-ref="quest" />
```

通过XML的配置，我们告知了Spring类之间的依赖关系，创建对象之间协作关系的行为叫做**装配（wiring）**，这也是依赖注入的本质。如此Spring便可以通过解析XML文件来完成类之间的依赖的自动装配。

Spring提供了两种注入依赖的配置供我们使用，即基于注解的配置和基于XML的配置。而依赖注入的方式有三种，分别是**构造方法注入**（constructor injection）、**setter方法注入**（setter injection）以及**接口注入**（interface injection）。对于这三种方式我们分别来看下如何使用Spring来进行依赖注入。

### 1. 可选的装配方案

Spring主要提供了三种装配机制：

- 隐式的bean自动发现和自动装配机制
- 显式的利用Java进行配置
- 显式的利用XML进行配置

推荐尽可能的使用自动装配机制，必须要显示配置时，尽量采用Java配置的方式。

#### 1.1 自动化装配

Spring从两个角度实现自动化装配：

- **组件扫描（component scanning）**：Spring会自动发现应用上下文中所创建的bean
- **自动装配（autowiring）**：Spring自动满足bean之间的依赖

以CD机为例。CD播放器需要插入（注入）CD才能进行播放。在Java中定义CD这个概念：

```java
package soundsystem;

public interface CompactDisc {
    void play();
}
```

将CD定义为接口，定义了CD播放机对CD能进行的操作，将CD播放器的实现和CD间的耦合降到了最低。

CD的具体实现

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

##### 启用组件扫描

Spring默认是不会扫描组件的，需要在配置类中将其启用：

```java
package soundsystem;

@Configuration		    // 声明为配置类
@ComponentScan          // 启用组件扫描
public class CDPlayerConfig {}
```

如果用xml的方式启用组件扫描的话：

```xml
<context:component-scan base-package="soundsystem" />
```

##### 为扫描的bean命名

Spring应用上下文中所有的bean都会有一个给定的ID。如果我们不显示指定的话，它会将“类名的首字母小写”后的名称作为bean的ID。

想要指定ID的话：

```java
@Component("lonelyHeartsClub")    // 声明该类作为组件类,告诉spring要为这个类创建bean,通过括号参数指定bean id
public class SgtPeppers implements CompactDisc {
```

##### 指定组件扫描的包

默认规则下组件扫描会以配置类所在的包作为基础包来扫描组件。如果需要将配置类放在单独的包中就需要指定组件扫描的规则了：

```java
@Configuration
@ComponentScan("soundsystem")
```

##### 通过为bean添加注解实现自动装配

```java
public interface MediaPlayer {
    void play();     // 定义CD播放机接口
}
```

实现具体的CD播放机，并使用@Autowired注解实现自动装配：

```java
public class CDPlayer implements MediaPlayer {
    private CompactDisc cd;
    
	@Autowired     // Autowired注解进行自动装配
    public CDPlayer(CompactDisc cd) {
        this.cd = cd;
    }
    @Override
    public void play() {
        cd.play();
    }
}
```

在Spring创建CDPlayer bean的时候，会通过构造器实例化并传入一个可设置为CompactDisc的bean。除了用在构造器上，@Autowired注解还能用在setter方法上：

```java
@Autowired
public void setCd(CompactDisc compactDisc) {
    this.cd = compactDisc;
}
```

在Spring初始化bean之后，它会尽可能的满足bean的依赖，依赖是通过@Autowired的注解来声明的。

注：@Autowired可以和@Inject互换。

#### 1.2  使用Java进行装配

让我们重新开始。

```java
package soundsystem;

@Configuration		    // 声明为配置类
public class CDPlayerConfig {}
```

我们去掉了@ComponentScan注解，换用Java的显式装配。

##### 声明简单地bean

在JavaConfig中声明Bean：

```java
@Bean(name="lonelyHeartsClubBand")   //注册为Bean，并命名
public CompactDisc sgtPeppers() {
    return new SgtPeppers();
}
```

##### 利用JavaConfig实现注入

当需要依赖其他bean的时候可以用JavaConfig实现依赖注入：

```java
@Bean
public CDPlayer cdPlayer() {
    return new CDPlayer(sgtPeppers());
}
```

更好的方式是选择传入compactDisc参数：

```java
@Bean
public CDPlayer cdPlayer(CompactDisc compactDisc) {
    return new CDPlayer(compactDisc);
}
```

#### 1.3 使用XML进行装配

使用XML声明bean时类似利用Java配置，需要用到`<bean>`元素：

```xml
<bean id="compactDisc" class="soudsystem.SgtPeppers" />
```

##### 使用构造器注入

XML为构造器注入提供了两种方式：

- `<constructor-arg>`元素
- Spring3.0引入的c-命名空间

**使用constructor-arg元素装配**

```xml
<bean id="cdPlayer" class="soundsystem.CDPlayer"
      <constructor-arg ref="compactDisc" />
</bean?
```

当Spring遇到这个bean元素时，它会创建一个CDPlayer实例。constructor-arg元素告知Spring要为ID为compactDisc的bean引用传递到CDPlayer的构造器中。

**使用c-命名空间装配**

```xml
<bean id="cdPlayer" class="soundsystem.CDPlayer"
      c:cd-ref="compactDisc" />
```

属性以"c:"开头，为命名空间的前缀。之后的"cd"是构造器的参数名，"-ref"则是一种约定，告诉Spring正在装配一个bean的引用。

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

使用c-命名空间：

```xml
<bean id = "compactDisc" class="soundsystem.BlankDisc"
    c:_title="Some Strings"
    c:_artist="other strings" />
```

`c:_title`、`c_artist`同样可以用`c:_0`和`c_1`来替换。

##### 设置属性

依赖注入除了使用构造器注入之外还可以使用setter方法注入。对于可选性的依赖，更应该选择使用setter方法注入的形式。

```java
public class CDPlayer implements MediaPlayer {
    private CompactDisc compactDisc;
    
	@Autowired     // Autowired注解进行自动装配
    public void setCompactDisc(CompactDisc compactDisc) {
        this.compactDisc = compactDisc;
    }
    @Override
    public void play() {
        compactDisc.play();
    }
}
```

上述Java代码中并没有用到构造器，而是使用了setter方法进行依赖注入。使用XML进行注入：

```xml
<bean id="cdPlayer" class="soundsystem.CDPlayer">
    <property name="compactDisc" ref="compactDisc" />
</bean>
```

property元素为属性的setter方法提供的功能和constructor-arg元素为构造器提供的功能是一样的。

与c-命名空间类似，Spring提供了p-命名空间作为property元素的替代方案：

```xml
<bean id="cdPlayer" class"soundsystem.CDPlayer"
      p:compactDisc-ref="compactDisc" />
```

**装配字面量**

借助`<property>`元素的value属性可以装配字面量：

```xml
<property name="artist" value="The Beatles" />
<property name="tracks">
    <list>
        <value> Sgt. Pepper's Lonely Hearts Club Band </value>
        <value>Another track.</value>
    </list>
</property>
```

### 2. 高级装配

### 3. Bean的作用域

默认情况下的