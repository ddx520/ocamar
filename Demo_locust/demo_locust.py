import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")


    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})

if __name__ == '__main__':
    import os
    os.system("locust -f demo_locust.py --host=http://10.10.5.21:8085/cccsp/static/index.html#/userManagement")