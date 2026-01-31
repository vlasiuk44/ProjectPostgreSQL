import sys
from datetime import datetime

sys.path.append('tables')

from project_config import *
from dbconnection import *
from dbtable import *
from cars_table import *
from drivers_table import *


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)
    page_size = 5

    def __init__(self):
        DbTable.dbconn = self.connection
        self.cars_cache = []
        self.car_plate = None
        self.cars_page = 0
        self.drivers_page = 0
        return

    def db_init(self):
        ct = CarsTable()
        dt = DriversTable()
        ct.create()
        dt.create()
        return

    def db_insert_somethings(self):
        ct = CarsTable()
        dt = DriversTable()
        ct.insert_one(["А777АА77", "Mercedes Benz E-Class", "бизнес", "черный", 2022])
        ct.insert_one(["К197ХК197", "Hyundai Solaris", "эконом", "белый", 2020])
        ct.insert_one(["М999ММ99", "BMW x5", "бизнес", "белый", 2021])
        ct.insert_one(["Е555КХ777", "Kia Rio", "эконом", "красный", 2019])
        ct.insert_one(["В123ОР750", "Skoda Karoq", "эконом", "серый", 2021])
        dt.insert_one(["770123456789", "Иванов", "Сергей", "Петрович", "1985-05-12", "4510", "123459", "А777АА77"])
        dt.insert_one(["770987654321", "Петров", "Алексей", "Игоревич", "1990-10-20", "4512", "654321", "К197ХК197"])
        dt.insert_one(["770111222333", "Сидоров", "Дмитрий", "Олегович", "1982-03-15", "4508", "111223", "М999ММ99"])
        dt.insert_one(["770444555666", "Кузнецов", "Андрей", "Васильевич", "1988-07-30", "4515", "556444", "Е555КХ777"])
        dt.insert_one(["500123987456", "Смирнов", "Михаил", "Юрьевич", "1993-12-01", "4610", "987623", "В123ОР750"])

    def db_drop(self):
        dt = DriversTable()
        ct = CarsTable()
        try:
            dt.drop()
        except Exception:
            pass
        try:
            ct.drop()
        except Exception:
            pass
        return

    def show_main_menu(self):
        menu = """Добро пожаловать!
Основное меню (выберите цифру в соответствии с необходимым действием):
    0 - повторить меню;
    1 - просмотр автомобилей;
    2 - сброс и инициализация таблиц;
    3 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step == "3":
            return "9"
        elif next_step == "0":
            return "0"
        elif next_step != "1" and next_step != "3":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def read_non_empty(self, prompt, max_len):
        while True:
            value = input(prompt).strip()
            if value == "1":
                return None
            if len(value) == 0:
                print("Значение не может быть пустым!")
                continue
            if len(value) > max_len:
                print("Слишком длинное значение! Максимум:", max_len)
                continue
            return value

    def read_optional(self, prompt, max_len):
        while True:
            value = input(prompt).strip()
            if value == "1":
                return None
            if len(value) == 0:
                return ""
            if len(value) > max_len:
                print("Слишком длинное значение! Максимум:", max_len)
                continue
            return value

    def read_int(self, prompt, min_val, max_val, cancel_key="1"):
        while True:
            value = input(prompt).strip()
            if value == cancel_key:
                return None
            if not value.isdigit():
                print("Введите целое число!")
                continue
            number = int(value)
            if number < min_val or number > max_val:
                print("Число должно быть в диапазоне", min_val, "-", max_val)
                continue
            return number

    def read_date(self, prompt):
        while True:
            value = input(prompt).strip()
            if value == "1":
                return None
            try:
                dt = datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                print("Введите дату в формате ГГГГ-ММ-ДД!")
                continue
            return dt.strftime("%Y-%m-%d")

    def read_index(self, prompt, max_index):
        while True:
            value = input(prompt).strip()
            if value == "0":
                return None
            if not value.isdigit():
                print("Введите номер строки!")
                continue
            number = int(value)
            if number < 1 or number > max_index:
                print("Введено число, неудовлетворяющее количеству строк!")
                continue
            return number

    def read_choice(self, prompt, choices):
        while True:
            value = input(prompt).strip()
            if value == "1":
                return None
            if value not in choices:
                print("Выберите одно из значений:", ", ".join(choices))
                continue
            return value

    def read_digits(self, prompt, length):
        while True:
            value = input(prompt).strip()
            if value == "1":
                return None
            if not value.isdigit() or len(value) != length:
                print("Введите число длиной", length)
                continue
            return value

    def show_cars(self):
        menu = """Просмотр списка автомобилей!
