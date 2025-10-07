import redis

try:
    r = redis.Redis(host="localhost", port=6379)
    print("PING:", r.ping())
except Exception as e:
    print("Error:", e)