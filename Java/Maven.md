## Maven

### 1. 安装配置

下载zip包后，解压至想要安装的文件夹。

新建环境变量`M2_HOME`,值为maven解压后的路径，如C:\Program Files\apache-maven-3.5.3。

在Path中新增一条，值为`%M2_HOME%\bin;`，而后在命令行输入`mvn -v `即可看到maven输出版本信息啦。

#### 1.1 安装目录分析

- bin：包含了mvn运行的脚本
- boot：只包含一个文件，是一个类加载器框架，maven使用该框架加载记得类库
- conf：包含了settings.xml，是maven的全局配置
- lib：包含了maven运行时需要的各种Java类库

#### 1.2 ~/.m2

用户目录下的.m2文件夹下存放的是maven本地的仓库。可以将主目录下conf/settings.xml复制一份到~/.m2目录下，如此该配置文件就只对当前用户生效。

### 2. 使用

#### 2.0 使用archetype生成项目骨架

mvn指定了文件目录结构，使用`mvn archetype:generate`即可生成项目的骨架。

#### 2.1 pom.xml配置

maven的核心是pom.xml，POM（Project Object Model，项目对象模型）定义了项目的基本信息，用于描述项目如何被构建，声明项目依赖等。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.learnmaven</groupId>
    <artifactId>chapter3</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <name>Learn Maven Project</name>
</project>
```

第一行是XML头，指定了xml的版本和编码方式。

然后是project元素，project元素是pom.xml的根元素。根元素下的modelVersion指定了当前POM模型的版本，对于maven2和maven3来说，它只能是4.0.0。

groupId元素定义了项目属于哪个组，这个往往与项目所在的组织和公司有关，类似于包名。

artifactId定义了当前maven项目在组中的唯一ID。

version定义了版本，SNAPSHOT意为快照，表示项目还在开发中。

```xml
<dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>4.0.5</version>
        </dependency>
</dependencies>
```

dependencies元素下可以包含多个依赖，这里我们添加了spring-boot依赖。依赖使用groupId、artifactId和version来指定。有了这段声明，maven就可以自动下载依赖。

dependency元素下还可以指定scope元素，默认为compile，即该依赖对测试和主代码都有效，若scope的值为test，则只对测试有效，在主代码中import依赖会报错。

#### 2.2 常用命令

- mvn clean compile：编译主代码
- mvn clean test：执行测试
- mvn clean package：将项目打包，默认格式为jar，可通过package属性修改
- mvn clean install：将打包好的项目安装到本地仓库，如此就可以在其他项目中使用

默认打包生成的jar是无法直接运行的，因为带有main方法的类信息不会添加到manifest中去。为了生成可执行的jar文件，需要借助maven-shade-plugin：

```xml
<build>
    <pulgins>
        <plugin>  
        <groupId>org.apache.maven.plugins</groupId>  
          <artifactId>maven-shade-plugin</artifactId>  
          <version>1.2.1</version>  
          <executions>  
            <execution>  
              <phase>package</phase>  
              <goals>  
                <goal>shade</goal>  
              </goals>  
              <configuration>  
                <transformers>  
                  <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">            <mainClass>com.learnmvn.youmainclass</mainClass>  
                 </transformer>  
               </transformers>  
             </configuration>  
             </execution>  
          </executions>  
        </plugin>  
    </pulgins>
</build>
```

如此配置之后，再次执行mvn clean install生成的jar包即可直接运行。

### 3. 坐标和依赖详解

#### 3.1 坐标

maven坐标为各种构件引入了秩序，任何一个构件都必须明确定义自己的坐标。共有下面几个坐标元素：

- groupId：定义当前maven项目隶属的实际项目
- artifactId：定义实际项目中的一个maven模块，推荐使用实际项目的名称作为artifactId的前缀
- version：定义版本号
- packaging：定义打包方式，默认为jar
- classifier：用来帮助定义构建输出的一些附属构件，不能直接定义，由附加的插件帮忙生成

#### 3.2 依赖配置

- groupId、artifactId、version：定义依赖的基本坐标
- type：依赖的类型，对应于项目坐标中的packageing
- scope：依赖的范围：
  - compile：编译依赖范围，默认值，对编译、测试、运行都有效
  - test：测试依赖范围，只对测试有效
  - provided：已提供依赖范围，对于编译和测试有效，运行无效，典型的如servlet-api
  - runtime：运行时依赖
  - system：系统依赖范围
- optional：标记依赖是否可选
- exclusions：用来排除传递性依赖