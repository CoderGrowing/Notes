## Ruby

#### 简介

- 日本的松本行弘于 1993 年发明
- 动态类型
- 纯面向对象

#### 输出

主要有下面几个用于输出的方法：

- print：类似于 C 中的 pringf，转义，输出
- puts：类似于 Java 中的 println，转义，加换行，输出
- p：不转义，原样输出，用于调试
- pp：更美观的输出

此外，Ruby 对单引号和双引号有不同的解释。单引号直接输出，双引号可以完成替换。
```ruby
puts 'hello, world!'    
# hello, world

language = 'ruby'
puts "hello, #{language}"
# hello, ruby
```

输出有多个参数时，直接用逗号隔开即可：

```ruby
print " 参数 1", " 参数 2"
```

**中文**

Ruby 默认编码格式为 UTF-8，通常可以正常解释中文。如果中文出错的话，可以利用类似 Python 中的注释：

```ruby
# encoding: GBK
```

**注释**

用 # 表示注释的开始，多行注释使用 `=begin` 开始，`=end` 表示结束。

#### 变量

**声明**

Ruby 中较为特殊的是对于不同作用域的变量声明方式不同。

- 局部变量：以英文小写字母或下划线开头
- 全局变量：以 $ 开头
- 实例变量：以 @ 开头
- 类变量：以 @@ 开头

**赋值**

赋值中值得一提的是 Ruby 支持类似 Python 中的多重赋值，即下面这种形式：

```ruby
a, b, c = 1, 2, 3
a, b = b, a
arr = [1, 2]
a, b = arr    # 解包
```

#### 条件控制

##### true 和 false

- 除了 nil 和 false，其余的均为 true
- true 和 false 均是一等对象
- &&(and)、||(or)、均是短路求值，如果不想要短路求值，换用 & 和 |

##### if/then/else/unless

- if 条件 then 执行，then 可以省略
- if/unless 既可以多行写成块形式，也可以单行
- unless 表达的是 not 或者！的意思

```ruby
if x == 4
    puts "x=4"
end

puts "x=4" if x == 4
puts "x==4" unless x == 4
```

##### 循环

**for**

```ruby
for i in 1..5   # ruby 会自动构建 Range 对象
    puts "Hello"
end
```

**while**

while 也可用于单行 / 多行形式。

```ruby
i = 1
while i < 10
    puts i
    i = i + 1
end
```

**times**

当循环次数确定时可以用 times 方法：

```ruby
9.times do
    puts i
end
```

**until**

```ruby
sum = 0
until sum >= 10
    sum += 1
    puts "Hello"
end
```

**each**

each 用于遍历可迭代的对象。

```ruby
a = 1..5
a.each do |i|
    puts i
end

# 等价于
a.each {|i| puts i}
```

**loop**

用于无限循环

```ruby
loop do
    print "ruby"
end
```

#### 数据结构

```ruby
1.class
# Integer

(0.1).class
# Float
```

##### 数组

- 用中括号括起来 arr = [1, 2, 3]
- 下标访问 , arr[0], arr[-1]
- 自动构建 Range 对象，arr[0..1]
- arr.push
- arr.pop

##### 字符串

- **to_s** converts values to **s**trings.
- **to_i** converts values to **i**ntegers (numbers.)
- **to_a** converts values to **a**rrays.

##### 符号 (symbol)

符号类似于字符串，一般作为名称标签使用。创建符号只需要在标识符前加上冒号就行了：

```ruby
sym = :foo
```

##### 散列表

创建散列表：

```ruby
number = {one => 'one', two => 'two'}
```

Ruby 中经常使用符号作为键，当符号作为键时可以使用简略的写法：

```ruby
number = {one: 'one', two: 'two'}
```

#### 函数

**定义函数**

**参数个数不确定**

```ruby
def foo(*args)
    args
end
p foo(1, 2, 3)
# [1, 2, 3]
```

**关键字参数**

```ruby
def area2(x: 0, y: 0)
    puts x * y
end

area2(x: 1, y: 2)

# 或者
def area2(x=0, y=0)
    puts x*y
end
area2(x=1, y=2)
```







#### 正则表达式



#### 编码习惯

- 类：驼峰式命名法，CamelClass
- 实例变量：必须加 @ 前缀，下划线命名
- 类变量：必须加 @@ 前缀，下划线命名
- 方法：下划线命名

#### 常用方法

##### 数值运算

