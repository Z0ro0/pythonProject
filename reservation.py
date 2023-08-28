import datetime
from user_management import UserManagement
from PIL import Image

class ReservationManagement:
    #예약, 예약 조회, 예약 변경
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.user_management = UserManagement(self.db_connection)
        self.current_user_id = None
        
        #예약 가능한 좌석의 수
        self.available_reservation_seats = {
            '1': 30,
            '2': 50,
            '3': 60
        }

    def check_user_logged_in(self):
        if self.current_user_id is None:
            print("로그인이 필요합니다.")
            return False
        return True

    def make_reservation(self):
        #예약 기능
        #1. 방 선택하기
        #2. 시간 입력하기
        #3. 그 시간에 예약할 수 있는 좌석 알려 주기
        #4. 몇 번 좌석 예약할 건지 입력하기
        #예외... 그 시간에 예약 불가할 때는... 예외 처리 해 주기
        #예외... 이미 예약된 좌석일 때는 예약 불가능하게 해 주기
        if not self.check_user_logged_in():
            return

        print("1. 1번 방 - 코워킹스페이스 (30자리)")
        img = Image.open('coworking.png')
        img.show()
        print("2. 2번 방 - 도서관 (50자리)")
        img1 = Image.open('library.png.png')
        img1.show()
        print("3. 3번 방 - 상상카페2 (60자리)")
        img2 = Image.open('imaginecafe.png.png')
        img2.show()

        room_id = input("예약할 방: ")

        if room_id not in self.available_reservation_seats:
            print("해당 방은 존재하지 않습니다.")
            return

        pmax = self.available_reservation_seats[room_id]
        print(f"{room_id}번 방은 총 {pmax}개의 자리가 있습니다.")

        today_date = datetime.datetime.now().date().strftime('%Y-%m-%d')
        reservation_start_time = input("예약 시작 시간 (HH:MM): ")
        reservation_end_time = input("예약 종료 시간 (HH:MM): ")

        user_id = self.current_user_id

        available_seats = self.check_available_seats(room_id, today_date, reservation_start_time, reservation_end_time)

        if not available_seats:
            print("해당 시간에 예약 가능한 좌석이 없습니다.")
            return

        print(f"예약 가능한 좌석: {', '.join(available_seats)}")
        seat_number = input("예약할 좌석 번호: ")

        if seat_number not in available_seats:
            print("해당 좌석은 이미 예약되었거나 존재하지 않습니다.")
            return

        self.db_connection.cursor.execute("""
            INSERT INTO reservation (reservationid, roomid, id, seat, reservationdate, starttime, endtime)
            VALUES (reservation_id_seq.nextval, :roomid, :id, :seat, TO_DATE(:reservationdate, 'YYYY-MM-DD'), 
                    TO_TIMESTAMP(:starttime, 'HH24:MI'), TO_TIMESTAMP(:endtime, 'HH24:MI'))
        """, roomid=room_id, id=user_id, seat=seat_number, reservationdate=today_date,
            starttime=reservation_start_time, endtime=reservation_end_time)

        self.db_connection.connection.commit()
        print("예약이 완료되었습니다.")

    def check_available_seats(self, room_id, reservation_date, reservation_start_time, reservation_end_time):
        #예약 가능한 좌석인지 확인
        #방, 날짜, 시간에 예약된 좌석을 조회합니다.
        #조회된 좌석들 담아주기
        #가능한 좌석 담아주기
        #예약 가능한 좌석 반환
        
        self.db_connection.cursor.execute("""
            SELECT seat FROM reservation
            WHERE roomid = :roomid
            AND reservationdate = TO_DATE(:reservationdate, 'YYYY-MM-DD')
            AND (starttime, endtime) OVERLAPS (TO_TIMESTAMP(:starttime, 'HH24:MI'), TO_TIMESTAMP(:endtime, 'HH24:MI'))
        """, roomid=room_id, reservationdate=reservation_date, starttime=reservation_start_time,
            endtime=reservation_end_time)

        reserved_seats = [row[0] for row in self.db_connection.cursor.fetchall()]
        available_seats = [str(seat_number) for seat_number in range(1, self.available_reservation_seats[room_id] + 1)
                           if str(seat_number) not in reserved_seats]

        return available_seats

    def view_reservations(self):
        #예약 조회 기능
        #로그인 된 아이디에서 예약한 정보 불러오기
        #조회된 결과 한 줄씩 가져옴(null -)
        self.db_connection.cursor.execute("""
            SELECT reservationid, roomid, seat, TO_CHAR(reservationdate, 'YYYY-MM-DD'),
                   TO_CHAR(starttime, 'HH24:MI'), TO_CHAR(endtime, 'HH24:MI')
            FROM reservation
            WHERE id = :id
        """, id=self.current_user_id)

        print(" 예약 ID | 방 번호 | 좌석 번호 | 예약 날짜 | 시작 시간 | 종료 시간 ")
        print("-" * 52)

        for row in self.db_connection.cursor.fetchall():
            reservation_id, room_id, seat, reservation_date, start_time, end_time = row
            reserid = reservation_id or '-'
            room_id_str = room_id or '-'
            seat_str = seat or '-'
            reservation_date_str = reservation_date or '-'
            start_time_str = start_time or '-'
            end_time_str = end_time or '-'
            print(f" {reserid} | {room_id_str:^7} | {seat_str:^8} | {reservation_date_str} | {start_time_str} | {end_time_str}")

        print("-" * 52)#52번출력

    def modify_reservation(self):
        #예약 변경 기능
        #예약 조회 기능 긁어와서 그동안 예약한 내역 주르륵 보여주기
        #예약번호 선택하고 예약 정보 보여주기
        #시작 시간 끝나는 시간 업데이트 해 주기
            if not self.check_user_logged_in():
                return

            self.db_connection.cursor.execute("""
                        SELECT reservationid, roomid, seat, TO_CHAR(reservationdate, 'YYYY-MM-DD'),
                               TO_CHAR(starttime, 'HH24:MI'), TO_CHAR(endtime, 'HH24:MI')
                        FROM reservation
                        WHERE id = :id
                    """, id=self.current_user_id)

            print(" 예약 ID | 방 번호 | 좌석 번호 | 예약 날짜 | 시작 시간 | 종료 시간 ")
            print("-" * 52)

            for row in self.db_connection.cursor.fetchall():
                reservation_id, room_id, seat, reservation_date, start_time, end_time = row
                reserid = reservation_id or '-'
                room_id_str = room_id or '-'
                seat_str = seat or '-'
                reservation_date_str = reservation_date or '-'
                start_time_str = start_time or '-'
                end_time_str = end_time or '-'
                print(
                    f" {reserid} | {room_id_str:^7} | {seat_str:^8} | {reservation_date_str} | {start_time_str} | {end_time_str}")

            print("-" * 52)

            reservation_id = input("변경할 예약 ID: ")

            #다른 사람의 예약 정보를 바꿀 수 없도록 하는 코드
            self.db_connection.cursor.execute("""
                    SELECT roomid, seat, reservationdate, starttime, endtime FROM reservation
                    WHERE id = :id AND reservationid = :reservationid
                """, id=self.current_user_id, reservationid=reservation_id)

            row = self.db_connection.cursor.fetchone()

            if not row:
                print("해당 예약 정보를 찾을 수 없거나 권한이 없습니다.")
                return

            room_id, seat, reservation_date, start_time, end_time = row

            print("현재 예약 정보:")
            print(f"방 번호: {room_id}")
            print(f"좌석 번호: {seat}")
            print(f"예약 날짜: {reservation_date}")
            print(f"시작 시간: {start_time}")
            print(f"종료 시간: {end_time}")

            new_start_time = input("새로운 시작 시간 (HH:MM): ")
            new_end_time = input("새로운 종료 시간 (HH:MM): ")

            self.db_connection.cursor.execute("""
                UPDATE reservation
                SET starttime = TO_TIMESTAMP(:new_start_time, 'HH24:MI'), endtime = TO_TIMESTAMP(:new_end_time, 'HH24:MI')
                WHERE id = :id AND reservationid = :reservationid
            """, new_start_time=new_start_time, new_end_time=new_end_time,
                id=self.current_user_id, reservationid=reservation_id)

            self.db_connection.connection.commit()
            print("예약 정보가 변경되었습니다.")