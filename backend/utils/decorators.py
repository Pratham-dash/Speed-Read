import time
from functools import wraps
from flask import jsonify


def timing_metric(name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
            return result, {"metric": name, "elapsed_ms": elapsed_ms}

        return wrapper

    return decorator


def require_json_keys(*required_keys: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            from flask import request

            payload = request.get_json(silent=True) or {}
            missing = [key for key in required_keys if not payload.get(key)]
            if missing:
                return jsonify({"error": "Missing required fields", "missing": missing}), 400
            return func(*args, **kwargs)

        return wrapper

    return decorator
