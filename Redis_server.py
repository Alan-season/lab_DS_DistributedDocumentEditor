import os
import subprocess
import time
import redis
import atexit

class Redis_server:
    """Redis服务器，使用run方法启动"""
    def __init__(self):
        self.redis_process = None

    def _start_redis_server(self):
        """启动Redis服务器"""
        redis_server_path = os.path.join(os.path.dirname(__file__), 'redis', 'redis-server.exe')
        redis_conf_path = os.path.join(os.path.dirname(__file__), 'redis', 'redis.conf')
        self.redis_process = subprocess.Popen([redis_server_path, redis_conf_path])
        time.sleep(1)  # 等待Redis服务器启动，降低连接失败或者连接超时的风险

    def _check_redis_connection(self):
        """检查Redis服务器是否启动"""
        for _ in range(10):
            try:
                r = redis.Redis(host='localhost', port=6379, db=0)
                r.ping()
                r.close()
                return True
            except redis.exceptions.ConnectionError:
                time.sleep(1)
        return False

    def _stop_redis_server(self):
        """关闭Redis服务器"""
        if self.redis_process:
            self.redis_process.terminate()
            self.redis_process.wait()
    
    def show_database(self):
        """显示数据库中存储的数据"""
        r = redis.Redis(host='localhost', port=6379, db=0)
        print("All data in database:")
        keys = r.keys('*')
        for key in keys:
            value = r.get(key)
            print(f'{key.decode("utf-8")}: {value.decode("utf-8")}')
        r.close()

    def run(self):
        """启动Redis服务器并检查连接"""
        print("Trying to start Redis server...")
        self._start_redis_server()
        atexit.register(self._stop_redis_server)
        if self._check_redis_connection():
            print("Redis server started successfully.")
        else:
            print("Failed to start Redis server.")
            return

if __name__ == "__main__":
    rs = Redis_server()
    rs.run()
    rs.show_database()