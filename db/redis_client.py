import json

import redis


class RedisDB:
    def __init__(
        self,
        host="localhost",
        port=6379,
        db=0,
    ):
        self.host = host
        self.port = port
        self.db = db
        self.connection = None

    def connect(self):
        try:
            self.connection = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
            )
            self.connection.ping()
            print("Connected to Redis successfully!")
        except redis.exceptions.ConnectionError as e:
            print(f"Could not connect to Redis: {e}")

    def set(self, key, value):
        if self.connection:
            self.connection.set(key, value)
        else:
            print("Not connected to Redis.")

    def get(self, key):
        if self.connection:
            return self.connection.get(key)
        else:
            print("Not connected to Redis.")
            return None

    def delete(self, key):
        if self.connection:
            self.connection.delete(key)
        else:
            print("Not connected to Redis.")

    def create_initial_data(self, initial_data):
        if self.connection:
            for key, value in initial_data.items():
                self.connection.set(key, json.dumps(value))
            print("Initial data created successfully.")
        else:
            print("Not connected to Redis.")


if __name__ == "__main__":
    redis_db = RedisDB()
    redis_db.connect()
    redis_db.set(
        "user_tenant1", json.dumps({"tenant_id": "101", "password": "pass101"})
    )
    value = redis_db.get("user_tenant1")
    print(f"Retrieved value: {value}")
    redis_db.delete("user_tenant1")
    value = redis_db.get("user_tenant1")
    print(f"Retrieved value after deletion: {value}")
