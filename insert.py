import pymysql
import json
import random
import menu
# JSON 데이터
file_names = ['ribbon0.json','ribbon1.json','ribbon2.json']
data = []

for file_name in file_names:
    with open(file_name, 'r', encoding='utf-8') as file:
        data.extend(json.load(file))  # 각 JSON 파일의 내용을 리스트로 병합

# MySQL 연결 설정
db = pymysql.connect(
    host='3.38.214.167',
    user='root',  # MySQL 사용자 이름
    password='ori6006',  # MySQL 비밀번호
    database='WaitMate',
    charset='utf8mb4'
)

try:
    with db.cursor() as cursor:
        sql="ALTER TABLE restaurant CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        sql10="ALTER TABLE restaurant_info CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        sql11=" ALTER TABLE restaurant_menu CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cursor.execute(sql)
        db.commit()
        cursor.execute(sql10)
        db.commit()
        cursor.execute(sql11)
        db.commit()
        for entry in data:
            try:
                if entry['rest_name'] == "null" or entry['image_url'] == "null":
                    continue
                if entry['rest_name'] is None or entry['image_url'] is None:
                    continue

                # 첫 번째 INSERT 쿼리 실행
                sql1 = """
                INSERT INTO login (email, password, type)
                VALUES ('example@example.com', '1111', 'RESTAURANT');
                """
                cursor.execute(sql1)
                db.commit()
                login_id = cursor.lastrowid

                # 두 번째 INSERT 쿼리 실행
                sql2 = """
                INSERT INTO restaurant (rest_id, rest_name, rest_owner, rest_phone, rest_photo, rest_data, rest_num, is_blocked, join_date, quit_date, rest_status, rest_isopen, rest_account) 
                VALUES (%s, %s, '김식당주인', '01012345678', %s,'사업자등록증', '1231212345', false, '2024-07-10', NULL, %s, true, '신한 123-5233-234-234');
                """
                cursor.execute(sql2, (login_id, entry['rest_name'], entry['image_url'], random.choice(['A', 'B', 'C'])))
                db.commit()

                # 세 번째 INSERT 쿼리 실행
                sql3 = """
                INSERT INTO restaurant_info (rest_id, key_id,key_id2,key_id3, rest_deposit, rest_deposit_method,
                                             rest_address, rest_intro, rest_phone, rest_reserveopen_rule, rest_reserve_interval,
                                             rest_grade, max_ppl, rest_tablenum, rest_post, rev_wait, rest_waiting_status)

                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql3, (
                    login_id,
                    random.randint(1,8),
                    random.randint(1,8),
                    random.randint(1,8),
                    random.choice([0, 20000, 30000]),
                    random.choice(["A", "B"]),
                    entry['rest_address'],
                    entry['feature'],
                    entry['rest_phone'],
                    random.choice(['WEEK', 'MONTH']),
                    random.choice(['ONEHOUR', 'HALFHOUR']),
                    round(random.uniform(2, 5), 1),
                    random.randint(10, 40),
                    random.randint(5, 20),
                    entry['find_path'],
                    random.choice(["A", "B"]),
                    random.choice(["A", "B", "C"])
                ))
                menus=menu.extract_menu_items(entry['menu'])
                for menu_name, menu_price in menus:
                    sql4 = """
                    INSERT INTO restaurant_menu (rest_id,menu_name,menu_price,menu_photo)
                    VALUES (%s,%s,%s,%s);
                    """
                    cursor.execute(sql4, (login_id,menu_name,menu_price,"null"))
                db.commit()

            except pymysql.Error as e:
                print(f"데이터베이스 작업 중 오류 발생: {e}")
                db.rollback()  # 롤백을 통해 이전 상태로 복구

finally:
    db.close()

print("데이터베이스에 데이터가 성공적으로 저장되었습니다.")
