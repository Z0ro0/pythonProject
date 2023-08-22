class UserManagement:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_user(self, id, name, password, pnum):
        self.db_connection.cursor.execute(
            "INSERT INTO userinfo (id, name, password, pnum) VALUES (:id, :name, :password, :pnum)",
            id=id, name=name, password=password, pnum=pnum)
        self.db_connection.connection.commit()
        print("사용자 등록이 완료되었습니다.")

    def login(self, id, password):
        # 로그인 기능
        # if else 사용해서 사용자 정보 확인해야 됨
        # 비밀번호와 아이디 받기
        self.db_connection.cursor.execute("SELECT id FROM userinfo WHERE id = :id AND password = :password",
                            id=id, password=password)

        row = self.db_connection.cursor.fetchone()
        if row:
            print("로그인 성공!")
            self.current_user_id = row[0]
        else:
            print("로그인 실패: 사용자 정보가 맞지 않습니다.")
