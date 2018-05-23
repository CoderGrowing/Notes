### Ruby元编程

### 1. 元这个字眼

如果把代码看成是一个世界，那么其中就充斥着各种成员（变量、类、方法等）。这些成员称为**语言构件**（language construct）。

类似C、C++这样的语言编译后在运行时很多语言构件只存在于内存中，看不见摸不着了。但对于Ruby这样的动态语言来说，运行时你仍然可以取得绝大多数语言构件的信息。这种在运行时取得构件信息的特性叫做**内省**（introspection）。

**元编程**就是利用内省的特性，来编写能在运行时操作语言构件的代码。

**动态元编程**是指在运行时操作自身的代码，而代码生成器和编译器生成代码的方式叫做**静态元编程**。

### 2. 对象模型

#### 2.1 开放类

Ruby中最让我惊叹的一个特性应该就是开放类的概念。那么什么是开放类呢？我们通过一个例子来看一下：

```ruby
class String
  def hello
      "Hello, #{self}."
  end
end

"Bob".hello  # Hello, Bob
```

我们可以直接修改Ruby的核心类String，为所有的字符串对象都添加上我们自定义的hello方法！再看一个例子：

```ruby
class Klass
  def x;  "x"  end
end

class Klass
  def y;  "y"  end
end
```

我们做了什么？难道可以定义两个同名的类？并不是这样的。我们来看一下上面的语句到底干了什么：

```ruby
obj = Klass.new
obj.x     # "x"
obj.y     # "y"
```

我们第一次使用class Klass时，Ruby会为我们定义这个类；而我们第二次使用这个语句时，Ruby就不会再次定义了。它只会重新“打开”这个类，并定义y方法。

在Ruby中，定义类的语句和其他语句没有本质区别。它更像是一个作用域操作符，而不是类声明语句。创建一个新的类，这个作用更像是一个“副作用”。Ruby中类的这个特性叫做**开放类**（open class）。

开放类我们提供了极大地方便，我们可以直接对核心类进行操作，提供我们想要的功能。但这也带来了一些问题。试想如果核心类中定义的方法被你覆盖了，整个Ruby系统都有可能因此而崩溃。所以定义核心类的时候一定要注意，**在为某个类定义新方法前应该仔细检查该类是否已经有同名的方法**。

**细化**

除了小心检查之外，Ruby还提供了另一种解决冲突的方法：细化。

首先，需要定义一个模块，再在这个模块中利用refine来定义为类添加的方法即可：

```ruby
module StringEdit
    refine String do
        def hello
            "hello"
        end
    end
end
```

需要使用添加的方法时，需要使用using方法：

```ruby
module UseEditString
    using StringEdit
    # do something
end
```

StringEdit的修改只在使用using方法的模块内有效。

#### 2.2 类和对象中有什么

让我们回忆一下类中可以定义什么：可以定义实例变量、实例方法、类方法和类变量。那么这些元素在哪里存储呢？

```ruby
class MyClass
  def my_method
      @v = 1
  end
end

obj = MyClass.new
```

我们为MyClass新建了一个obj对象，那么obj中存储了什么呢？首先它存储了自己的实例变量(@v，调用my_method后才会有)，然后它存储了对自身类的一个引用。至于my_method这个实例方法，并没有存储在obj中，而是存储在MyClass中。

**实例变量存储在对象中，而实例方法存储在类中**。

#### 2.3 类的真相

```ruby
"hello".class # String
String.class  # Class
```

String这个类也有自己的类！这就是类的真相：**类本身也是对象**。

在Ruby中，所有的类都是BasicObject类的子类，而所有的类都是Class类的对象。那么Class的超类是什么呢？

Module。是的，Class的超类是Module（模块），也就是说，其实每个类都是一个模块，只不过它比模块增加了三个方法（new、allocate和superclass）罢了。

那么什么时候用Module什么时候用Class呢？**当你希望自己的代码被包含（include）到别的代码中去的的时候就应该用模块，但你希望自己的代码被实例化或继承的时候，就使用类**。

#### 2.4 常量

任何以大写字母开头的引用（包括类名和模块名）都是常量。但Ruby中的常量其实更像变量，虽然当你试图修改常量值的时候会得到警告，但修改仍然可以完成。那么常量和变量的区别是什么呢？最大的区别在于作用域不同，常量有自己独特的作用域规则。

类似于文件路径，常量可以通过路径来标识：

```ruby
module M
    class C
        X = "a constant"
    end
    C::X
end
M::C::X
```

如果常量所在的位置较深，可以通过绝对路径来访问：

```ruby
Y = 'a root-level constant'
module M
    Y = 'a constant in M'
    Y     # 'a constant in M'
    ::Y   # 'a root-level constant'
end
```

#### 2.5 有关方法的内容

**方法查找顺序**

向右一步，再向上。

**执行方法**

```ruby
def my_method
    temp = @x + 1
    my_other_method(temp)
end
```

Ruby如何调用这个方法呢？首先，Ruby需要确定变量@x的归属，它属于哪个对象；其次，my_other_method()方法是属于哪个对象的？

Ruby中的每一行代码都会在一个对象中执行，这个对象就是当前对象（self）。如果没有显式指定调用者的话，Ruby就在self上调用。

**private**

私有方法遵守的规则：不能明确指定接受者来调用私有方法，即只能通过隐式的接收者self调用

### 3. 方法

#### 3.1 动态派发

我们通常会使用对象.方法的格式来调用方法，但还有其他的途径可以完成相同的功能：使用send方法：

```ruby
class Klass
    def method(arg)
        arg *2
    end
end

obj = Klass.new
obj.send(:my_method, 3)    # 6
```

在send方法里，想要调用的方法变成了参数，这样就可以在最后一刻来决定究竟调用哪个方法。这个技巧称为**动态派发（Dynamic Dispatch）**。

#### 3.2 动态定义

除了利用def关键字，我们还可以利用define_method方法来定义一个方法：

```ruby
class MyClas
    define_method :my_method do |arg|
        arg * 2
    end
end
```

#### 3.3 method_missing

当我们调用方法时，Ruby会按照一定的顺序来查找这个方法属于哪个类。如果最后在BasicObject中都没有找到这个方法的话，Ruby会在对象上调用一个method_missing的方法。

method_missing方法是BasicObject类的一个私有实例方法，所以任何对象都可用。当method_missing方法被调用时，编译器会抛出NoMethodError并打印相关的一些信息。

```ruby

```





