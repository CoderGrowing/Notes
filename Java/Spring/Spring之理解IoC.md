## Spring之理解IoC

IoC即Inversion of Control，中文译作“**控制反转**”，也叫作**依赖注入**（Dependency Injection）。

既然叫做“控制反转”，那么是反转了什么呢？其实反转的就是**依赖对象的创建方式**。正常情况下我们自己回去利用`new`关键字新建对象。但在IoC的设计理念下，这个新建过程转交给了Spring的容器，即我们需要对象时，只需通知容器一下即可获得我们所需的对象，而具体的新建过程由容器操控。

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

DamselRescuingKnight在构造函数中**自行创建**了RescueDamselQuest，它们两个紧紧地耦合在了一起。如此固然能够发挥作用，但也同样限制了骑士能做的事情。

为了解耦，我们将创建的过程交给其他类来处理，在构造函数中传入Quest即可：

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

不同于之前的DamselRescuingKnight，BraveKnight在构造时将探险任务作为参数传入，从而能够完成更多的任务。

```java
public class Dispatcher {
    public void dispatch() {
        // 指定探险任务
        Quest quest = new SomeQuest();
        
        //将探险任务注入
        BraveKnight knight = new BraveKnight(quest);
    }
}
```

但即便如此，探险任务的初始化仍需要我们来完成，只是这些工作转到了另一个类中去。那么可不可以有一个“第三方”的机构，帮助我们完成初始化和装配工作呢？Spring就扮演了这样的一个角色。

我们只需要提供给Spring类的信息，这样当我们需要时，Spring就可以创建类并交还给我们。由此，创建实例化类的工作由new的方式变成了Spring容器创建，实现了“控制反转”。

