import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addStatement(self, id_user, id_status, auto, problem, booking_date):
        try:
            self.__cur.execute(
                "INSERT INTO request VALUES(NULL, ?, ?, ?, ?, ?)",
                (id_user, id_status, auto, problem, booking_date),
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления статьи в БД " + str(e))
            return False

        return True

    def getStatement(self, id):
        try:
            self.__cur.execute(f"SELECT * FROM request WHERE id = '{id}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return False

    def getAllStatements(self):
        try:
            self.__cur.execute(
                """SELECT request.*,
                               user.*
                                FROM request
                               JOIN user ON request.id_user=user.id """
            )
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return False

    def addUser(self, name, email, psw, phone):
        try:
            print(email, 'yjy')
            self.__cur.execute(
                f"SELECT COUNT() as `count` FROM user WHERE email LIKE '{email}'"
            )
            res = self.__cur.fetchone()
            if res["count"] > 0:
                print("Пользователь с таким email уже существует")
                return (False, "Пользователь с таким email уже существует")

            self.__cur.execute(
                "INSERT INTO user VALUES(NULL, 1, ?, ?, ?, ?)",
                (psw, name, phone, email),
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False

        return (True, "Вы успешно зарегестрировались")

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM user WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def getUserStatements(self, user_id):
        try:
            self.__cur.execute(
                """SELECT * 
                                  FROM request 
                                  WHERE id_user = ?""",
                (user_id,),
            )
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))

        return False

    def getUserRole(self, user_id):
        try:
            self.__cur.execute(
                f"SELECT id_role FROM user WHERE id = '{user_id}' LIMIT 1"
            )
            res = self.__cur.fetchone()
            for i in res:
                print(i)
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

    def updateApprove(self, statement_id, approve):
        try:
            self.__cur.execute(
                f"UPDATE request SET id_status = {int(approve)} WHERE id = '{int(statement_id)}'"
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
