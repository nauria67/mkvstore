from flask import Flask

from core.auth.controller import blueprint as auth_blueprint
from db.redis_client import RedisDB

app = Flask(__name__)
app.register_blueprint(auth_blueprint, url_prefix="/auth")

if __name__ == "__main__":
    redis_db = RedisDB()

    # Preload tenant data
    initial_data = {
        "user_tenant1": {"tenant_id": "101", "password": "pass101"},
        "user_tenant2": {"tenant_id": "202", "password": "pass202"},
        "user_tenant3": {"tenant_id": "303", "password": "pass303"},
    }
    redis_db.create_initial_data(initial_data)

    app.run(debug=True)
