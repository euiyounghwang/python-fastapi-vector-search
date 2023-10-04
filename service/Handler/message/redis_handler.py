
# from redis.client import Redis
import random
# import zlib
from retry import retry

class Cache:
   
   def __init__(self, logger, doc, RedisHanlderInject):
      self.time_to_expire_s=180
      self.client = RedisHanlderInject
      self.logger = logger
      self.doc = doc
      
   @retry(ConnectionResetError, delay=0.1, tries=5)
   def set_key(self, key, value):
    #   self.client.set(key, zlib.compress(value.encode('utf-8')), ex=self.time_to_expire_s)
      self.client.set(key, value, ex=self.time_to_expire_s)
   
   @retry(ConnectionResetError, delay=0.1, tries=5)   
   def get_key(self, key):
      return self.client.get(key)
  
   @retry(ConnectionResetError, delay=0.1, tries=5)
   def get_keys_all(self):
      return self.client.keys()
   
   @retry(ConnectionResetError, delay=0.1, tries=5)
   def delete_key(self, key):
      return self.client.delete(key)

