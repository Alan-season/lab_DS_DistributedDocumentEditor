"""
软件分为两个部分：客户端和服务器

数据存储：
将用户数据存储在文件夹user下。
用一个user_info.txt文件存储用户的编号user_id和用户名user_name。
一个用户有很多个工作组，工作组有对应的group_id，将工作组的相关信息存储在group_id同名的文件夹下。
每个工作组文件夹中存储唯一对应的文件document.txt，此外，将该工作组的成员的user_id存储在member.txt中

举例说明：
user/
├── user_info.txt
├── group_001/      # 假设group_id == 001
│   ├── document.txt
│   └── member.txt
├── group_002/      # 假设group_id == 002
│   ├── document.txt
│   └── member.txt
...

class Group:
self.group_id: int
self.group_name: str
self.member: [int]
self.version: [int]
self.document: {int:str}




"""

查看占用指定端口的进程：
```cmd
netstat -ano | findstr :端口号
```

查看进程的详细信息：
```cmd
tasklist | findstr 进程ID
```