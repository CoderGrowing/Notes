## Pythonic写法

#### 1. 两个数是否都为正数

```python
(num1) < 0 is (num2) < 0
```

#### 2. 找出列表中唯一一个单数元素(其他都有两个，只有该元素只出现一次)

```python
res = 0
for i in num:
    res ^= i
return res
```



