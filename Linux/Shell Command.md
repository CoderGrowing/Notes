## 权限相关

#### chown: 更改文件所有者(change owner)

- chown user.group file 可直接修改用户和组
- chown .group file 只修改组

#### chgrp: 更改所属用户组(change group)

#### chmod: 更改文件权限

- 数字方式：chmod 777 filename
- 权限方式：chmod u+x filename

更改权限可用的方式：

用户身份：

- u：user，用户
- g：group，用户组
- o：others，其他
- a：all，所有

设置内容

- +：加上
- -：除去
- =：设置为

如修改所有人权限为只读：chmod a=r filename

注意对于目录而言，拥有r权限可以列出目录下的内容，拥有x权限才可进入目录。

## 文件与目录管理

#### cp: 复制

参数：

-a：相当于-pdr

-d：若源文件为连接文件的属性(link file)，则复制文件属性而非文件本身

-f：force，若文件已经存在且无法开启，则删除后再尝试一次

-i：若目标文件已经存在，覆盖时会先询问再进行

-l：进行硬连接(hard link)的连接文件创建

-p：连同文件的属性一同复制过去，而非使用默认属性(常用来备份)

-r：递归复制

-s：复制成为符号连接文件，即快捷方式

-u：若destination比source新才更新destination

#### touch: 修改文件时间或者创建新文件

Linux下有三个主要的变动时间：

- modification time(mtime)：文件内容的修改时间
- status time(stime)：文件权限或者属性的修改时间
- access time(atime)：文件访问时间

默认情况下ls命令查看的是文件的mtime，当然我们也可以查看其它两个时间，使用`--time=ctime`或者`--time=atime`即可，如`ls -l --time=ctime /etc`。

用`touch`命令可以更改文件的时间。

参数：

-a：仅修改访问时间

-c：仅修改文件的时间，若文件不存在则创建文件

-d：后面接欲修改的日期而不是使用当前日期

-m：仅修改mtime

-t：后面接欲修改的时间而不是使用当前时间，格式为[YYMMDDhhmm]

#### umask: 文件默认权限

umask指定目前用户在新建文件或者目录时候的权限默认值。

默认的umask值为：0022。那这四个数字什么意思呢？我们先来看

fffffffff





