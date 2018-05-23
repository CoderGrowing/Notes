## Gradle

#### 开始

Gradle构建脚本的默认名字是build.gradle

**插件**

```groovy
apply plugin 'java'
```

约定代码位置为src/main/java目录。

**仓库**

仓库是可以找到依赖jar文件的文件系统或者中心服务器。Gradle要求至少定义一个仓库来使用依赖：

```groovy
repositories {
    mavenCentral() 
}
```

**依赖**

