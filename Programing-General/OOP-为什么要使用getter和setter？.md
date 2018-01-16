# OOP-为什么要使用getter和setter？

```java
public class Demo {
    private int x;
    private int y;
    
    public getX() {
        return x;
    }
    public getY() {
        return y;
    }
    
    public setX(int x) {
    	this.x = x;
    }
    public setY(int y) {
        this.y = y;
    }
}
```

为类的属性设置getter和setter方法，而不是直接访问有什么好处？

1. 允许以后向getter和setter方法中添加行为(如验证)
2. 可以保持外部接口不变的情况下，修改内部存储方式和逻辑。
3. 可以方便调试，打断点。
4. 允许子类更改对应的行为
5. …………………………

参考：

1. [getter和setter方法有什么用-知乎](https://www.zhihu.com/question/21401198)

2. [why-use-getters-and-setters-accessors---stackoverflow](https://stackoverflow.com/questions/1568091/why-use-getters-and-setters-accessors)

   ​