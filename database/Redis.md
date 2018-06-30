## Redis

### 1. 什么是 Redis

Redis 是 Remote Dictionary Server（远程字典服务器）的缩写，它用字典结构存储数据，并允许其他应用通过 TCP 协议读写字典中的内容。

Redis 数据库的所有数据都存储在内存中，当然 Redis 也提供对持久化的支持，可以将内存中的数据异步写入到硬盘中。

### 2. 安装和启动 Redis

Redis 不支持 Windows 系统，Windows 下需要借助 cygwin 来运行。其他 POSIX 系统可以直接安装运行 Redis。

```bash
wget http://download.redis.io/redis-stable.tar.gz
tar zxvf redis-stable.tar.gz
cd redis-stable
make
# make install
```

安装完成后，Redis 可执行文件如下：

- redis-server：Redis 服务器
- redis-cli：Redis 命令行客户端
- redis-benchmark：Redis 性能测试工具
- redis-check-aof：AOF 文件修复工具
- redis-check-dump：RDB 文件检查工具

Redis 服务器默认端口为 6379，通过参数 --port 可以修改这个参数。

启动 Redis 服务器：

```bash
redis-server
```

启动 Redis 客户端：

```bash
redis-cli
```

测试连接是否正常：

```bash
redis 127.0.0.1:6379> ping
# PONG
```

### 3. 基本数据结构

Redis 中共有五个基本数据结构：字符串、散列、集合、列表和有序集合。

#### 3.1 字符串

Redis 字符串不同于编程语言中字符串的概念，它可以存储以下三种类型的值：

- 字节串（byte string）
- 整数
- 浮点数

用户可以对存储整数和浮点数的字符串进行自增或自减操作。整数的取值范围和系统的长整数（long integer）取值范围相同，浮点数则与 double 类型相同。

常用命令：

```bash
GET key   # 获取 key 对应的值，若键不存在返回 (nil)
SET key value  # 成功返回 True

INCR key  			# 将 key 的值加 1，若 key 不存在则 key 的值设为 1 返回增加后 key 的值
INCRBY key 2 		# 将 key 的值增加 2  返回增加后 key 的值
INCRBYFLOAT key 2.7  # 可以设置浮点数值
# 对应的还有 DECR/DECRBY 命令减少值，但没有 DECRBYFLOAT

APPEND key "content" # 向尾部追加值  返回增加后 key 的长度

STRLEN key           # 获取 key 的长度
MGET key1 key2		 # 同时获取多个键的数据
MSET key1 v1 key2 v2 # 同时设置多个键的数据

GETBIT key offset    # 获取 offset 处键的值（0 或 1）
SETBIT key offset value   # 设置 offset 处的值
BITCOUNT key [start] [end]  # 从 start 到 end 处值为 1 的 2 进制位的长度
BITTOP operation destkey key [key...]   # 进行 AND、OR、XOR 或 NOT 操作

type key             # 获取 key 的类型

KEYS pattern         # 获取符合规则的键名列表，支持 glob 风格通配符
EXISTS key           # key 存在返回 1，否则返回 0
DEL key  			# 删除 key
```

#### 3.2 散列类型

散列类型的键值也是一种字典结构，存储了字段和字段值的映射。但字段值只能是字符串。一个散列类型建最多可以存储 2^32^-1 个字段。

散列类型对应的常用命令如下：

```bash
HSET key field value        # 给字段赋值；若字段存在，更新值，返回 0；不存在，创建字段，返回 1
HGET key field              # 获取字段对应的值
HGETALL key                 # 获取所有的字段名
HMSET key field value [field value ...]     # 同时给多个字段赋值
HMGET key field [field...]  # 同时获取多个字段的值

HEXISTS key field           # 判断字段是否存在，存在返回 1，否则返回 0
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

LPOP key                         # 从左边弹出元素，同理有 RPOP

LLEN key					  # 获取列表中元素的个数
LRANGE key start stop  			# 获取列表片段

# 从列表中删除指定的值  
# count > 0 从左开始删除 count 个值为 value 的元素
# count < 0 从右边删除
# count = 0 删除全部的值为 value 的元素
# 返回值为实际删除的元素个数
LREM key count value			

LINDEX key index                 # 用来返回指定索引处的元素
LSET key index value             # 将制定索引出的元素值设为 value

LTRIM key start end              # 切片，只保留指定的 start--end 的片段（均含）

# 从左向右查找值为 pivot 的元素，再根据 after 或者 before 决定插入位置
LINSERT key before|after pivot value  

RPOPLPUSH source destination      # 先执行 RPOP 在执行 LPUSH，将值从 source 转入到 destination 中
```

#### 3.4 集合类型

集合类型无序、不存储重复，同样是最多存储 2^32^-1 个字符串。

```bash
SADD key member [member...]             # 增加元素
SREM key member [member...]             # 删除元素

SMEMBERS key                            # 获取 key 中的所有元素
SISMEMBER key member                    # 判断元素是否在集合中

# 集合间运算
SDIFF key [key...]                      # 将集合进行差集运算
SINTER key [key...]                     # 将集合进行交集运算
SUNION key [key...]                     # 将集合进行并集运算

SCARD key    						  # 获取集合中元素个数

# 类似于 SDIFF 但不返回结果而是将结果存储在 destination，同理还有 SINTERSTORE   SUNIONSTORE
SDIFFSTORE destination key [key...]     

# 随机获取集合中的元素，指定 count 时可以返回多个元素
# count 为正数时随机从集合中获取 count 个元素，不重复，count>size 时返回整个集合
# count 为负数时，随机获取 |count| 个元素，可能重复
SRANDMEMBER key [count]	 		
```

#### 3.5 有序集合类型

```bash
# 添加一个元素和该元素的分数，若已存在则替换，返回值是新加的元素个数
ZADD key score member [score member...]           

ZSCORE key number 			# 获得元素的分数

# 按照元素分数大小的顺序返回索引从 start 到 stop 的所有元素（含两端）
ZRANGE key start stop [WITHSCORES]			
ZREVRANGE key start stop [WITHSCORES]   # 同上，但是反序输出

# 获得指定分数范围内的元素
ZRANGEBYSOCRE key min max [WITHSCORES] [LIMIT OFFSET COUNT]
```

### 4. 其他常用命令

#### 4.1 发布 / 订阅

```bash
SUBSCRIBE channel [channel...]      # 订阅一个或多个频道
UNSUBSCRIBE [channel...]            # 退订一个或多个频道，如果不指定，退订所有的
PUBLISH channel message             # 向给定频道发送消息
PSUBSCRIBE pattern [pattern...]     # 订阅与给定模式相匹配的所有频道
PUNSUBSCRIBE pattern [pattern...]   # 退订给定的模式，若不指定，退订所有
```

#### 4.2 排序



#### 4.1 事务

Redis 中的事务（transaction）是一组命令的集合，要么都执行，要么都不执行。

使用 `MULTI` 命令来通知 Redis 以下的命令都是事务的一部分，当命令输入完成后，使用 `EXEC` 来执行队列中的所有命令。

```bash
MULTI
SADD "user:1:following" 2
SADD "user:2:followers" 1
EXEC
```

#### 4.2 过期时间

使用 `EXPIRE` 命令来存储一些有时效的数据，过期会自动删除。

```bash
EXPIRE key seconds                # 设置键的过期时间为 seconds 秒
TTL key							# 返回一个键还有多久被删除；永久的键返回 -1，键不存在返回 -2
PERSIST key						# 将键设为永久（默认值）
```

#### 4.3 排序

