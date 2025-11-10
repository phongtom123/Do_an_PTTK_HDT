def get_all_units():
    """
    Lấy danh sách tất cả Units trong database 'bleu'.
    Trả về danh sách tuple (unit_id, unit_name)
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT unit_id, unit_name
            FROM Units
            ORDER BY unit_id;
        """)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    except mysql.connector.Error as e:
        print("❌ Lỗi lấy Units:", e)
        return []
    except Exception as e:
        print("❌ Lỗi không xác định khi lấy Units:", e)
        return []
