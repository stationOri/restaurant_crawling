import pymysql

# MySQL 연결 설정
db = pymysql.connect(
    host='3.38.214.167',
    user='root',  # MySQL 사용자 이름
    password='ori6006',  # MySQL 비밀번호
    database='WaitMate',
    charset='utf8mb4'
)


# 삽입할 데이터 리스트
keywords = [
    "파스타",
    "모던한식",
    "돈까스",
    "카페",
    "퓨전음식",
    "한식",
    "일식",
    "중식"
]

try:

    with db.cursor() as cursor:
        sql = "ALTER TABLE keyword CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        cursor.execute(sql)
        db.commit()
        # 여러 개의 행을 한 번에 삽입하기 위한 SQL 문장 작성
        sql = "INSERT INTO keyword (keyword) VALUES (%s)"

        # 다수의 행을 삽입하기 위해 executemany() 사용
        cursor.executemany(sql, [(keyword,) for keyword in keywords])

        # 변경사항 저장
        db.commit()

        print(f"{cursor.rowcount} row(s) inserted successfully.")

except pymysql.Error as e:
    print(f"Error: {e}")
    db.rollback()  # 롤백하여 이전 상태로 복구

finally:
    db.close()
