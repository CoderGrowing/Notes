### 由来

1972年由贝尔实验室Dennis Ritchie开发

### 各种C标准

- **ANSI C**：ANSI(美国国家标准化组织)于1989年正式被采用的标准，称为ANSI C，和ISO C相同。也称C89(ANSI于1989年批准该标准)或者C90(ISO于1990年批准该标准)
- **C99**：1994年标准重新修订，产生了C99标准

### 数据类型

| 数据类型     | 格式输出 | 所占位数 |      |
| -------- | ---- | ---- | ---- |
| short    | %h   |      |      |
| int      | %d   |      |      |
| float    | %f   |      |      |
| double   | %lf  |      |      |
| long     | %l   |      |      |
| unsigned | %u   |      |      |

### printf和scanf返回值

- printf: 返回打印字符的个数，若有输出错误，返回一个负数
- scanf：返回成功读入的项目个数，若没有读取(或预期读入类型与实际类型不符)返回0；遇到文件结尾(end of file)EOF返回EOF

### 关键字:const

const用于创建符号常量，在C90中加入。类似于#define，用const限定后的值不可修改，但它比#define更加灵活。

#### const作为形式参数

如果不想让函数对数组(或其他可变类型)做修改，可以将参数用const限定符修饰。在形式参数中使用const并不表示数组不可变，只是声明此函数不可改变数组的值

```c
int sum (const int arr[], int n);
```

#### 指针与const

1. 指向常量的指针，不可用于修改数据，`const double * pd`

   ```c
   double rates[5] = {1.1, 2.2, 3.3, 4.4, 5.5};
   const double * pd = rates;    // pd为指向const double的指针，不可用来修改它指向的数值

   * pd = 8.8;      // 不允许
   pd[2] = 7.7;     // 不允许
   rates[0] = 9.9;  // 允许，因为rates是常量
   pd++;            // 允许，可以指向其他地址
   ```

    通常用作函数参数，表明函数不会用这个指针修改数据。

2. 指向固定地址的指针，不可修改指向，`double * const pc`

   ```c
   double rates[5] = {1.1, 2.2, 3.3, 4.4, 5.5};
   double * const pc = rates;    // pc指向rates开始处
   pc = &rates[2];               // 不允许，不可修改指向
   *pc = 9.88;                   // 允许，可以用来修改值
   ```

3. 既不可更改指向，也不可更改指向的值，`const double * const pc`

   ```c
   double rates[5] = {1.1, 2.2, 3.3, 4.4, 5.5};
   const double * const pc = rates;
   ```

### 宏

每一个#define行都由三部分组成：第一部分为#define自身。第二部分是所选择的缩略语，这些缩略语就称为宏。用于定义常量的宏被称为类对象宏。第三部分(#define行剩余部分)被称为替换列表或主体。

预处理器会用主体将宏替换掉，替换的过程被称为宏展开。

#### 类函数宏

除了类对象宏，我们还可以定义含有参数的类函数宏。宏的参数也是用圆括号括起来，和函数十分相似。

```c
#define SQUARE(X) X*X   // 宏一般用大写
```

注意预处理器只会替换，并不进行计算。如果参数是需要运算的话，可能得到意想不到的结果。

```c
x = 4;
SQUARE(x+2);             // 14???
```

这个14是怎么来的？x*x 变成了 x+2 * x+2 = 14。尽量避免在宏的参数中进行计算。

#### 宏和函数

宏和函数都能完成类似的功能，选择宏还是函数？以下几点需要注意：

- 编译器一般限制宏只能定义为一行，一般用于简单地函数。
- 宏不检查参数类型， int或者float、double都可使用SQUARE。
- 宏产生内联代码，速度比函数快，但浪费空间。


