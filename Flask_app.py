from sys import version
from flask import Flask, request, jsonify, render_template
import webbrowser
import json
import protos.group_pb2 as gpb
import socket
import threading
from Redis_server import *

def get_timestamp():
    """获取时间戳以标识用户ID和工作组Group ID，时间戳从2024年7月1日开始，UTC+8，精确到0.1s"""
    return int(time.time() * 10) - 17197632000

class User:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class Group:
    def __init__(self, group_id, group_name, user):
        self.group_id = group_id
        self.group_name = group_name
        self.member = [user]
        self.member_id = [user.id]
        self.version = {user.id: 0}
        self.document = {user.id: ""}

    def accept_new_member(self, user):
        self.member.append(user)
        self.member_id.append(user.id)
        self.version.update({user.id: 0})
        self.document.update({user.id: ""})

    def update_document(self, user, new_version, new_document):
        if self.version[user.id] < new_version:
            self.version[user.id] = new_version
            self.document[user.id] = new_document

    def to_gpb(self):
        """将Group对象以protobuf3的形式编码成序列，方便Redis存储和gRPC发送"""
        group_message = gpb.Group(
            group_id=self.group_id,
            group_name=self.group_name,
        )
        for user in self.member:
            user_message = gpb.User(name=user.name, id=user.id)
            group_message.members.append(user_message)
        for user_id, version in self.version.items():
            group_message.version[user_id] = version
        for user_id, document in self.document.items():
            group_message.document[user_id] = document
        return group_message.SerializeToString()

    @classmethod
    def from_gpb(cls, serialized_data):
        """将protobuf3编码的序列转换成Group对象，方便Redis读取和gRPC接收"""
        group_message = gpb.Group.FromString(serialized_data)
        initial_user = group_message.members[0]
        group = cls(group_message.group_id, group_message.group_name, User(initial_user.name, initial_user.id))
        group.member = [User(user.name, user.id) for user in group_message.members]
        group.member_id = [user.id for user in group_message.members]
        group.version = dict(group_message.version)
        group.document = dict(group_message.document)
        return group

class Flask_app:
    def __init__(self):
        self.app = Flask(__name__, template_folder="web_pages", static_folder="web_pages/source")
        try:
            self.r = redis.Redis(host='localhost', port=6379, db=0)
            self.r.ping()
        except redis.exceptions.ConnectionError:
            print("Error: Check if Redis server is running.")
            exit(0)

        @self.app.route('/')
        def index():
            if self.r.exists('user_name') and self.r.exists('user_id'):
                # 获取用户信息
                user_name = self.r.get('user_name').decode('utf-8')
                user_id = eval(self.r.get('user_id').decode('utf-8'))
                self.user = User(user_name, user_id)

                print(f"Logged in as \"{user_name}\" with user ID \"{user_id}\"")
                return render_template('index.html', user_info=self.user)
            else:
                return render_template('sign_up.html')

        # 注册信息提交
        @self.app.route('/sign_up_submit', methods=['POST'])
        def sign_up_submit():
            data = request.get_json()
            user_name = data.get('user_name')
            user_id = get_timestamp()
            self.r.set('user_name', user_name)
            self.r.set('user_id', user_id)
            self.r.save()
            print(f"Signed up as {user_name} with user ID {user_id}")
            return jsonify({'user_name': user_name})

        # 文档提交
        @self.app.route('/document_submit', methods=['POST'])
        def document_submit():
            data = request.get_json()
            group_id = data.get('group_id')
            user_id = data.get('user_id')
            text = data.get('text')
            group_temp = Group.from_gpb(self.r.get(group_id))
            version_temp = group_temp.version[user_id]
            group_temp.version.update({user_id: version_temp + 1})
            group_temp.document.update({user_id: text})
            self.r.set(group_id, group_temp.to_gpb())
            self.r.save()
            return jsonify({'version': version_temp+1})

        # 获取当前用户工作组
        @self.app.route('/get_groups', methods=['GET'])
        def get_groups():
            group_ids = [int(i) for i in self.r.lrange('group_list', 0, -1)]
            groups = [Group.from_gpb(self.r.get(group_id)) for group_id in group_ids]
            group_names = [g.group_name for g in groups]
            group_ids = [g.group_id for g in groups]
            return jsonify({'group_names': group_names, 'group_ids': group_ids})

        # 获取group_id对应的用户信息
        @self.app.route('/get_users', methods=['POST'])
        def get_users():
            data = request.get_json()
            group_id = data.get('group_id')
            group_temp = Group.from_gpb(self.r.get(group_id))
            user_ids = group_temp.member_id
            user_names = [u.name for u in group_temp.member]
            return jsonify({'user_names': user_names, 'user_ids': user_ids})
        
        # 获取group_id、user_id对应的文档
        @self.app.route('/get_document', methods=['POST'])
        def get_document():
            data = request.get_json()
            group_id = data.get('group_id')
            user_id = data.get('user_id')
            group_temp = Group.from_gpb(self.r.get(group_id))
            text = group_temp.document[user_id]
            return jsonify({'text': text})

        @self.app.route('/create_group', methods=['POST'])
        def create_group():
            data = request.get_json()
            group_name = data.get('group_name')
            group_id = get_timestamp()
            self.r.rpush('group_list', group_id)
            new_group = Group(group_id, group_name, self.user)
            self.r.set(group_id, new_group.to_gpb())
            self.r.save()
            print(f"Create group {group_name} with group ID {group_id}")
            return jsonify({'group_id': group_id})
        
        @self.app.route('/broadcast', methods=['POST'])
        def broadcast():
            data = request.get_json()
            user_id = data.get('user_id')
            group_id = data.get('group_id')
            # UDP广播，端口号50000，期待回复IP地址
            message = json.dumps({'user_id': user_id, 'group_id': group_id}).encode('utf-8')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(5)
            sock.sendto(message, ('<broadcast>', 50000))
            try:
                response, addr = sock.recvfrom(1024)
                response_data = json.loads(response.decode('utf-8'))
                print(f"Received response from {addr}: {response_data}")
                return jsonify(response_data)
            except socket.timeout:
                print("Broadcast timeout: no response received")
                return jsonify({'error': 'No response received'}), 504

    # 监听广播
    def listen_for_broadcast(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 50000))
        while True:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode('utf-8'))
            user_id = message['user_id']
            group_id = message['group_id']
            if self.r.exists('user_id') and self.r.exists('group_list'):
                current_user_id = self.r.get('user_id').decode('utf-8')
                current_group_ids = [int(i) for i in self.r.lrange('group_list', 0, -1)]
                if current_user_id == user_id and group_id in current_group_ids:
                    response = {
                        'ip': addr[0],
                        'port': addr[1]
                    }
                    response_message = json.dumps(response).encode('utf-8')
                    sock.sendto(response_message, addr)
    
    def run(self):
        url = "http://127.0.0.1:5000/"
        webbrowser.open_new(url)
        flask_thread = threading.Thread(target=self.app.run, kwargs={'threaded': True})
        flask_thread.start()
        broadcast_thread = threading.Thread(target=self.listen_for_broadcast)
        broadcast_thread.start()

if __name__ == "__main__":
    rs = Redis_server()
    rs.run()
    fa = Flask_app()
    fa.run()