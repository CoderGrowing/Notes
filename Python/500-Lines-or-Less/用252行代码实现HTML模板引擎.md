## 500lines or less: 实现一个 HTML 模板引擎

> 简介：500-lines-or-less 是一本开源的图书，共 22 章，每章都是由对应行业的大牛完成的。每章都实现了一个独立的系统，如 Web Server、OCR、3D Modeller 等等，而且代码行数均少于 500 行。
>
> 官网地址：[500-lines-or-less](http://aosabook.org/en/index.html)
>
> github 项目地址：[500lines](https://github.com/aosabook/500lines/)

本文是《500lines or less》第 21 章：A Template Engine 的笔记。

### 介绍

我们写的程序大多都是包含了很多逻辑结构和少部分的纯文本。比如我们使用 `def` 去定义函数，使用 `class` 去定义类，使用 `if-else` 控制分支流程等。这些都是为程序的逻辑服务的。而像 `print` 这种语句则是为纯文本服务。而有些程序则相反，它由大多数的纯文本和少部分的逻辑结构组成。我们今天要说的模板引擎就是这样的程序。

我在学习模板之前曾经有一个疑惑：一个网站成千上万的网页难道都需要手写 HTML 代码来实现么？那岂不是很麻烦。后来学习了 Flask，Flask 的模板引擎 Jinjia2 给了我答案：网页都是模板渲染出来的！你只需要定义页面的架构和数据，模板会帮你渲染成统一风格的 HTML 页面。

那么我们该如何用 Python 实现这样的功能呢？首先想到的当然是替换，将模板中的变量替换为自定义的数据即可。

比如现在有这么一段 HTML 代码：

```html
<p>Welcome, Charlie!</p>
<p>Products:</p>
<ul>
    <li>Apple: $1.00</li>
    <li>Fig: $1.50</li>
    <li>Pomegranate: $3.25</li>
</ul>
```

我们可以很轻易的区分哪些是固定内容哪些是需要动态生成的内容：**用户名是变化的，货物和价格是变化的，其他都是固定的**。那么我们可以定义下面的结构来完成这件工作：

```python
PAGE_HTML = """
<p>Welcome, {name}!</p>
<p>Products:</p>
<ul>
{products}
</ul>
"""
PRODUCT_HTML = "<li>{prodname}: {price}</li>\n"
```

我们将动态的内容定义为了变量，并用 "{}" 将其包装了起来以便于与普通文本区分。下一步要做的就是将变量替换为值：

```python
def make_page(username, products):
    product_html = ""
    for prodname, price in products:
        product_html += PRODUCT_HTML.format(
            prodname=prodname, price=format_price(price))
    html = PAGE_HTML.format(name=username, products=product_html)
    return html
```

利用 Python 的 `format()` 函数，我们将前边定义的变量替换为需要的值，即可完成页面的渲染。

这看起来不错，但是如果我们需要修改 HTML 的内容呢？它是嵌入在我们的程序中的，难道修改一下 HTML 代码还需要修改我们后端的程序源代码么？这显然不合理。

### 模板

更好的方式是使用*模板*。就像下边的这些代码：

```html
<p>Welcome, {{user_name}}!</p>
<p>Products:</p>
<ul>
{% for product in product_list %}
    <li>{{ product.name }}:
        {{ product.price|format_price }}</li>
{% endfor %}
</ul>
```

我们把主要的工作放到了页面中来，而不是后端程序中。在这里我们的主要代码是由静态的 HTML 标记组成的，而不是 Python 的逻辑。下边看一个示例：

```python
def hello():
    print("hello, world")
```

最简单的 hello world 程序，Python 解释这个程序时，会把特殊的标记如 `def hello()` 这样的文字解释为需要执行的标记，而引号引起来的内容解释为普通文本。绝大多数的编程语言都是这样工作的：大多数的动态指令，小部分的静态标记。

而现在看一下我们的模板：

```html
<p>Welcome, {{user_name}}!</p>
```

它将这个行为给颠倒了：大部分的标记都是静态的，特殊标记被解释为可执行的动态部分。在这个例子中 `{{}}` 被解释为特殊标记，被括起来的内容用变量的值来替换。这样我们就实现了前后端的分离。

其实我们在替换那里用到的 `format()` 函数就是模板思想的最佳例子，`hello, {name}.format(name="Joey")`。

为了使用模板来撰写 HTML 页面，我们需要一个模板引擎：一个函数，它使用静态模板来描述页面的结构和静态内容，以及提供插入模板的动态数据的动态上下文。模板引擎结合模板和上下文生成完整的 HTML 字符串。模板引擎的工作是解释模板，用实际数据替换动态部分。

#### 模板的语法

我们要实现的模板引擎基于 Django 模板的语法：

- {{user_name}} ："{{}}" 括起来的是变量
- {% if conditon %} 或者 {% for i in iterable%}："{%%}" 之间可以为 if 语句或者 for 语句
- {%endif%} 或 {%endfor%}：结束条件或循环
- {{obj.method}} 或 {{dict.key}} 或 {{obj.attr}}：在 Python 中，`dict['key']/obj.attr/obj.method()` 表示的是不同的含义，而在我们的模板中这三种调用都由点号来获取
- {{username| lower}}：过滤器的支持，`lower` 可以将用户名全部转化为小写字母
- {# This is comment#}：当然，还支持注释

#### 实现方法

下面开始着手实现。总体而言，模板引擎将有两个主要阶段：解析模板，然后渲染模板。

渲染模板可以分为三个步骤：

- 管理动态的数据上下文
- 执行逻辑元素结构
- 实现点调用方法和过滤器

从解析阶段向渲染阶段传递什么东西是问题的关键。解析出什么来供渲染阶段去渲染？一般有两个选择，我们叫它们解释和编译。

在一个解释模型中，解析产生一个数据结构表示模板，渲染阶段遍历那个数据结构，基于找到的指令装载结果文本。Django 模板引擎就是使用的这种方法。而在一个编译模型中，解析产生某种形式的可直接执行的代码。渲染阶段执行那个代码，产生结果。Jinja2 和 Mako 都是使用编译方法的模板引擎。

编译模型的优势是程序运行速度快，但是较为复杂，正好与解释模型相反（类比编程语言就好，解释型语言通常学习曲线平缓，但是效率低；编译型语言执行效率高，但是学习曲线陡峭）。为了长远考虑，我们选择使用编译模型来完成我们的模板引擎。

#### 编译成 Python

**CoderBuilder**

首先我们需要一个能把模板转化为 Python 代码的类，我们称之为 CoderBuilder。

```python
class CodeBuilder(object):
    """Build source code conveniently."""

    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent
```

CoderBuilder 类维护了一个列表，保存需要转化的代码。还有一个 `indent_level` 属性，代表代码需要的缩进值（毕竟 Python 是被称为需要用游标卡尺书写的语言）。

```python
def add_line(self, line):
    """Add a line of source to the code.
    Indentation and newline will be added for you, don't provide them.
	"""
    self.code.extend([" " * self.indent_level, line, "\n"])
```

`add_line()` 方法将一行代码添加到代码列表中，注意这里就用到了缩进值。

```python
def add_section(self):
    """Add a section, a sub-CodeBuilder."""
    section = CodeBuilder(self.indent_level)
    self.code.append(section)
    return section
```

`add_section()` 方法是在添加多行代码时使用的。它由另一个 CoderBuilder 实例管理。所以在 `self.code` 列表中除了代码字符串，还包含了 CoderBuilder 实例的引用。

```python
INDENT_STEP = 4      # PEP8 says so!

def indent(self):
    """Increase the current indent for following lines."""
    self.indent_level += self.INDENT_STEP

def dedent(self):
    """Decrease the current indent for following lines."""
    self.indent_level -= self.INDENT_STEP
```

这两个方法用于调整代码的缩进值。当需要增加缩进时，调用 `indent()` 方法，否则调用 `dedent()` 方法即可。

```python
def __str__(self):
    return "".join(str(c) for c in self.code)
```

这是一个特殊方法，当我们调用 `str(CoderBuilder 实例 )` 的时候它被调用。它将 `self.code` 中的所有代码字符串拼接到了一起。当然，`self.code` 中还包含了其他实例的引用，所以这个方法可能会被递归调用，直到所有的代码字符串都拼接到了一起，而后返回这个代码字符串。

```python
def get_globals(self):
    """Execute the code, and return a dict of globals it defines."""
    # A check that the caller really finished all the blocks they started.
    assert self.indent_level == 0
    # Get the Python source as a single string.
    python_source = str(self)
    # Execute the source, defining globals, and return them.
    global_namespace = {}
    exec(python_source, global_namespace)
    return global_namespace
```

`get_globals()` 方法产生最终的代码，它将代码字符串转化为可执行的 Python 代码。怎么做到的呢？这里用到了 Python 的一个 " 魔法方法 "：`exec` 函数执行一串包含 python 代码的字符串，它的第二个参数是一个字典，用来收集字符串代码中定义的全局变量。举例如下：

```python
python_source = """\
SEVENTEEN = 17

def three():
    return 3
"""
global_namespace = {}
exec(python_source, global_namespace)
```

执行过后 `global_namespace['SEVENTEEN']` 的值就是 17，`global_namespace['three']` 的值就是名为 `three` 的函数。

通过这个特性，我们就可以得到可执行的 Python 代码了。

#### Templite

下边开始实现模板类。

先看一下我们的模板：

```html
<p>Welcome, {{user_name}}!</p>
<p>Products:</p>
<ul>
{% for product in product_list %}
    <li>{{ product.name }}:
        {{ product.price|format_price }}</li>
{% endfor %}
</ul>
```

```python
class Templite:
    def __init__(self, text, *contexts):
        self.content = {}
        for context in contexts:
            self.content.update(context)
            
        self.all_vars = set()
        self.loop_vars = set()
        
        code = CoderBuilder()
        code.add_line("def render_function(context, do_dots):")
        code.indent()
        vars_code = code.add_setion()   ###### Why???
        code.add_line("result = []")
        code.add_line("append_result = result.append")
        code.add_line("extend_result = result.extend")
        code.add_line("to_str = str")
```

`render_function()` 函数就是我们最终要用来渲染的函数，它接收两个参数，`context` 是一个字典，`do_dots` 方法实现方法的调用。

```python
		buffered = []
        def flush_output():
            """Force `buffered` to the code builder."""
            if len(buffered) == 1:
                code.add_line("append_result(%s)" % buffered[0])
            elif len(buffered) > 1:
                code.add_line("extend_result([%s])" % ", ".join(buffered))
            del buffered[:]
```

`buffered` 暂存需要渲染的代码，`flush_output` 函数将其渲染。

为什么要用闭包？？？？？？

下面是我们为编译它书写的代码：

```python
def render_function(context, do_dots):
    c_user_name = context['user_name']
    c_product_list = context['product_list']
    c_format_price = context['format_price']

    result = []
    append_result = result.append
    extend_result = result.extend
    to_str = str

    extend_result([
        '<p>Welcome, ',
        to_str(c_user_name),
        '!</p>\n<p>Products:</p>\n<ul>\n'
    ])
    for c_product in c_product_list:
        extend_result([
            '\n    <li>',
            to_str(do_dots(c_product, 'name')),
            ':\n        ',
            to_str(c_format_price(do_dots(c_product, 'price'))),
            '</li>\n'
        ])
    append_result('\n</ul>\n')
    return ''.join(result)
```



