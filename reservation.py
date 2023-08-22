from datetime import datetime
from database import DatabaseConnection
from user_management import UserManagement


class ReservationManagement:
    def __init__(self, db_connection):
        self.db_connection = db_connection
        self.user_management = UserManagement(self.db_connection)
        self.current_user_id = None
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
        if not self.check_user_logged_in():
            return

        print("1. 1번 방 - 코워킹스페이스 (30자리)")
        print("2. 2번 방 - 도서관 (50자리)")
        print("3. 3번 방 - 도서관 (60자리)")
        room_id = input("예약할 방: ")

        if room_id not in self.available_reservation_seats:
            print("해당 방은 존재하지 않습니다.")
            return

        pmax = self.available_reservation_seats[room_id]
        print(f"{room_id}번 방은 총 {pmax}개의 자리가 있습니다.")

        today_date = datetime.now().date().strftime('%Y-%m-%d')
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
