class UserManagement:
    #로그인, 회원가입
    #
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def register_user(self, id, name, password, pnum):
        #회원가입 기능
        #id, name, password, pnum 받아서 insert 해 주고 회원가입 완료 출력
        self.db_connection.cursor.execute(
            "INSERT INTO userinfo (id, name, password, pnum) VALUES (:id, :name, :password, :pnum)",
            id=id, name=name, password=password, pnum=pnum)
        self.db_connection.connection.commit()
        print("회원가입 완료")

    def login(self, id, password):
        # 로그인 기능
        #id, password 맞는지 확인해서
        # if else 사용해서 사용자 정보 확인해야 됨

        #SELECT id FROM userinfo WHERE id = id AND password = password", id=id, password=password
        #콜론 써 줘야 오류 안 남
        self.db_connection.cursor.execute("SELECT id FROM userinfo WHERE id = :id AND password = :password", id=id, password=password)
        row = self.db_connection.cursor.fetchone()#한 줄 가져오기
        if row:
            print("로그인 성공!")
            self.current_user_id = row[0]
        else:
            print("로그인 실패")
