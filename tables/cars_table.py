# Таблица машин и особые действия с ней.

from dbtable import *


class CarsTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "cars"

    def columns(self):
        return {
            "plate_number": ["varchar(15)", "PRIMARY KEY"],
            "brand": ["varchar(100)", "NOT NULL"],
            "car_class": ["varchar(20)", "NOT NULL", "CHECK (car_class IN ('бизнес', 'эконом'))"],
            "color": ["varchar(50)", "NOT NULL"],
            "year_produced": ["integer", "NOT NULL", "CHECK (year_produced > 1900)"],
        }

    def column_names_without_id(self):
        return ["plate_number", "brand", "car_class", "color", "year_produced"]

    def primary_key(self):
        return ["plate_number"]

    def exists_by_plate(self, plate_number):
        sql = "SELECT 1 FROM " + self.table_name() + " WHERE plate_number = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (plate_number,))
        return cur.fetchone() is not None

    def update_by_plate(self, old_plate, new_data):
        sql = "UPDATE " + self.table_name()
        sql += " SET plate_number = %s, brand = %s, car_class = %s, color = %s, year_produced = %s"
        sql += " WHERE plate_number = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, new_data + [old_plate])
        self.dbconn.conn.commit()
        return

    def delete_by_plate(self, plate_number):
        sql = "DELETE FROM " + self.table_name() + " WHERE plate_number = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (plate_number,))
        self.dbconn.conn.commit()
        return
