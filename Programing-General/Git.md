# Git

**1. 每次向远程仓库提交都需要输入 github 用户名和密码**

问题可能出在推送的协议上，如果使用的是 HTTPS 协议，则需要每次都输入用户名密码，将其改为 SSH 协议即可。

```shell
> git remote -v             // 查看远程地址
> git remote rm origin      // 删除原有的推送地址
> git remote add origin git@github.com:< 用户名 >/ 版本库名
```