```ruby
x.div(y)     # 返回 x 除以 y 之后商的整数，同 /
x.quo(y)     # 返回 x 除以 y 以后的商，如果 x 和 y 都是整数，返回 Rational 对象 (5/2)
x.modulo(y)  # 同 x % y
```

数学函数需要在前面加上 Math. 使用。

```ruby
Math.sin(10)
Math.sqrt(100)   # 10
```

##### 随机数

```ruby
Random.rand			# 返回 0 到 1 之间的随机小数
Random.rand(3)       # 返回 0 到 3 之间的整数
```

##### 命令行参数

使用 `ARGV` 这个 Ruby 内置的数组来获取命令行传递来的参数。

```ruby
puts " 首个参数：#{ARGV[0]}"
puts " 第二个参数：#{ARGV[1]}"
```



##### 文件读写

读取文件：

```ruby
filename = ARGV[0]
file = File.open(filename)  # 打开文件
text = file.read      	    # 获取文件内所有内容
# text = File.read(filename)  等同于上两行内容

file.each_line do |line|    # 逐行读取 
    print line
end
file.close
```

#### 模块

模块是 Ruby 的特色功能，经常利用模块来实现混入（Mix-in）扩展功能。

```ruby
module MyModule
    # some methods
end

class TestModule
    include MyModule   # 可以使用 MyModule 中的方法
end
```

模块中的方法可以在模块中和包含模块的类中直接使用，但如果想要使用 " 模块名 . 方法名 " 来调用时，需要用到 `module_function` 方法：

```ruby
module_function :hello
```

#### 面向对象

##### 类

```ruby
class SomeClass
    # some exp
end

test = SomeClass.new
```

**initialize 方法**

在使用 new 新建对象时 initialize 方法会被调用，类似于 Python 中的 `__init__`。

**self**

在实例方法中，可以使用 self 这个特殊的变量来引用方法的接收者。

```ruby
class HelloWorld
    attr_accessor :name
    def greet
        puts "Hi, I am #{self.name}"
    end
end
```

通常情况下 self 为默认的接收者，可以省略。但当使用类似 name= 这样的以 = 结束的方法时需要显式使用 self 调用。

**类方法**

```ruby

```

##### 属性读写器

类似于 Java 中的 private 变量，Ruby 不允许在类以外访问实例变量。所以很多情况下我们需要提供 getter 和 setter 方法：

```ruby
# setter，和属性同名加上一个等号
def name=(new_value)
    @name = new_value
end

# getter，和属性同名
def name
    @name
end
```

这样书写方法实在很麻烦，所以 Ruby 提供了一个简便的方法：
- attr_writer :name    写（setter）方法
- attr_reader :name   读（getter）方法
- attr_accessor :name 读写方法

这三个方法都可以同时有多个参数，指定多个需要定义存取方法的属性。

#### 异常处理

##### 抛出异常

```ruby
raise ExceptionName, "message"
```
##### 处理异常

Ruby 使用 begin-rescue-ensure-end 语句来描述异常处理。

```ruby
begin
    # 可能发生异常的语句
rescue => 变量
    # 发生异常后的处理
ensure
    # 不管是否发生异常都进行的处理
end
```

发生异常时，ruby 会自动将异常信息赋值给两个变量：

- `$!`：最后发生的异常（异常对象）
- `$@`：最后发生异常的位置信息

同时可以通过调用相应的方法得到相关的异常信息：

- `class`：异常的种类
- `message`：异常信息
- `backtrace`：异常发生的位置信息（`$@` 等同于 `$!.backtrace`



#### 关键字

- `BEGIN`
- `END `
- `__FILE__`
- `__LINE__`
- `__ENCODING__`
- `case `
- `break`：跳出循环
- `and`：同 &&
- `begin`：约等于 try，开始有可能抛出异常的语句
- `do`
- `else `：分支
- `alias`：为已有方法设置别名
- `def`：定义函数
- `defined?`
- `cass`：类似 C 中的 switch
- `false`：False
- `for `：循环
- `elsif`：分支
- `end`：结束分支条件 / 循环
- `ensure`：约等于 finally，不管是否发生异常都会进行的操作
- `in`
- `module`：定义模块
- `next`：类似于 continue
- `nil `
- `redo`：在相同的条件下重复刚才的处理
- `rescue`
- `retry `
- `or`
- `then`
- `true `：True
- `return`：返回
- `self`
- `super`
- `until`：循环
- `while `：循环
- `when`：类似 C 中的 case，与 Ruby 中的 case 一块使用
- `undef`：删除已经定义的方法
- `unless`：用于条件控制，同 if not
- `yield`：用于定义块方法，在 yield 处产出值