
# from redis.client import Redis
import random
# import zlib
from retry import retry
from datetime import datetime
# from redis.commands.json.path import Path
import json

class Cache:
   
   def __init__(self, logger, doc, RedisHanlderInject):
      self.time_to_expire_s=180
      self.client = RedisHanlderInject
      self.logger = logger
      self.doc = doc
      self.REQEUST_INFO = {
            "KEY" : None,
            "REQUEST_USER_ID": "pd292816",
            "OBJECT_V" : None,
            "INPUT_DATE" : None
        }
      
   
   async def transform_to_pydantic_with_gap(self, all_datas):
      reset_all_datas = {}
      results = []
      for k, v in all_datas.items():
         print('#$%$', k, v)
         # reset_all_datas = v
         delta = datetime.now() - datetime.strptime(all_datas.get(k)['INPUT_DATE'], "%Y-%m-%d %H:%M:%S")
         v.update({"KEY" :  k, "EXPIRED_SECONDS" : float(delta.seconds/60)})  
         results.append(v) 
      return results
      
   @retry(ConnectionResetError, delay=0.1, tries=5)
   def set_key(self, key, value):
    #   self.client.set(key, zlib.compress(value.encode('utf-8')), ex=self.time_to_expire_s)
      self.client.set(key, value, ex=self.time_to_expire_s)
      
   @retry(ConnectionResetError, delay=0.1, tries=5)
   def set_json_key(self, key, value):
      self.REQEUST_INFO.update({"OBJECT_V": value, 'INPUT_DATE' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
      obj = json.dumps(self.REQEUST_INFO, ensure_ascii=False).encode('utf-8')
      self.client.set(key, obj, ex=self.time_to_expire_s)
      
   @retry(ConnectionResetError, delay=0.1, tries=5)
   async def get_json_key(self, key):
      print('$#$', self.client.get(key))
      # return json.dumps(self.client.get(key), ensure_ascii=False)
      return self.client.get(key)
      
   @retry(ConnectionResetError, delay=0.1, tries=5)   
   async def get_key(self, key):
      return self.client.get(key)
  
   @retry(ConnectionResetError, delay=0.1, tries=5)
   async def get_keys_all(self):
      return self.client.keys()
   
   @retry(ConnectionResetError, delay=0.1, tries=5)
   def delete_key(self, key):
      return self.client.delete(key)

   async def get_transformed_dict(self, lookup=None):
      '''
      transforming to json like
       [
         {
            "EXPIRED_SECONDS": 0.95,
            "INPUT_DATE": "2023-10-14 03:02:01",
            "KEY": "1234",
            "OBJECT_V": "1234",
            "REQUEST_USER_ID": "pd292816"
         },
         {
            "EXPIRED_SECONDS": 0.26666666666666666,
            "INPUT_DATE": "2023-10-14 03:02:42",
            "KEY": "1",
            "OBJECT_V": "1",
            "REQUEST_USER_ID": "pd292816"
         }
      ]
      '''
      if lookup:
         all_datas = {k : dict(json.loads(await self.get_json_key(k))) for k in await self.get_keys_all() if k == lookup}
      else:
         all_datas = {k : dict(json.loads(await self.get_json_key(k))) for k in await self.get_keys_all()}
         
      # Update the gap time for each cache values
      all_datas = await self.transform_to_pydantic_with_gap(all_datas)
      return all_datas
