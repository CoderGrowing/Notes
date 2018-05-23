## Redis

### 1. 什么是Redis

Redis是Remote Dictionary Server（远程字典服务器）的缩写，它用字典结构存储数据，并允许其他应用通过TCP协议读写字典中的内容。

Redis数据库的所有数据都存储在内存中，当然Redis也提供对持久化的支持，可以将内存中的数据异步写入到硬盘中。

### 2. 安装和启动Redis

Redis不支持Windows系统，Windows下需要借助cygwin来运行。其他POSIX系统可以直接安装运行Redis。

```bash
wget http://download.redis.io/redis-stable.tar.gz
tar zxvf redis-stable.tar.gz
cd redis-stable
make
# make install
```

安装完成后，Redis可执行文件如下：

- redis-server：Redis服务器
- redis-cli：Redis命令行客户端
- redis-benchmark：Redis性能测试工具
- redis-check-aof：AOF文件修复工具
- redis-check-dump：RDB文件检查工具

Redis服务器默认端口为6379，通过参数--port可以修改这个参数。

启动Redis服务器：

```bash
redis-server
```

启动Redis客户端：

```bash
redis-cli
```

测试连接是否正常：

```bash
redis 127.0.0.1:6379> ping
# PONG
```

### 3. 基本数据结构

Redis中共有五个基本数据结构：字符串、散列、集合、列表和有序集合。

#### 3.1 字符串

Redis字符串不同于编程语言中字符串的概念，它可以存储以下三种类型的值：

- 字节串（byte string）
- 整数
- 浮点数

用户可以对存储整数和浮点数的字符串进行自增或自减操作。整数的取值范围和系统的长整数（long integer）取值范围相同，浮点数则与double类型相同。

常用命令：

```bash
GET key   # 获取key对应的值，若键不存在返回(nil)
SET key value  # 成功返回True

INCR key  			#将key的值加1，若key不存在则key的值设为1 返回增加后key的值
INCRBY key 2 		# 将key的值增加2  返回增加后key的值
INCRBYFLOAT key 2.7  # 可以设置浮点数值
# 对应的还有DECR/DECRBY命令减少值，但没有DECRBYFLOAT

APPEND key "content" # 向尾部追加值  返回增加后key的长度

STRLEN key           # 获取key的长度
MGET key1 key2		 # 同时获取多个键的数据
MSET key1 v1 key2 v2 # 同时设置多个键的数据

GETBIT key offset    # 获取offset处键的值（0或1）
SETBIT key offset value   # 设置offset处的值
BITCOUNT key [start] [end]  #从start到end处值为1的2进制位的长度
BITTOP operation destkey key [key...]   # 进行AND、OR、XOR或NOT操作

type key             # 获取key的类型

KEYS pattern         # 获取符合规则的键名列表，支持glob风格通配符
EXISTS key           # key存在返回1，否则返回0
DEL key  			# 删除key
```

#### 3.2 散列类型

散列类型的键值也是一种字典结构，存储了字段和字段值的映射。但字段值只能是字符串。一个散列类型建最多可以存储2^32^-1个字段。

散列类型对应的常用命令如下：

```bash
HSET key field value        # 给字段赋值；若字段存在，更新值，返回0；不存在，创建字段，返回1
HGET key field              # 获取字段对应的值
HGETALL key                 # 获取所有的字段名
HMSET key field value [field value ...]     # 同时给多个字段赋值
HMGET key field [field...]  # 同时获取多个字段的值

HEXISTS key field           # 判断字段是否存在，存在返回1，否则返回0
HSETNX ksy field value      # 字段不存在时赋值，存在时则不进行操作

HINCRBY key field increment # 增加值
HDEL key field [field...]   # 删除一个或多个值

HKEYS key                   # 只获取字段名
HVALS key                   # 只获取值
HLEN  key				  # 获取字段数量
```

#### 3.3 列表类型

```bash
LPUSH key value [value...]  	# 从左边向列表添加元素
RPUSH key value [value...]      # 从右边向列表添加元素

LPOP key                         # 从左边弹出元素，同理有RPOP

LLEN key					  # 获取列表中元素的个数
LRANGE key start stop  			# 获取列表片段

# 从列表中删除指定的值  
# count > 0 从左开始删除count个值为value的元素
# count < 0 从右边删除
# count = 0 删除全部的值为value的元素
# 返回值为实际删除的元素个数
LREM key count value			

LINDEX key index                 # 用来返回指定索引处的元素
LSET key index value             # 将制定索引出的元素值设为value

LTRIM key start end              # 切片，只保留指定的start--end的片段（均含）

# 从左向右查找值为pivot的元素，再根据after或者before决定插入位置
LINSERT key before|after pivot value  

RPOPLPUSH source destination      # 先执行RPOP在执行LPUSH，将值从source转入到destination中
```

#### 3.4 集合类型

集合类型无序、不存储重复，同样是最多存储2^32^-1个字符串。

```bash
SADD key member [member...]             # 增加元素
SREM key member [member...]             # 删除元素

SMEMBERS key                            # 获取key中的所有元素
SISMEMBER key member                    # 判断元素是否在集合中

# 集合间运算
SDIFF key [key...]                      # 将集合进行差集运算
SINTER key [key...]                     # 将集合进行交集运算
SUNION key [key...]                     # 将集合进行并集运算

SCARD key    						  # 获取集合中元素个数

# 类似于SDIFF但不返回结果而是将结果存储在destination，同理还有SINTERSTORE   SUNIONSTORE
SDIFFSTORE destination key [key...]     

# 随机获取集合中的元素，指定count时可以返回多个元素
# count为正数时随机从集合中获取count个元素，不重复，count>size时返回整个集合
# count为负数时，随机获取|count|个元素，可能重复
SRANDMEMBER key [count]	 		
```

#### 3.5 有序集合类型

```bash
# 添加一个元素和该元素的分数，若已存在则替换，返回值是新加的元素个数
ZADD key score member [score member...]           

ZSCORE key number 			# 获得元素的分数

# 按照元素分数大小的顺序返回索引从start到stop的所有元素（含两端）
ZRANGE key start stop [WITHSCORES]			
ZREVRANGE key start stop [WITHSCORES]   # 同上，但是反序输出

# 获得指定分数范围内的元素
ZRANGEBYSOCRE key min max [WITHSCORES] [LIMIT OFFSET COUNT]
```

### 4. 其他常用命令

#### 4.1 发布/订阅

```bash
SUBSCRIBE channel [channel...]      # 订阅一个或多个频道
UNSUBSCRIBE [channel...]            # 退订一个或多个频道，如果不指定，退订所有的
PUBLISH channel message             # 向给定频道发送消息
PSUBSCRIBE pattern [pattern...]     # 订阅与给定模式相匹配的所有频道
PUNSUBSCRIBE pattern [pattern...]   # 退订给定的模式，若不指定，退订所有
```

#### 4.2 排序



#### 4.1 事务

Redis中的事务（transaction）是一组命令的集合，要么都执行，要么都不执行。

使用`MULTI`命令来通知Redis以下的命令都是事务的一部分，当命令输入完成后，使用`EXEC`来执行队列中的所有命令。

```bash
MULTI
SADD "user:1:following" 2
SADD "user:2:followers" 1
EXEC
```

#### 4.2 过期时间

使用`EXPIRE`命令来存储一些有时效的数据，过期会自动删除。

```bash
EXPIRE key seconds                # 设置键的过期时间为seconds秒
TTL key							# 返回一个键还有多久被删除；永久的键返回-1，键不存在返回-2
PERSIST key						# 将键设为永久（默认值）
```

#### 4.3 排序

