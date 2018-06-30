## Gradle

#### 开始

Gradle 构建脚本的默认名字是 build.gradle

**插件**

```groovy
apply plugin 'java'
```

约定代码位置为 src/main/java 目录。

**仓库**

仓库是可以找到依赖 jar 文件的文件系统或者中心服务器。Gradle 要求至少定义一个仓库来使用依赖：

```groovy
repositories {
    mavenCentral() 
}
```

**依赖**

