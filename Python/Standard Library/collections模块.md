## collections模块

#### 1. collections.namedtuple

顾名思义，namedtuple就是有名字的元组，即具名元组。常常用来构建只有属性没有方法的对象。

```python
from collections import namedtuple

City = namedtuple('City', 'name country population')
beijing = City('Beijing', 'CN', '1000')

# >>> bejing
# City(name='Beijing', country='CN', population='1000')
# >>> beijing.name
# Beijing
```

**具名元组的方法和属性**

```python
# 获取具名元组的字段名
# >>> City._fields
# ('name', 'country', 'population')

# 利用_make创建
# beijing_data = ('Beijing', 'CN', '1000')
# >>> City._make(beijing_data)
# City(name='Beijing', country='CN', population='1000')

```

#### 2. defaultdict

在新建一个defaultdict对象时，需要给它配置一个创建默认值的方法。

```python
import collections

index = collections.defaultdict(list)
```



#### 