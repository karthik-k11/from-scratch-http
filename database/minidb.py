class MiniDB:

    def __init__(self):
        self.store = {}

    def insert(self, key, value):
        self.store[key] = value
        return True

    def select(self, key):
        return self.store.get(key, None)

    def stats(self):
        return {
            "total_keys": len(self.store)
        }