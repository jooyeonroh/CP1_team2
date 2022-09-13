from operator import itemgetter
import os
import csv
from tqdm import tqdm

## DB insert 가능한 형태로 변형 ##
def ord_unique_list(data_list):
    idx_data_list = []
    data_list.sort() ## (1) 데이터 가,나,다 순으로 정렬 진행
    unique_list = list(dict.fromkeys(data_list)) ## (2) 정렬된 순서를 유지한 채로 중복제거
    
    for i, raw_data in enumerate(unique_list): ## (3) 최종list로 인덱스값을 추가한 list로 변형
        i += 1 # 0부터 시작하는 index값을 1부터 시작하게끔 조정
        idx_data_list.append((i, raw_data))
    
    return idx_data_list

# csv_f = open("./barcode_final.csv" , 'r', encoding='utf-8')
# # 리스트 형식
# f = csv.reader(csv_f)
# next(f)

# # ## 바코드 데이터 수 9717개
# # ## (0)b_category_name, (1)barcode, (2)product_name, (3)company_name, (4)expiry_date
# category_name_list = []
# company_name_list = []

# ## 데이터 저장 ##
# for data in f:
#     category_name_list.append(data[0])
#     company_name_list.append(data[3])

# insert_cate_list = ord_unique_list(category_name_list)
# insert_com_list = ord_unique_list(company_name_list)
# # print(insert_cate_list)
# # print("-----------------------------------------------------------------------------")
# # print(insert_com_list)
# csv_f.close() ## barcode opencsv close




# csv_b = open("./barcode_final.csv" , 'r', encoding='utf-8')
# # 리스트 형식
# f = csv.reader(csv_b)
# next(f)
# barcode_list = []
# for i, data in enumerate(f):
#     temp = []
#     i += 1
#     for j in insert_cate_list: # 참조 category_id 추출
#         if data[0] == j[1]:
#             temp.append(j[0]) # category_id = temp[0]
#     for k in insert_com_list: # 참조 company_id 추출
#         if data[3] == k[1]:
#             temp.append(k[0]) # company_id = temp[1]
#     barcode_list.append((i, data[1], temp[0], temp[1], data[2], int(float(data[4])), int(float(data[5]))))

# print(barcode_list)

############# DB에 넣을 수 있게 데이터 정제 진행상세 과정 #################

# print("정렬 전: ", category_name_list)
# print("정렬 전: ", company_name_list)
# print("------------------------------------------------------------")

# ## 가, 나, 다 순 정렬 ## -> 루틴화 가능
# category_name_list.sort()
# company_name_list.sort()
# print("정렬 후: ", category_name_list)
# print("정렬 후: ", company_name_list)
# print("------------------------------------------------------------")

# ## 정렬 진행 후 중복 제거 진행 -> 루틴화 가능
# category_nlist= list(dict.fromkeys(category_name_list))
# company_nlist= list(dict.fromkeys(company_name_list))

# print("중복 제거 후: ",category_nlist)
# print("중복 제거 후: ",company_nlist)
# print("-----------------------------------------------------------------------")

# final_cate_list = []
# for i, data in enumerate(category_nlist):
#     i += 1
#     final_cate_list.append((i, data))
# print("최종 insert data: ", final_cate_list)
# print("-----------------------------------------------------------------------")

# final_com_list = []
# for i, data in enumerate(company_nlist):
#     i += 1
#     final_com_list.append((i, data))
# print("최종 insert data: ", final_com_list)





# ## recipe csv 데이터 오픈 후 -> 재료만 선 추출
# csv_recipe = open('./raw_preproc_recipe_data.v.0.3.csv', 'r', encoding = 'utf-8')
# file = csv.reader(csv_recipe)
# next(file) # 맨 위의 컬럼명 skip

# i = 0
# ingredient_temp_list = []
# for data in file: # 해당 파일의 데이터가 모두 String값이여서 String데이터 정제 필요!
#     temp = data[8].replace("'",'')
#     temp= temp.replace("[", '')
#     temp=temp.replace("]", '')
#     temp = temp.split(', ')
#     for ingredient in temp:
#         ingredient_temp_list.append(ingredient)
        
# ingredient_list = ord_unique_list(ingredient_temp_list)
# print(ingredient_list)

# print(ingredient_list)
## (0)b_category_name, (1)barcode, (2)product_name, (3)company_name, (4)expiry_date

# ## csv데이터 재오픈
# csv_f = open("./barcode_2차.csv" , 'r')
# # 리스트 형식
# f = csv.reader(csv_f)
# next(f)
# barcode_list = []
# for i, data in enumerate(f):
#     temp = []
#     i += 1
#     for j in insert_cate_list: # 참조 category_id 추출
#         if data[0] == j[1]:
#             temp.append(j[0]) # category_id = temp[0]
#     for k in insert_com_list: # 참조 company_id 추출
#         if data[3] == k[1]:
#             temp.append(k[0]) # company_id = temp[1]
#     barcode_list.append((i, data[1], temp[0], temp[1], data[2], data[4]))

# print("--------------------------------------------------------------------------------")
# print(barcode_list)
# print("--------------------------------------------------------------------------------")


recipe_list = []
recipe_temp_list = []
situation_temp_list = []
recipe_situation_temp_list = []

# (0)recipe_name, (1)views, (2)recommand, (3)scrap, (5)situation_name, (8)recipe_desc, (9)ingredient_name
# (10)cooking_serving (11)level (12)cooking_time

# CREATE TABLE recipes(
#     recipe_id SERIAL PRIMARY KEY,
#     recipe_name VARCHAR(50),
#     recipe_desc TEXT,
#     views INTEGER,
#     recommand INTEGER,
#     scrap INTEGER,
#     cooking_serving INTEGER,
#     level INTEGER,
#     cooking_time INTEGER);
recipe_ingredient_temp_list = []
recipe_ingredient_list = []
csv_recipe = open('./raw_preproc_recipe_data.v.0.3.csv', 'r', encoding = 'utf-8')
file = csv.reader(csv_recipe)
next(file) # 맨 위의 컬럼명 skip


ingredient_temp_list = []
for i, data in enumerate(tqdm(file)): # 해당 파일의 데이터가 모두 String값이여서 String데이터 정제 필요!
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
print(len(recipe_ingredient_list))


# print(len(ingredient_temp_list))
# print(ingredient_temp_list[1])
# with open('./recipe_1차전처리.csv', 'r') as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)
#     for i, r in enumerate(reader):
#         i += 1
#         recipe_temp_list.append((i, r[0], r[8], r[1], r[2], r[3], r[10], r[11], r[12], r[5]))
#     csvfile.close()

# for i in recipe_temp_list:
#     recipe_list.append(i[:-1])
#     situation_temp_list.append(i[-1])

# situation_list = ord_unique_list(situation_temp_list)

# for j in recipe_temp_list:
#     for k in situation_list:
#         if k[1] == j[-1]:
#             recipe_situation_temp_list.append((j[0], k[0]))

# print(recipe_situation_temp_list)
# with open('./recipe_1차전처리.csv', 'r') as csvf:
#     reader = csv.reader(csvf)
#     next(reader)
#     for r in reader:
#         recipe_temp_list.append((r[0], r[8], r[1], r[2], r[3], r[10], r[11], r[12]))
#     csvfile.close()
# stl = situation_temp_list
# situation_list = ord_unique_list(situation_temp_list)

# print("전처리 전: ",stl)
# print("--------------------------------------------------------------")
# print("전처리 후: ",situation_list)

