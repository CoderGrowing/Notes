# Java基础

#### 基本数据类型

int、float、double、char、byte和boolean

#### 输入数据

Java的输入输出真是我见过的编程语言中最复杂的╮(╯▽╰)╭

```java
import java.util.Scanner;

public class InputDemo {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.println("Please input a number: ");
        double in = input.nextDouble();
        System.out.println("The number is: " + in);
    }
}
```

#### 变量与初始化

