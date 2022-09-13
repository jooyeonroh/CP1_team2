import psycopg2
import csv

from database_connection import mongoconn_barcode, mongoconn_classify, postgreconn

conn, cur = postgreconn()


#################### 테이블 삭제 관련 코드이기 떄문에 한번 돌리고 나서 주석처리 꼭꼭꼭!!!###################
## barcode 테이블 삭제 관련 ##

## 외래키 제약이 붙어있을 때는 제약키를 삭제해야 TABLE을 정상 삭제 가능
cur.execute("""ALTER TABLE barcode
               DROP CONSTRAINT barcode_b_category_id_fkey;""")
cur.execute("""ALTER TABLE barcode
               DROP CONSTRAINT barcode_company_id_fkey;""")
cur.execute("DROP TABLE IF EXISTS barcode;")

cur.execute("DROP TABLE IF EXISTS barcode_categories;")
cur.execute("DROP TABLE IF EXISTS barcode_companies;")



## recipe 테이블 삭제 관련 ##
# 외래키 제약이 붙어있을 때는 제약키를 삭제해야 TABLE을 정상 삭제 가능
cur.execute("""ALTER TABLE recipe_situation
               DROP CONSTRAINT recipe_situation_recipe_id_fkey;""")
cur.execute("""ALTER TABLE recipe_situation
               DROP CONSTRAINT recipe_situation_situation_id_fkey;""")
cur.execute("DROP TABLE IF EXISTS recipe_situation;")

cur.execute("""ALTER TABLE recipe_ingredient
               DROP CONSTRAINT recipe_ingredient_recipe_id_fkey""")
cur.execute("""ALTER TABLE recipe_ingredient
               DROP CONSTRAINT recipe_ingredient_ingredient_id_fkey""")
cur.execute("DROP TABLE IF EXISTS recipe_ingredient;")

cur.execute("DROP TABLE IF EXISTS ingredient;")
cur.execute("DROP TABLE IF EXISTS situation;")
cur.execute("DROP TABLE IF EXISTS recipes;")
conn.commit()


############################# 테이블 생성 관련 코드 #############################3
## barcode 테이블 생성 ##
cur.execute("""
    CREATE TABLE barcode_categories(
        b_category_id SERIAL PRIMARY KEY,
        b_category_name VARCHAR(20));""")

cur.execute("""
    CREATE TABLE barcode_companies(
        company_id SERIAL PRIMARY KEY,
        company_name VARCHAR(50));""")

cur.execute("""
    CREATE TABLE ingredient(
        ingredient_id SERIAL PRIMARY KEY,
        ingredient_name VARCHAR(20));""")


cur.execute("""
    CREATE TABLE barcode(
        barcode_id SERIAL PRIMARY KEY,
        barcode VARCHAR(13),
        b_category_id INTEGER,
        company_id INTEGER,
        product_name VARCHAR(100),
        shelf_life INTEGER,
        expiry_date INTEGER,
        FOREIGN KEY (b_category_id) REFERENCES barcode_categories(b_category_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (company_id) REFERENCES barcode_companies(company_id) ON DELETE CASCADE ON UPDATE CASCADE);""")

## recipe 관련 테이블 생성 ##
cur.execute("""
    CREATE TABLE recipes(
        recipe_id SERIAL PRIMARY KEY,
        recipe_name VARCHAR(50),
        recipe_desc TEXT,
        views INTEGER,
        recommand INTEGER,
        scrap INTEGER,
        cooking_serving INTEGER,
        level INTEGER,
        cooking_time INTEGER);""")

cur.execute("""
    CREATE TABLE recipe_ingredient(
        id SERIAL PRIMARY KEY,
        recipe_id INTEGER,
        ingredient_id INTEGER,
        FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ingredient_id) REFERENCES ingredient(ingredient_id) ON DELETE CASCADE ON UPDATE CASCADE);""")

cur.execute("""
    CREATE TABLE situation(
        situation_id INTEGER PRIMARY KEY,
        situation_name VARCHAR(20));""")

cur.execute("""
    CREATE TABLE recipe_situation(
        recipe_id SERIAL PRIMARY KEY,
        situation_id INTEGER,
        FOREIGN KEY (situation_id) REFERENCES situation(situation_id) ON DELETE CASCADE ON UPDATE CASCADE);""")
                                                                                                      
conn.commit() ## table 생성에 대한 COMMIT
# conn.close() ## 연결 이후 데이터베이스 구동 완료 후 close 꼭!!!


#################### 데이터베이스 INSERT 작업 페이지 ############################
#################### (1) INSERT작업 위해 데이터 형식 변형 #######################

## DB insert 가능한 형태로 변형 ##
## (1) 가, 나, 다 순으로 정렬 , (2) 정렬된 순서 유지하면서 중복제거, (3) 인덱스 추가 후 튜플형태로 묶어 리스트에 저장 ##
def ord_unique_list(data_list):
    idx_data_list = []
    data_list.sort() ## (1) 데이터 가,나,다 순으로 정렬 진행
    unique_list = list(dict.fromkeys(data_list)) ## (2) 정렬된 순서를 유지한 채로 중복제거
    
    for i, raw_data in enumerate(unique_list): ## (3) 최종list로 인덱스값을 추가한 list로 변형
        i += 1 # 0부터 시작하는 index값을 1부터 시작하게끔 조정
        idx_data_list.append((i, raw_data))
    
    return idx_data_list


