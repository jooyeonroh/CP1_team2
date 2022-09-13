import requests
import json
import os
import time
from pymongo import MongoClient
from database_connection import mongoconn_classify ## 모듈에 생성해놨음
from dotenv import load_dotenv

## NoSQL DB세팅 ## 
# -> 데이터가 API를 통해서 대량으로 가져오다보니, 가공해서 적재를 할 수 없음 #

load_dotenv() # take enviroment variables from .env

## MongoDB 적재할 계정정보 입력

coll = mongoconn_classify()

endIndex = 0
keyId = os.environ.get('CLASSIFY_SECOND_KEY')
    
for startIndex in range(1, 100000, 1000):
    startIndex
    endIndex += 1000

    print('startIndex: ',startIndex)
    print('endIndex: ',endIndex)

#     ## API호출 ##
    c_code_URL = f'http://openapi.foodsafetykorea.go.kr/api/{keyId}/I2570/json/{startIndex}/{endIndex}'
    response = requests.get(c_code_URL)
    print(response)
    c_data = json.loads(response.content)
    print(c_data)   
    coll.insert_one(c_data) ## MongoDB 데이터 적재
    time.sleep(1)