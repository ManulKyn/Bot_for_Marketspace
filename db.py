import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id, username):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO `users` (`user_id`,`username`) VALUES (?, ?)", (user_id, username))
        return self.conn.commit()

    def user_follow_exists(self, user_id):
        """Проверяем, есть ли отслеживаемый товар в базе"""
        result = self.cursor.execute("SELECT `id` FROM `follow_goods` WHERE `user_id` = ?", (self.get_user_id(user_id),))
        return bool(len(result.fetchall()))

    def count_follows(self, user_id):
        """Проверяем, есть ли отслеживаемый товар в базе"""
        result = self.cursor.execute("SELECT `id` FROM `follow_goods` WHERE `user_id` = ?", (self.get_user_id(user_id),))
        return len(result.fetchall())

    def get_follow(self, user_id):
        """Достаем все отслеживаемые товары из базы"""
        result = self.cursor.execute("SELECT `goods_name`, `goods_price` FROM `follow_goods` WHERE `user_id` = ?", (self.get_user_id(user_id),))
        return result.fetchall()

    def get_follow_url(self, user_id):
        """Достаем все отслеживаемые товары из базы"""
        result = self.cursor.execute("SELECT `goods_url` FROM `follow_goods` WHERE `user_id` = ?", (self.get_user_id(user_id),))
        return result.fetchall()

    def add_follow(self, user_id, goods_name, goods_price, goods_url):
        """Создаем запись о товаре"""
        self.cursor.execute("INSERT INTO `follow_goods` (`user_id`, `goods_name`, `goods_price`, `goods_url`) VALUES (?, ?, ?, ?)",
            (self.get_user_id(user_id),
            goods_name,
            goods_price,
            goods_url)
        )
        return self.conn.commit()
    #
    # def get_records(self, user_id, within = "all"):
    #     """Получаем историю о доходах/расходах"""
    #
    #     if(within == "day"):
    #         result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY `date`",
    #             (self.get_user_id(user_id),))
    #     elif(within == "week"):
    #         result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY `date`",
    #             (self.get_user_id(user_id),))
    #     elif(within == "month"):
    #         result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `date` BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY `date`",
    #             (self.get_user_id(user_id),))
    #     else:
    #         result = self.cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? ORDER BY `date`",
    #             (self.get_user_id(user_id),))
    #
    #     return result.fetchall()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()