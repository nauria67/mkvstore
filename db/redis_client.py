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


if __name__ == "__main__":
    redis_db = RedisDB()
    redis_db.connect()
    redis_db.set("example_key", "example_value")
    value = redis_db.get("example_key")
    print(f"Retrieved value: {value}")
    redis_db.delete("example_key")
    value = redis_db.get("example_key")
    print(f"Retrieved value after deletion: {value}")