#################### barcode_category, barcode_company 데이터 추출 #######################
csv_f = open("./barcode_final.csv" , 'r', encoding='utf-8')
# 리스트 형식
f = csv.reader(csv_f)
next(f)

## 바코드 데이터 수 9717개
## (0)b_category_name, (1)barcode, (2)product_name, (3)company_name, (4)expiry_date
category_name_list = []
company_name_list = []

## 데이터 저장 ##
for data in f:
    category_name_list.append(data[0])
    company_name_list.append(data[3])

insert_cate_list = ord_unique_list(category_name_list)
insert_com_list = ord_unique_list(company_name_list)
csv_f.close() ## barcode opencsv close


################### barcode 데이터 추출 #######################
csv_b = open("./barcode_final.csv" , 'r', encoding='utf-8')
# 리스트 형식
f = csv.reader(csv_b)
next(f)
barcode_list = []
for i, data in enumerate(f):
    temp = []
    i += 1
    for j in insert_cate_list: # 참조 category_id 추출
        if data[0] == j[1]:
            temp.append(j[0]) # category_id = temp[0]
    for k in insert_com_list: # 참조 company_id 추출
        if data[3] == k[1]:
            temp.append(k[0]) # company_id = temp[1]
    barcode_list.append((i, data[1], temp[0], temp[1], data[2], int(float(data[4])), int(float(data[5]))))


############# ingredient 테이블 데이터  선 추출 ################
csv_recipe = open('./raw_preproc_recipe_data.v.0.3.csv', 'r', encoding = 'utf-8')
file = csv.reader(csv_recipe)
next(file) # 맨 위의 컬럼명 skip

recipe_ingredient_temp_list = []
recipe_ingredient_list = []
ingredient_temp_list = []
for i, data in enumerate(file): # 해당 파일의 데이터가 모두 String값이여서 String데이터 정제 필요!
    i += 1
    temp = data[8].replace("'",'')
    temp= temp.replace("[", '')
    temp=temp.replace("]", '')
    temp = temp.split(', ')
    for ingredient in temp:
        ingredient_temp_list.append(ingredient)
        recipe_ingredient_temp_list.append((i,ingredient))
csv_recipe.close()

ingredient_list = ord_unique_list(ingredient_temp_list)



for j in recipe_ingredient_temp_list:
    for k in ingredient_list:
        if j[1] == k[1]:
            recipe_ingredient_list.append((j[0], k[0]))

############# recipes, situation, recipe_situation 테이블 데이터  선 추출 ################

recipe_list = []
recipe_temp_list = []
situation_temp_list = []
recipe_situation_temp_list = []

with open('./recipe_1차전처리.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for i, r in enumerate(reader):
        i += 1
        recipe_temp_list.append((i, r[0], r[8], r[1], r[2], r[3], r[10], r[11], r[12], r[5]))
    csvfile.close()

for i in recipe_temp_list:
    recipe_list.append(i[:-1]) # recipes 데이터 최종추출
    situation_temp_list.append(i[-1]) # situation 원본 데이터 추출

situation_list = ord_unique_list(situation_temp_list) # situation 최종 가공 데이터 추출

for j in recipe_temp_list:
    for k in situation_list:
        if k[1] == j[-1]:
            recipe_situation_temp_list.append((j[0], k[0])) # recipe_situation 최종 가공 데이터 추출


#################### (2) INSERT작업  #######################
conn, cur = postgreconn()

## (1) barcode_categories테이블 데이터 삽입 ##
for category in insert_cate_list: 
    cur.execute("INSERT INTO barcode_categories(b_category_id, b_category_name)VALUES (%s, %s);", category)

## (2) barcode_companies 테이블 데이터 삽입 ##
for company in insert_com_list:
    cur.execute("INSERT INTO barcode_companies(company_id, company_name)VALUES (%s, %s);", company)

## (3) barcode 테이블 데이터 삽입 ##
for barcode in barcode_list:
    cur.execute("""INSERT INTO barcode (barcode_id, barcode, b_category_id, company_id, product_name, shelf_life, expiry_date)
                 VALUES(%s, %s, %s, %s, %s, %s, %s)""", barcode)

## (4) ingredient 테이블 데이터 삽입 ##
for ingredient in ingredient_list:
    cur.execute("INSERT INTO ingredient(ingredient_id, ingredient_name) VALUES (%s, %s);", ingredient)

# (5) recipes 테이블 데이터 삽입 ##
for recipe in recipe_list:
    cur.execute("INSERT INTO recipes VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);", recipe)

## (6) situation 테이블 데이터 삽입 ##
for situation in situation_list:
    cur.execute("INSERT INTO situation VALUES(%s, %s);", situation)

## (7) recipe_situation 테이블 데이터 삽입 ##
for rs in recipe_situation_temp_list:
    cur.execute("INSERT INTO recipe_situation VALUES(%s, %s);", rs)

## (8) recipe_ingredient 테이블 데이터 삽입 ##
for i, ri in enumerate(recipe_ingredient_list):
    i += 1
    cur.execute(f"INSERT INTO recipe_ingredient VALUES({i}, {ri[0]}, {ri[1]});")
    conn.commit()

conn.commit()

conn.close()

