# Таблица водителей и особые действия с ней.

from dbtable import *


class DriversTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "drivers"

    def columns(self):
        return {
            "inn": ["varchar(12)", "PRIMARY KEY"],
            "last_name": ["varchar(100)", "NOT NULL"],
            "first_name": ["varchar(100)", "NOT NULL"],
            "middle_name": ["varchar(100)"],
            "birth_date": ["date", "NOT NULL"],
            "passport_series": ["varchar(4)", "NOT NULL"],
            "passport_number": ["varchar(6)", "NOT NULL"],
            "car_plate": ["varchar(15)", "NOT NULL"],
        }

    def column_names_without_id(self):
        return ["inn", "last_name", "first_name", "middle_name", "birth_date", "passport_series", "passport_number", "car_plate"]

    def primary_key(self):
        return ["inn"]

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()

    def exists_by_inn(self, inn):
        sql = "SELECT 1 FROM " + self.table_name() + " WHERE inn = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (inn,))
        return cur.fetchone() is not None

    def all_by_car_plate(self, plate_number):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE car_plate = %s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (plate_number,))
        return cur.fetchall()

    def all_by_car_plate_paged(self, plate_number, limit, offset):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE car_plate = %s"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT %s OFFSET %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (plate_number, limit, offset))
        return cur.fetchall()

    def count_by_car_plate(self, plate_number):
        sql = "SELECT COUNT(*) FROM " + self.table_name() + " WHERE car_plate = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (plate_number,))
        return cur.fetchone()[0]

    def update_car_plate(self, old_plate, new_plate):
        sql = "UPDATE " + self.table_name() + " SET car_plate = %s WHERE car_plate = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (new_plate, old_plate))
        self.dbconn.conn.commit()
        return

    def delete_by_inn(self, inn):
        sql = "DELETE FROM " + self.table_name() + " WHERE inn = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (inn,))
        self.dbconn.conn.commit()
        return

    def delete_by_car_plate(self, plate_number):
        sql = "DELETE FROM " + self.table_name() + " WHERE car_plate = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (plate_number,))
        self.dbconn.conn.commit()
        return

    def update_by_inn(self, old_inn, new_data):
        sql = "UPDATE " + self.table_name()
        sql += " SET inn = %s, last_name = %s, first_name = %s, middle_name = %s, birth_date = %s, passport_series = %s, passport_number = %s, car_plate = %s"
        sql += " WHERE inn = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, new_data + [old_inn])
        self.dbconn.conn.commit()
        return