№\tГосномер\tМарка\tКласс\tЦвет\tГод"""
        print(menu)
        total = CarsTable().count_all()
        total_pages = max(1, (total + self.page_size - 1) // self.page_size)
        if self.cars_page >= total_pages:
            self.cars_page = total_pages - 1
        if self.cars_page < 0:
            self.cars_page = 0
        offset = self.cars_page * self.page_size
        self.cars_cache = CarsTable().all_paged(self.page_size, offset)
        if len(self.cars_cache) == 0:
            print("Нет записей.")
        else:
            for idx, car in enumerate(self.cars_cache, start=1):
                print(str(idx) + "\t" + str(car[0]) + "\t" + str(car[1]) + "\t" + str(car[2]) + "\t" + str(car[3]) + "\t" + str(car[4]))
        print("Страница:", str(self.cars_page + 1), "из", str(total_pages))
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - добавление нового автомобиля;
    2 - изменение автомобиля;
    3 - удаление автомобиля;
    4 - просмотр водителей автомобиля;
    5 - следующая страница;
    6 - предыдущая страница;
    7 - выход."""
        print(menu)
        return

    def after_show_cars(self, next_step):
        while True:
            if next_step == "3":
                self.show_delete_car()
                return "1"
            elif next_step == "4":
                return self.show_drivers_by_car()
            elif next_step == "5":
                self.cars_page += 1
                return "1"
            elif next_step == "6":
                self.cars_page -= 1
                return "1"
            elif next_step == "1":
                self.show_add_car()
                return "1"
            elif next_step == "2":
                self.show_edit_car()
                return "1"
            elif next_step != "0" and next_step != "7":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                if next_step == "7":
                    return "9"
                return next_step

    def show_add_car(self):
        ct = CarsTable()
        plate_number = self.read_non_empty("Введите госномер (1 - отмена): ", 15)
        if plate_number is None:
            return
        if ct.exists_by_plate(plate_number):
            print("Автомобиль с таким номером уже существует!")
            return
        brand = self.read_non_empty("Введите марку (1 - отмена): ", 100)
        if brand is None:
            return
        car_class = self.read_choice("Введите класс (бизнес/эконом, 1 - отмена): ", ["бизнес", "эконом"])
        if car_class is None:
            return
        color = self.read_non_empty("Введите цвет (1 - отмена): ", 50)
        if color is None:
            return
        year_produced = self.read_int("Введите год выпуска (>1900, 1 - отмена): ", 1901, 2100)
        if year_produced is None:
            return
        ct.insert_one([plate_number, brand, car_class, color, year_produced])
        return

    def show_edit_car(self):
        if len(self.cars_cache) == 0:
            print("Список автомобилей пуст!")
            return
        num = self.read_index("Укажите номер строки автомобиля для изменения (0 - отмена): ", len(self.cars_cache))
        if num is None:
            return
        car = self.cars_cache[num - 1]
        old_plate = car[0]
        print("Изменение автомобиля:", old_plate)
        new_plate = input("Введите госномер (Enter - без изменений, 1 - отмена): ").strip()
        if new_plate == "1":
            return
        if len(new_plate) == 0:
            new_plate = old_plate
        elif len(new_plate) > 15:
            print("Слишком длинное значение! Максимум: 15")
            return
        elif new_plate != old_plate and CarsTable().exists_by_plate(new_plate):
            print("Автомобиль с таким номером уже существует!")
            return
        brand = input("Введите марку (Enter - без изменений, 1 - отмена): ").strip()
        if brand == "1":
            return
        if len(brand) == 0:
            brand = car[1]
        elif len(brand) > 100:
            print("Слишком длинное значение! Максимум: 100")
            return
        car_class = input("Введите класс (бизнес/эконом, Enter - без изменений, 1 - отмена): ").strip()
        if car_class == "1":
            return
        if len(car_class) == 0:
            car_class = car[2]
        elif car_class not in ["бизнес", "эконом"]:
            print("Класс должен быть: бизнес или эконом")
            return
        color = input("Введите цвет (Enter - без изменений, 1 - отмена): ").strip()
        if color == "1":
            return
        if len(color) == 0:
            color = car[3]
        elif len(color) > 50:
            print("Слишком длинное значение! Максимум: 50")
            return
        year_input = input("Введите год выпуска (>1900, Enter - без изменений, 1 - отмена): ").strip()
        if year_input == "1":
            return
        if len(year_input) == 0:
            year_produced = car[4]
        elif not year_input.isdigit():
            print("Введите целое число!")
            return
        else:
            year_produced = int(year_input)
            if year_produced <= 1900:
                print("Год должен быть больше 1900")
                return
        CarsTable().update_by_plate(old_plate, [new_plate, brand, car_class, color, year_produced])
        if new_plate != old_plate:
            DriversTable().update_car_plate(old_plate, new_plate)
        return

    def show_delete_car(self):
        if len(self.cars_cache) == 0:
            print("Список автомобилей пуст!")
            return
        num = self.read_index("Укажите номер строки автомобиля для удаления (0 - отмена): ", len(self.cars_cache))
        if num is None:
            return
        car = self.cars_cache[num - 1]
        plate_number = car[0]
        answer = input("Удалить автомобиль и связанных водителей? (д/н, 1 - отмена): ").strip().lower()
        if answer == "1":
            return
        if answer in ["д", "y"]:
            DriversTable().delete_by_car_plate(plate_number)
            CarsTable().delete_by_plate(plate_number)
            print("Автомобиль удален!")
        else:
            print("Удаление отменено.")
        return

    def show_drivers_by_car(self):
        self.car_plate = None
        self.drivers_page = 0
        if len(self.cars_cache) == 0:
            print("Список автомобилей пуст!")
            return "1"
        num = self.read_index("Укажите номер строки автомобиля (0 - отмена): ", len(self.cars_cache))
        if num is None:
            return "1"
        car = self.cars_cache[num - 1]
        self.car_plate = car[0]
        while True:
            print("Выбран автомобиль:", self.car_plate)
            print("Водители автомобиля:")
            total = DriversTable().count_by_car_plate(self.car_plate)
            total_pages = max(1, (total + self.page_size - 1) // self.page_size)
            if self.drivers_page >= total_pages:
                self.drivers_page = total_pages - 1
            if self.drivers_page < 0:
                self.drivers_page = 0
            offset = self.drivers_page * self.page_size
            drivers = DriversTable().all_by_car_plate_paged(self.car_plate, self.page_size, offset)
            print("№\tИНН\tФамилия\tИмя\tОтчество\tДата рожд.\tПаспорт")
            if len(drivers) == 0:
                print("Нет записей.")
            else:
                for idx, drv in enumerate(drivers, start=1):
                    passport = str(drv[5]) + " " + str(drv[6])
                    print(str(idx) + "\t" + str(drv[0]) + "\t" + str(drv[1]) + "\t" + str(drv[2]) + "\t" + str(drv[3]) + "\t" + str(drv[4]) + "\t" + passport)
            print("Страница:", str(self.drivers_page + 1), "из", str(total_pages))
            menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр автомобилей;
    2 - изменение водителя;
    3 - следующая страница;
    4 - предыдущая страница;
    5 - добавление водителя;
    6 - удаление водителя;
    7 - выход."""
            print(menu)
            step = self.read_next_step()
            if step == "5":
                self.show_add_driver()
            elif step == "6":
                self.show_delete_driver(drivers)
            elif step == "2":
                self.show_edit_driver(drivers)
            elif step == "3":
                self.drivers_page += 1
            elif step == "4":
                self.drivers_page -= 1
            elif step == "0":
                return "0"
            elif step == "1":
                return "1"
            elif step == "7":
                return "9"
            else:
                print("Выбрано неверное число! Повторите ввод!")

    def show_add_driver(self):
        dt = DriversTable()
        inn = self.read_digits("Введите ИНН (12 цифр, 1 - отмена): ", 12)
        if inn is None:
            return
        if dt.exists_by_inn(inn):
            print("Водитель с таким ИНН уже существует!")
            return
        last_name = self.read_non_empty("Введите фамилию (1 - отмена): ", 100)
        if last_name is None:
            return
        first_name = self.read_non_empty("Введите имя (1 - отмена): ", 100)
        if first_name is None:
            return
        middle_name = self.read_optional("Введите отчество (1 - отмена, можно пусто): ", 100)
        if middle_name is None:
            return
        birth_date = self.read_date("Введите дату рождения (ГГГГ-ММ-ДД, 1 - отмена): ")
        if birth_date is None:
            return
        passport_series = self.read_digits("Введите серию паспорта (4 цифры, 1 - отмена): ", 4)
        if passport_series is None:
            return
        passport_number = self.read_digits("Введите номер паспорта (6 цифр, 1 - отмена): ", 6)
        if passport_number is None:
            return
        dt.insert_one([inn, last_name, first_name, middle_name, birth_date, passport_series, passport_number, self.car_plate])
        return

    def show_delete_driver(self, drivers):
        if len(drivers) == 0:
            print("Список водителей пуст!")
            return
        num = self.read_index("Укажите номер строки водителя для удаления (0 - отмена): ", len(drivers))
        if num is None:
            return
        driver = drivers[num - 1]
        DriversTable().delete_by_inn(driver[0])
        print("Водитель удален!")
        return

    def show_edit_driver(self, drivers):
        if len(drivers) == 0:
            print("Список водителей пуст!")
            return
        num = self.read_index("Укажите номер строки водителя для изменения (0 - отмена): ", len(drivers))
        if num is None:
            return
        driver = drivers[num - 1]
        old_inn = driver[0]
        print("Изменение водителя:", driver[1], driver[2], driver[3], "(", old_inn, ")")
        inn = input("Введите ИНН (12 цифр, Enter - без изменений, 1 - отмена): ").strip()
        if inn == "1":
            return
        if len(inn) == 0:
            inn = old_inn
        elif not inn.isdigit() or len(inn) != 12:
            print("Введите ИНН из 12 цифр!")
            return
        elif inn != old_inn and DriversTable().exists_by_inn(inn):
            print("Водитель с таким ИНН уже существует!")
            return
        last_name = input("Введите фамилию (Enter - без изменений, 1 - отмена): ").strip()
        if last_name == "1":
            return
        if len(last_name) == 0:
            last_name = driver[1]
        elif len(last_name) > 100:
            print("Слишком длинное значение! Максимум: 100")
            return
        first_name = input("Введите имя (Enter - без изменений, 1 - отмена): ").strip()
        if first_name == "1":
            return
        if len(first_name) == 0:
            first_name = driver[2]
        elif len(first_name) > 100:
            print("Слишком длинное значение! Максимум: 100")
            return
        middle_name = input("Введите отчество (Enter - без изменений, 1 - отмена): ").strip()
        if middle_name == "1":
            return
        if len(middle_name) == 0:
            middle_name = driver[3]
        elif len(middle_name) > 100:
            print("Слишком длинное значение! Максимум: 100")
            return
        birth_date_input = input("Введите дату рождения (ГГГГ-ММ-ДД, Enter - без изменений, 1 - отмена): ").strip()
        if birth_date_input == "1":
            return
        if len(birth_date_input) == 0:
            birth_date = driver[4]
        else:
            try:
                birth_date = datetime.strptime(birth_date_input, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Введите дату в формате ГГГГ-ММ-ДД!")
                return
        passport_series = input("Введите серию паспорта (4 цифры, Enter - без изменений, 1 - отмена): ").strip()
        if passport_series == "1":
            return
        if len(passport_series) == 0:
            passport_series = driver[5]
        elif not passport_series.isdigit() or len(passport_series) != 4:
            print("Введите серию паспорта из 4 цифр!")
            return
        passport_number = input("Введите номер паспорта (6 цифр, Enter - без изменений, 1 - отмена): ").strip()
        if passport_number == "1":
            return
        if len(passport_number) == 0:
            passport_number = driver[6]
        elif not passport_number.isdigit() or len(passport_number) != 6:
            print("Введите номер паспорта из 6 цифр!")
            return
        DriversTable().update_by_inn(old_inn, [inn, last_name, first_name, middle_name, birth_date, passport_series, passport_number, self.car_plate])
        print("Водитель обновлен!")
        return

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_cars()
                next_step = self.read_next_step()
                current_menu = self.after_show_cars(next_step)
            elif current_menu == "2":
                self.show_main_menu()
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()


m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle()
