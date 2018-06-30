```java
// 新建一个套接字
Socket s = new Socket("host", "port");
s.setTimeout(1000);  // 1s 超时

InputStream in = s.getInputStream();  // 获取 InputStream
OutputStream out = s.getOutputStream(); // 获取输出流

ServerSocket server = new ServerSocket(int port);	// 创建一个监听端口的套接字
server.accept();   // 等待连接
server.close();    // 关闭连接
```

