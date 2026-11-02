"""
Database connection module with intentional bugs
"""
bgguugg
class DatabaseConnection:
    def __init__(self, host, port):
        # BUG #1: Missing null check on host
        self.host = host  # Can be None
        self.port = port
        self.connection = None
    
    def connect(self):
        # BUG #2: NoneType has no attribute 'split'
        # This will crash if self.host is None
        host_parts = self.host.split(':')  # TypeError if host is None
        return f"Connected to {host_parts[0]}"
    
    def query(self, sql):
        # BUG #3: Connection not checked before use
        # This will crash if connection is None
        result = self.connection.execute(sql)  # AttributeError
        return result
    
    def close(self):
        # BUG #4: Resource leak - connection never properly closed
        del self.connection  # This is not proper cleanup


class UserService:
    def __init__(self):
        self.db = DatabaseConnection(None, 5432)  # Passing None causes errors
    
    def get_user(self, user_id):
        # This will trigger BUG #2
        conn_str = self.db.connect()
        
        # BUG #5: SQL injection vulnerability (also causes errors)
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return self.db.query(query)
    
    def update_user(self, user_id, data):
        # BUG #6: Missing error handling
        # Any exception here will crash the application
        self.db.query(f"UPDATE users SET {data} WHERE id = {user_id}")


class CacheService:
    def __init__(self):
        self.cache = {}
        self.max_size = 1000
    
    def set(self, key, value):
        # BUG #7: Memory leak - no cache eviction
        # Cache grows indefinitely, causing memory errors
        self.cache[key] = value
        if len(self.cache) > self.max_size:
            # This is never executed because of logic error
            pass
    
    def get(self, key):
        # BUG #8: KeyError not handled
        # Missing key will crash the application
        return self.cache[key]  # No default or try/except


class APIHandler:
    def __init__(self):
        self.user_service = UserService()
        self.cache = CacheService()
    
    def handle_request(self, request):
        # BUG #9: Blocking operation in main thread
        # No timeout, can hang indefinitely
        user = self.user_service.get_user(request.get('user_id'))
        
        # BUG #10: Race condition in cache
        # Concurrent access without locks
        self.cache.set(f"user_{request.get('user_id')}", user)
        return user


# This code will generate the following errors:
# TypeError: expected string or bytes-like object
# AttributeError: 'NoneType' object has no attribute 'execute'
# KeyError: missing keys
# MemoryError: cache grows unbounded
# RecursionError: potential infinite loops
