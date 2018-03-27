# Java I/O

### File类

常用方法如下：

- `File(String pathname)`：为一个指定的路径创建一个File对象，路径名可以为目录或者文件
- `File(String/File parent, String child)`：在目录parent下新建一个子路径的File对象，子路径可能为目录或者文件。注意这里的parent可以为字符串或者File对象
- `exists()`：File对象代表的文件和目录存在就返回true
- `canRead()`、`canWrite()`、`isDiretory()`、`isFile()`：可读/可写、是目录、是文件
- `isAbsolute()`：File对象是否是绝对路径创建的


### 2. 文件输入和输出

使用Scanner类从文件中读取文本数据，使用PrintWriter类向文本文件中写入数据。

**PrintWriter**

首先应该为一个文本文件创建一个PrintWriter对象：

```java
PrintWriter output = new PrintWriter(filename);
```

常用方法：

- `PrintWriter(File file)`：为指定的文件对象创建一个PrintWriter对象
- `PrintWriter(String filename)`：为指定的文件名字创建一个PrintWriter对象


- `print(E s)`：将内容写入文件中，参数可为字符串、字符、字符数组、int/float/double/long等类型

```java
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;

public class WriteData {
    public static void main(String[] args) {
        File file = new File("test.txt");
        if (file.exists()) {
            System.out.println("File already exists!");
            System.exit(1);
        }
        try (
                PrintWriter printWriter = new PrintWriter(file);
        )
        {
            printWriter.print("John T Smith ");
            printWriter.println("90");
            printWriter.print("Eric K Jones ");
            printWriter.println("85");
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
}
```

注意代码中使用了try-with-resources，将resources放在try后边的括号中。资源必须是AutoCloseable的子类型，具有close方法。

**Scanner**

Scanner类用来从控制台或者文本读取内容。从控制台读取时，我们为System.in传建一个Scanner：

```java
Scanner input = new Scanner(System.in);
```

当我们需要从文件中读取内容时，为文件创建Scanner：

```java
Scanner input = new Scanner(new File(filename));
```

常用方法：

- `close()`：关闭Scanner
- `hasNext()`：如果还有更多数据要读取，返回true
- `next()`：读取下一个标记并作为字符串返回
- `nextLine()`：读取一行，以换行符作为结束
- `nextInt()`：读取一个int值并返回，类似的还有double、byte、long、float和short
- `useDelimiter(String pattern)`：设置Scanner的分隔符，并返回该Scanner

