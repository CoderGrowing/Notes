## Linux 设备与磁盘管理

### 1.1 设备在 Linux 下的文件名

所有的设备在 Linux 下都是以文件的方式被识别的。那么如何通过文件名来辨别设备呢？

常见的设备在 Linux 下的文件名如下：

| 设备               | 设备对应的文件名                           |
| ------------------ | ------------------------------------------ |
| SATA/USB 硬盘       | /dev/sd[a-p]                               |
| U 盘                | /dev/sd[a-p]（与硬盘相同）                 |
| 打印机             | 25 针：/dev/lp[0-2]；USB：/dev/usb/lp[0-15] |
| 鼠标               | /dev/usb/mouse[0-15]                       |
| 当前 CD ROM/DVD ROM | /dev/cdrom                                 |
| 当前鼠标           | /dev/mouse                                 |

需要注意的是，硬盘和 U 盘具有相同的文件名格式，具体区分在于开机时的识别顺序。开机首先识别的为 /dev/sda，然后是 /dev/sdb ……

最后，我们还经常见到类似 /dev/sdb3 这样的格式。最后的标号是分区。

### 1.2 磁盘分区

传统磁盘中最小的单位是扇区 (sector)，大小一般为 512bytes。整块磁盘的第一个扇区最为重要，它记录了两个信息：

- 主引导分区 (Master Boot Record, MBR)，安装引导加载程序的地方，占用 446bytes
- 分区表（partition table）：记录整块硬盘分区情况的地方，有 64bytes

由于分区表的大小限制，所以硬盘最多只能被分为 4 个分区，这 4 个分区被称为主分区（primary partition）或者扩展分区（extended partition）。那如果需要更多的分区呢？那我们可以用额外的扇区记录分区表，这就是扩展分区的作用。由扩展分区再次切割出来的分区，被称为逻辑分区（logical partition）。

总结如下：

- 主分区和扩展分区最多只要四个（分区表大小所限制）
- 扩展分区最多只有一个（操作系统所限制）
- 扩展分区的目的在于切割为更多的逻辑分区，扩展分区本身无法被格式化。

### 1.3 开机流程

从按下开机键到系统启动中间经历了怎样的过程呢？

1. 按下开机键，BIOS 主动执行，识别第一个可开机的设备（硬盘、U 盘等）
2. 第一个可开机设备的第一个扇区的主引导 MBR 执行其中的引导加载程序
3. 引导加载程序（Boot loader）开始执行，读取系统内核文件
4. 内核文件开始执行操作系统的功能

需要注意的是 BIOS 和 MBR 都是硬件支持的功能，而 Boot loader 则是操作系统安装在 MBR 中的一套软件。

### 1.4 文件系统的结构 

在 Linux 系统下文件的数据包含文件权限（rwx）、文件属性（所有者、修改时间等）和文件的实际内容。Linux 惯用的 ext 文件系统会将这两部分数据放置到不同块中。

- inode：记录文件的属性，一个文件占用一个 inode，同时记录此文件的数据所在的 block 号码
- block：实际记录文件的内容，大文件会占用多个 block 块
- super block：记录文件系统的整体信息，包含 inode 和 block 的使用量等

有了 inode 记录 block 块号码，操作系统读取大文件时就可以直接读取多个块的内容啦。而对于 U 盘惯用的 FAT 系统，并没有 inode。它采取的方式是每个 block 号码记录在前一个 block 中。这样读取就需要一个个的挨个读取了。

这也是为何旧文件系统需要“碎片整理”的原因。当 block 太过分散时，磁盘需要转好几圈才能读取完毕一个文件，导致性能下降。“碎片整理”就是将同一个文件的 block 块汇合在一起。

### 1.5 inode、block 和 super block

通常，系统并不会将所有的 inode 和 block 块放置在一起，而是采用多个块组的形式来组织文件系统。每个块组都有自己的 inode/block/super block。

#### 1.5.1 block

ext 文件系统支持多个 block 大小，1KB，2KB 和 4KB。在格式化时系统的 block 大小就已经确定。那么不同大小的 block 对使用有什么影响呢？

**1. block 越大所支持的最大单一文件和最大文件系统就越大。**

| block 大小          | 1KB  | 2KB   | 4KB  |
| ------------------ | ---- | ----- | ---- |
| 最大单一文件限制   | 16GB | 256GB | 2TB  |
| 最大文件系统总容量 | 2TB  | 8TB   | 16TB |

**2. 每个 block 最多可放置一个文件的数据，用不完的 block 会被浪费掉。**

#### 1.5.2 inode

inode 的特点如下：

- 每个 inode 的大小为 128bytes
- 每个文件都会占用一个 inode

当文件很大时，会占用数以十万甚至百万计的 block 块。那么 128bytes 大小的 inode 怎么记录每一个 block 的信息呢？

系统采用了间接记录的方法。一个 inode 中包含 12 个直接记录、1 个间接、1 个双间接和一个三间接记录区。使用直接记录时，inode 直接指向 block 的号码。当文件过大间接记录不够用时，inode 会使用一个 block 块来间接记录 block 信息。文件更大时会使用双间接、三间接记录区。

#### 1.5.3 super block

super block 记录了整个文件系统的相关信息，包括：

- block 和 inode 的总量和已使用、未使用的量
- block 和 inode 的大小
- 文件系统的挂载时间、最近写入数据的时间等
- 一个 validbit 值， 文件系统已被挂载时 valid bit 为 1，否则为 0

dumpe2fs 命令可以查看 super block 相关的信息。

