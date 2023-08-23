from datetime import datetime


def submit_suggestion(reservation_system, suggestion_content):
    if not reservation_system.check_user_logged_in():
        return

    # 로그인된 사용자 ID 가져오기
    reservation_system.db_connection.cursor.execute("SELECT id FROM userinfo WHERE id = :id",
                                                    id=reservation_system.current_user_id)
    row = reservation_system.db_connection.cursor.fetchone()

    if row:
        user_id = row[0]
    else:
        print("사용자 정보를 가져올 수 없습니다.")
        return

    submission_date = datetime.now().date()

    # id는 primary key라서 외래 참조해야 됨 ex)1,2,3,4
    reservation_system.db_connection.cursor.execute("""
            INSERT INTO suggestion (suggestionid, id, submissiondate, suggestioncontent)
            VALUES (suggestion_id_seq.nextval, :id, :submissiondate, :suggestioncontent)
        """, id=user_id, submissiondate=submission_date, suggestioncontent=suggestion_content)

    reservation_system.db_connection.connection.commit()
    print("문의 사항 등록 완료")
