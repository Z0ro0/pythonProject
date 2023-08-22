from datetime import datetime
from database import DatabaseConnection
from reservation import ReservationManagement
from user_management import UserManagement

def main():
    db_connection = DatabaseConnection("reservation", "1234", "127.0.0.1", "1521", "XE")
    reservation_system = ReservationManagement(db_connection)

    while True:
        print("1. 회원가입")
        print("2. 로그인")
        print("3. 예약")
        print("4. 예약 변경")
        print("5. 예약 조회")
        print("6. 문의사항 등록")
        print("0. 종료")
        choice = input("원하는 작업 선택: ")

        if choice == "1":
            id = input("사용자 아이디: ")
            name = input("사용자 이름: ")
            password = input("비밀번호: ")
            pnum = input("전화번호: ")
            reservation_system.user_management.register_user(id, name, password, pnum)

        elif choice == "2":
            id = input("사용자 아이디: ")
            password = input("비밀번호: ")
            reservation_system.user_management.login(id, password)
            reservation_system.current_user_id = id

        elif choice == "3":
            reservation_system.make_reservation()

        elif choice == "4":
            reservation_system.modify_reservation()

        elif choice == "5":
            reservation_system.view_reservations()

        elif choice == "6":
            if reservation_system.check_user_logged_in():
                suggestion_content = input("문의 내용 : ")
                reservation_system.db_connection.submit_suggestion(suggestion_content)
            else:
                print("로그인 필요")

        elif choice == "0":
            reservation_system.db_connection.close()
            break

        else:
            print("선택할 수 있는 선택지가 아닙니다")

if __name__ == "__main__":
    main()