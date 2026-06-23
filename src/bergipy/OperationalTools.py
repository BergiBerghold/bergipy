import time, os
import mysql.connector
import datetime

def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def wait_for_prev_measurement(prev_pid):
    print('Waiting until previous measurement is done...')

    while True:
        if check_pid(prev_pid):
            time.sleep(1)
        else:
            break

    print(f'PID {prev_pid} is done. Starting in 3s ...')


class sqlWriter:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self, db_name):
        self.db_connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password)
        self.cursor = self.db_connection.cursor()

        self.cursor.execute(f"USE {db_name}")

    def select_table(self, table_name, table_fields):
        '''
        :param table_name: str: name of table you whish to write/create
        :param table_fields: dict: {name_of_field: type_of_field} e.g. {current: DECIMAL(8, 4)}
        '''

        self.table_name = table_name
        self.table_fields = table_fields

        self.cursor.execute("SHOW TABLES")
        existing_tables = [x[0] for x in self.cursor]

        if self.table_name not in existing_tables:
            print(f'Creating new table {self.table_name}')
            self.cursor.execute(f"CREATE TABLE {self.table_name} "
                                f"(id BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, "
                                f"time DATETIME, "
                                f"{', '.join([f'{field_name} {field_type}' for field_name, field_type in self.table_fields.items()])})")

    def write_sql(self, table_values):
        '''
        :param table_values: dict: {name_of_field: value_of_field} e.g. {current: 1.3}
        '''
        sql = (f"INSERT INTO {self.table_name} "
               f"(time, {', '.join(table_values.keys())}) "
               f"VALUES "
               f"(%s, {', '.join(['%s'] * len(table_values.keys()))})")


        val = (datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), *table_values.values())

        self.cursor.execute(sql, val)
        self.db_connection.commit()

    def close_connection(self):
        self.db_connection.close()