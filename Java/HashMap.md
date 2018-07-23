# HashMap

## 1. 简介

HashMap 是Java开发中使用频率最高的键值对数据类型容器。它根据键的哈希值（hashCode）来存储数据，访问速度高，但无法按照顺序遍历。HashMap 允许键值为空和记录为空，非线程安全。

另外，如果想要保持有序，可以使用LinkedHashMap。LinkedHashMap 是 HashMap 的一个子类，保存了记录的插入顺序，在用 Iterator 遍历 LinkedHashMap 时，先得到的记录肯定是先插入的，也可以在构造时带参数，按照访问次序排序。

## 2. 存储结构

HashMap 是数组 + 链表 + 红黑树（JDK1.8 新增）实现的哈希表结构，如下图如所示：

![](http://oqag5mdvp.bkt.clouddn.com/201804121006_86.jpg)

HashMap内部维护的数组类型为Node（jdk 1.8以前为Entry，仅仅换了名字）

```java
transient Node[] table;
```

Node就是存储数据的键值对，它包含了四个字段，具体的实现如下：

```java
static class Node<K, V> implements Map.Entry<K, V> {
    final int hash;    //用来定位数组索引位置
    final K key;
    V value;
    Node<K, V> next;   //链表的下一个node
    
    Node(int hash, K key, V value, Node<K, V> next) { ...}
    public final K getKey() { ...}
    public final V getValue() { ...}
    public final String toString() { ...}
    public final int hashCode() { ...}
    public final V setValue(V newValue) { ...}
    public final boolean equals(Object o) { ...}
}
```

由next字段可以看出，Node其实还是一个链表，即数组中的每个位置都被当成一个桶，一个桶存放一个链表，链表中存放哈希值相同的元素。 

执行代码时，Java 会调用 key 的 hashCode 方法，计算哈希值，而后通过 Hash 算法的后两步运算（高位运算和取模运算）来定位该键值对在数组中的存储位置。而后遍历该位置上的链表，即可得到所要的值。

key 的哈希值有可能相同，造成 Hash 碰撞。避免 Hash 碰撞的方法主要有两种：采用更好的哈希函数（根据数据计算哈希值的函数）和更大的哈希数组。当然，数组过大时会造成空间的浪费，因此在效率和空间上需要做一个权衡。Java 采用了扩容机制来权衡数组大小。具体而言，每个哈希数组有一个上限大小和一个负载因子，当数据达到上限* 负载因子后，数组大小翻倍。**默认数组大小为 16，负载因子为 0.75。**

需要注意的是，哈希表的大小一定为 2 的整数次方。所以当调用 `new HashMap<>(19)` 时，哈希表的大小为 32。（原因后面解释）

### 2.1 解决哈希冲突

哈希表为解决 Hash 冲突，可以采用**开放地址法**和**链地址法**来解决问题。HashMap 采用了链地址法。链地址法，简单来说，就是数组加链表的结合。在每个数组元素上都一个链表结构，当数据被 Hash 后，得到数组下标，把数据放在对应下标元素的链表上。

### 2.2 源码实现

不管增加、删除、查找键值对，定位到哈希数组的位置都是很关键的第一步。我们希望哈希值尽可能少的冲突，最好是数组中的每个位置只有一个元素，这样就可以直接定位，而不用去遍历链表。为了达到这个目的，一个好的定位方法是必须的。

Java 中 Hash 算法本质上就是三步：**取 key 的 hashCode 值、高位运算、取模运算（结果作为数组下标）**。

```java
static final int hash(Object key) {   //jdk1.8 & jdk1.7
     int h;
     // h = key.hashCode() 为第一步 取 hashCode 值
     // h ^ (h >>> 16)  为第二步 高位参与运算
     return (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);
}
```

首先，`hash()` 方法返回 key 的散列值（int 类型）。如果直接拿散列值作为下标访问话，范围从 -2147483648 到 2147483648，这么大的数组当然不能直接拿来使用。Java 是将它进行取模运算后当做数组下标使用的。模运算是在 `indexFor(hash, length)` 函数中完成的：

```java
// 第三步，取模运算，利用与运算来实现，效率比 % 高
static int indexFor(int h, int length) {
    return h & (length - 1);
}
```

不是说模运算么？为什么用的与运算？这是出于性能考虑的。模运算虽然简单便捷，但效率低下。为了更高效的实现模运算，Java 开发团队采用了一种「取巧」的方式来计算模运算的结果。

首先，HashMap 数组的长度必须为 2 的整数次幂，这样数组长度 -1正好相当于一个“**低位掩码”。**与操作的结果就是散列值的高位全部归零，只保留低位值用来做数组下标访问。（解释了为什么扩容总是翻2倍）

例如长度为 16 时，16-1 = 15，位表示为：00000000 00000000 00001111，与散列值做与运算后，只保留了低位的值。但是这样又会造成问题，要是只取最后几位的话，碰撞会很严重。在这里，**高位运算**就起了作用：

```java
h = key.hashCode() ^ (h >>> 16);
```

右位移 16 位，正好是 32bit 的一半，自己的高半区和低半区做异或，就是为了**混合原始哈希码的高位和低位，以此来加大低位的随机性**。而且混合后的低位掺杂了高位的部分特征，这样高位的信息也被变相保留下来。

整个过程如下图所示：

![](http://oqag5mdvp.bkt.clouddn.com/201804121205_64.jpg)

### 2.3 扩容

HashMap的容量是有限的，当元素个数超过负载上限*负载因子后，需要将大小变更为原来的两倍。这个操作的具体流程如下：

1. 扩容：创建一个新的Entry数组，大小为原来的2倍（JDK 1.7源码）

   ```java
   void resize(int newCapacity) {  
       Entry[] oldTable = table;                  //引用扩容前的Entry数组
       int oldCapacity = oldTable.length;         
       if (oldCapacity == MAXIMUM_CAPACITY) {    //扩容前的数组大小如果已经达到最大(2^30)了
           threshold = Integer.MAX_VALUE;    //修改阈值为int的最大值(2^31-1)，这样以后就不会扩容了
           return;
       }
       
       Entry[] newTable = new Entry[newCapacity];  //初始化一个新的Entry数组
       transfer(newTable);                         //！！将数据转移到新的Entry数组里
       table = newTable;                           //HashMap的table属性引用新的Entry数组
       threshold = (int)(newCapacity * loadFactor);//修改阈值
   }
   ```

2. ReHash，因为数组大小不同，Hash的规则也不同了，所以需要进行重新Hash

   ```java
    void transfer(Entry[] newTable) {
        Entry[] src = table;                   //src引用了旧的Entry数组
        int newCapacity = newTable.length;
        for (int j = 0; j < src.length; j++) { //遍历旧的Entry数组
            Entry<K,V> e = src[j];             //取得旧Entry数组的每个元素
            if (e != null) {
                src[j] = null;  //释放旧Entry数组的对象引用
                do {
                    Entry<K,V> next = e.next;
                    int i = indexFor(e.hash, newCapacity); //！！重新计算每个元素在数组中的位置
                    e.next = newTable[i]; //标记[1]
                    newTable[i] = e;      //将元素放在数组上
                    e = next;             //访问下一个Entry链上的元素
                } while (e != null);
            }
        }
    }
   ```

JDK 1.8 对此过程进行了优化。JDK 1.7 版本中，每次扩容都需要进行重新Hash，费时费力，而JDK 1.8则简化了此过程，具体如下：

每次扩容我们都将HashMap的容量变为原来的2倍，所以，元素的位置要么是在原位置，要么是在原位置再移动2次幂的位置。元素在重新计算hash之后，因为n变为2倍，那么n-1的mask范围在高位多1bit(红色)，因此新的index就会发生这样的变化：

![](./assets/a285d9b2da279a18b052fe5eed69afe9_r.jpg)

扩容前HashMap容量为16，两个元素的Hash值均为5。扩容后HashMap容量为32，第一个元素Hash值为5，第二个元素Hash值为21，移动了16位。

因此，我们在扩充HashMap的时候，不需要像JDK1.7的实现那样重新计算hash，只需要看看原来的hash值新增的那个bit是1还是0就好了，是0的话索引没变，是1的话索引变成「原索引+oldCap」。实现这个过程的JDK 1.8源码如下：

```java
final Node<K,V>[] resize() {
    Node<K,V>[] oldTab = table;
    int oldCap = (oldTab == null) ? 0 : oldTab.length;
    int oldThr = threshold;
    int newCap, newThr = 0;
    if (oldCap > 0) {
        // 超过最大值就不再扩充了，就只好随你碰撞去吧
        if (oldCap >= MAXIMUM_CAPACITY) {
            threshold = Integer.MAX_VALUE;
            return oldTab;
        }
        // 没超过最大值，就扩充为原来的2倍
        else if ((newCap = oldCap << 1) < MAXIMUM_CAPACITY &&
                 oldCap >= DEFAULT_INITIAL_CAPACITY)
            newThr = oldThr << 1; // double threshold
    }
    else if (oldThr > 0) // initial capacity was placed in threshold
        newCap = oldThr;
    else {               // zero initial threshold signifies using defaults
        newCap = DEFAULT_INITIAL_CAPACITY;
        newThr = (int)(DEFAULT_LOAD_FACTOR * DEFAULT_INITIAL_CAPACITY);
    }
    // 计算新的resize上限
    if (newThr == 0) {

        float ft = (float)newCap * loadFactor;
        newThr = (newCap < MAXIMUM_CAPACITY && ft < (float)MAXIMUM_CAPACITY ?
                  (int)ft : Integer.MAX_VALUE);
    }
    threshold = newThr;
    @SuppressWarnings({"rawtypes"，"unchecked"})
        Node<K,V>[] newTab = (Node<K,V>[])new Node[newCap];
    table = newTab;
    if (oldTab != null) {
        // 把每个bucket都移动到新的buckets中
        for (int j = 0; j < oldCap; ++j) {
            Node<K,V> e;
            if ((e = oldTab[j]) != null) {
                oldTab[j] = null;
                if (e.next == null)
                    newTab[e.hash & (newCap - 1)] = e;
                else if (e instanceof TreeNode)
                    ((TreeNode<K,V>)e).split(this, newTab, j, oldCap);
                else { // 链表优化重hash的代码块
                    Node<K,V> loHead = null, loTail = null;
                    Node<K,V> hiHead = null, hiTail = null;
                    Node<K,V> next;
                    do {
                        next = e.next;
                        // 原索引
                        if ((e.hash & oldCap) == 0) {
                            if (loTail == null)
                                loHead = e;
                            else
                                loTail.next = e;
                            loTail = e;
                        }
                        // 原索引+oldCap
                        else {
                            if (hiTail == null)
                                hiHead = e;
                            else
                                hiTail.next = e;
                            hiTail = e;
                        }
                    } while ((e = next) != null);
                    // 原索引放到bucket里
                    if (loTail != null) {
                        loTail.next = null;
                        newTab[j] = loHead;
                    }
                    // 原索引+oldCap放到bucket里
                    if (hiTail != null) {
                        hiTail.next = null;
                        newTab[j + oldCap] = hiHead;
                    }
                }
            }
        }
    }
    return newTab;
}
```

## 3. 并发环境下 HashMap 的问题

多线程下 HashMap 会有线程安全的问题，主要是因为 HashMap 需要进行resize的操作。Map进行put操作时，如果同时出发了rehash操作，会导致HashMap中可能出现循环节点。参考酷壳的文章 [疫苗：JAVA HASHMAP的死循环 ](https://coolshell.cn/articles/9606.html)。



