
JAVA多线程实现方式主要有三种：继承Thread类、实现Runnable接口、使用ExecutorService、Callable、Future实现有返回结果的多线程。

其实Thread中的run方法调用的是Runnable接口的run方法。

# 直接继承Thread的类

```java
class hello extends Thread {
 
    public hello() {
 
    }
 
    public hello(String name) {
        this.name = name;
    }
 
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(name + "运行     " + i);
        }
    }
 
    public static void main(String[] args) {
        hello h1=new hello("A");
        hello h2=new hello("B");
        h1.start();
        h2.start();
    }
 
    private String name;
}
```

# 通过实现Runnable接口

```java
class hello implements Runnable {
 
    public hello() {
 
    }
 
    public hello(String name) {
        this.name = name;
    }
 
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(name + "运行     " + i);
        }
    }
 
    public static void main(String[] args) {
        hello h1=new hello("线程A");
        Thread demo= new Thread(h1);
        hello h2=new hello("线程Ｂ");
        Thread demo1=new Thread(h2);
        demo.start();
        demo1.start();
    }
 
    private String name;
}
```

# Thread和Runnable的区别

如果一个类继承Thread，则不适合资源共享。但是如果实现了Runable接口的话，则很容易的实现资源共享。

```java
class hello extends Thread {
    public void run() {
        for (int i = 0; i < 4; i++) {
            if (count > 0) {
                System.out.println("count= " + count--);
            }
        }
    }
 
    public static void main(String[] args) {
        hello h1 = new hello();
        hello h2 = new hello();
        h1.start();
        h2.start();
    }
 
    private int count = 2;
}
```

【运行结果】：

count= 2

count= 1

count= 2

count= 1

```java
class MyThread implements Runnable{
 
    private int ticket = 5;  //5张票
 
    public void run() {
        for (int i=0; i<=20; i++) {
            if (this.ticket > 0) {
                System.out.println(Thread.currentThread().getName()+ "正在卖票"+this.ticket--);
            }
        }
    }
}
public class lzwCode {
     
    public static void main(String [] args) {
        MyThread my = new MyThread();
        new Thread(my, "1号窗口").start();
        new Thread(my, "2号窗口").start();
        new Thread(my, "3号窗口").start();
    }
}
```

【运行结果】：

1号窗口正在卖票5

1号窗口正在卖票4

2号窗口正在卖票3

3号窗口正在卖票1

1号窗口正在卖票2


实现Runnable接口比继承Thread类所具有的优势：

1.适合多个相同的程序代码的线程去处理同一个资源

2.可以避免java中的单继承的限制

3.增加程序的健壮性，代码可以被多个线程共享，代码和数据独立。