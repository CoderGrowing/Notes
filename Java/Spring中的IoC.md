## Spring中的IoC

IoC即Inversion of Control，中文译作“控制反转”，也叫作依赖注入（Dependency Injection）。

既然叫做“控制反转”，那么是反转了什么呢？其实反转的就是依赖对象的创建方式。正常情况下我们自己回去利用`new`关键字新建对象。但在IoC的设计理念下，这个新建过程转交给了Spring的容器，即我们需要对象时，只需通知容器一下即可获得我们所需的对象，而具体的新建过程由容器操控。

那这个“通知容器”的动作是怎么实现的呢？有三种依赖注入的方式，即构造方法注入（constructor
injection）、setter方法注入（setter injection）以及接口注入（interface injection）。

