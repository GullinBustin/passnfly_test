import pymysql.cursors


class DatabaseClient:

    insert_sql = "INSERT INTO {table} ({names}) VALUES ({values})"
    update_sql = "UPDATE {table} SET {key_and_values} WHERE {where};"
    delete_sql = "DELETE FROM {table} WHERE {where}; "

    @staticmethod
    def list_to_string(my_list):
        return ','.join(f"'{x}'" if isinstance(x, str) else f"{x}" for x in my_list)

    @staticmethod
    def key_value_to_string(element):
        return ','.join(f"{key}='{element[key]}'"
                        if isinstance(element[key], str)
                        else f"{key}={element[key]}"
                        for key in element)

    @staticmethod
    def where_string(field, value, comparator="="):
        if isinstance(value, str):
            return f"{field}{comparator}'{value}'"
        return f"{field}{comparator}{value}"

    def __init__(self, config):
        self.connection = pymysql.connect(**config)

    def insert(self, element, table):
        with self.connection.cursor() as cursor:
            sql = self.insert_sql.format(table=table,
                                         names=", ".join(element.keys()),
                                         values=self.list_to_string(element.values()))
            cursor.execute(sql)
        self.connection.commit()

    def update(self, element, table, where):
        with self.connection.cursor() as cursor:
            sql = self.update_sql.format(table=table,
                                         key_and_values=self.key_value_to_string(element),
                                         where=self.where_string(**where))
            cursor.execute(sql)
        self.connection.commit()

    def delete(self, table, where):
        with self.connection.cursor() as cursor:
            sql = self.delete_sql.format(table=table,
                                         where=self.where_string(**where))
            cursor.execute(sql)
        self.connection.commit()
