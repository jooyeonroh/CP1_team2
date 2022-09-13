import os
import psycopg2
from pymongo import MongoClient
from dotenv import load_dotenv

def mongoconn_barcode():
    ## NoSQL DB세팅 ## 
    # -> 데이터가 API를 통해서 대량으로 가져오다보니, 가공해서 적재를 할 수 없음 #

    load_dotenv() # take enviroment variables from .env

    ## MongoDB 적재할 계정정보 입력 ##
    HOST = os.environ.get('MONGO_HOST')
    USER = os.environ.get('MONGO_USER')
    PASSWORD = os.environ.get('MONGO_PASSWORD')
    DATABASE_NAME = os.environ.get('MONGO_DATABASE_NAME')
    COLLECTION_NAME = 'Barcode_API'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    ## 계정 접속 ##
    client = MongoClient(MONGO_URI)
    coll = client[DATABASE_NAME][COLLECTION_NAME]

    return coll

def mongoconn_classify():
    ## NoSQL DB세팅 ## 
    
    load_dotenv() # take enviroment variables from .env

    ## MongoDB 적재할 계정정보 입력 ##
    HOST = os.environ.get('MONGO_HOST')
    USER = os.environ.get('MONGO_USER')
    PASSWORD = os.environ.get('MONGO_PASSWORD')
    DATABASE_NAME = os.environ.get('MONGO_DATABASE_NAME')
    COLLECTION_NAME = 'Classfy_API'
    MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"

    ## 계정 접속 ##
    client = MongoClient(MONGO_URI)
    coll = client[DATABASE_NAME][COLLECTION_NAME]

    return coll

def postgreconn():

    load_dotenv() # take enviroment variables from .env

    ## 가공된 데이터 RDBMS 적재 ##
    host = os.environ.get('GRE_HOST')
    user = os.environ.get('GRE_USER')
    password = os.environ.get('GRE_PASSWORD')
    database = os.environ.get('GRE_DATABASE')

    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cur = connection.cursor()

    return connection, cur
