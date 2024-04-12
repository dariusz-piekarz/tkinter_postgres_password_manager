import psycopg2
from loguru import logger
from functools import wraps
import pandas as pd


class PostgreAdminConnector:
    tables_columns = dict({})

    def set_connection(self, user: str, password: str, host: str, port: str, database: str) -> None:
        self.connection = psycopg2.connect(
                                            user=user,
                                            password=password,
                                            host=host,
                                            port=port,
                                            database=database
                                         )
        self.cursor = self.connection.cursor()
        logger.info(f"Connection to {database} database established")

    def execute_query(self, query: str) -> list[tuple[any, ...]]:
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def query_to_df(self, qrt: str) -> pd.DataFrame:
        self.cursor.execute(qrt)
        record = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        df = pd.DataFrame(record, columns=columns)
        return df.copy(deep=True)

    def query_replace(self, query: str, words_to_replace: dict, to_df: bool = True):
        qry = query
        for key, value in words_to_replace.items():
            qry = qry.replace(key, value)
        if to_df:
            self.query_to_df(qry)
        else:
            self.execute_query(qry)

    def get_col_names(self, table_name: str) -> None:
        schema = table_name.split(".")[0]
        table = table_name.split(".")[1]
        self.cursor.execute(f"SELECT column_name FROM information_schema.columns"
                            f" WHERE table_schema = '{schema}'"
                            f"AND table_name = '{table}';")
        self.tables_columns[table_name] = [row[0] for row in self.cursor.fetchall()]

    def get_record_subset(self, table_name: str, col_names: list[str]) -> pd.DataFrame:
        if table_name not in self.tables_columns:
            self.get_col_names(table_name)
        cols = ", ".join(['"' + col_name + '"' for col_name in col_names])
        return self.query_to_df(f"SELECT {cols} FROM {table_name};")

    def get_record(self, table_name: str, where: dict[str: any]) -> list[tuple[any, ...]]:
        key_cond = '"' + list(where.keys())[0] + '"'
        val_cond = "'" + list(where.values())[0] + "'"
        qry = f'SELECT * FROM {table_name} WHERE {key_cond}={val_cond}'
        return self.execute_query(qry)

    def get_record_df(self, table_name: str, where: dict[str: any]) -> pd.DataFrame:
        key_cond = '"' + list(where.keys())[0] + '"'
        val_cond = "'" + list(where.values())[0] + "'"
        qry = f'SELECT * FROM {table_name} WHERE {key_cond}={val_cond}'
        return self.query_to_df(qry)

    def get_record_and_condition(self, table_name: str, where: dict[str: any]) -> list[tuple[any, ...]]:
        key_conds = ['"' + list(where.keys())[i] + '"' for i in range(2)]
        val_conds = ["'" + list(where.values())[i] + "'" for i in range(2)]
        qry = f'SELECT * FROM {table_name} WHERE {key_conds[0]}={val_conds[0]} AND {key_conds[1]}={val_conds[1]}'
        return self.execute_query(qry)

    def get_record_df_and_condition(self, table_name: str, where: dict[str: any]) -> pd.DataFrame:
        key_conds = ['"' + list(where.keys())[i] + '"' for i in range(2)]
        val_conds = ["'" + list(where.values())[i] + "'" for i in range(2)]
        qry = f'SELECT * FROM {table_name} WHERE {key_conds[0]}={val_conds[0]} AND {key_conds[1]}={val_conds[1]}'
        return self.query_to_df(qry)

    def insert_record(self, table_name: str, to_insert: dict[str: any]) -> None:
        if table_name not in self.tables_columns:
            self.get_col_names(table_name)

        columns = ", ".join(['"' + field_name + '"' for field_name in self.tables_columns[table_name]])
        values = ", ".join(["'" + to_insert[key_name] + "'"
                            if key_name in to_insert.keys()
                            else 'NULL'
                            for key_name in self.tables_columns[table_name]]).replace("'NULL'", "NULL")

        qrt = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        self.cursor.execute(qrt)
        self.connection.commit()

    def update_record(self, table_name: str, to_update: dict[str: any], update_on_field: dict[str: any]) -> None:

        update = ",".join(['"' + key + '"' + '=' + "'" + val + "'" for key, val in to_update.items()])

        where_key = '"' + str(list(update_on_field.keys())[0]) + '"'
        where_val = "'" + str(list(update_on_field.values())[0]) + "'"

        qrt = f'UPDATE {table_name} SET {update} WHERE {where_key}={where_val}'.replace("'NULL'", "NULL")
        self.cursor.execute(qrt)
        self.connection.commit()

    def update_record_condition_and(self, table_name: str, to_update: dict[str: any],
                                    update_on_fields: dict[str: any]) -> None:

        update = ",".join(['"' + key + '"' + '=' + "'" + val + "'" for key, val in to_update.items()])

        where_keys = ['"' + str(list(update_on_fields.keys())[i]) + '"' for i in range(2)]
        where_vals = ["'" + str(list(update_on_fields.values())[i]) + "'" for i in range(2)]

        qrt = (f'UPDATE {table_name} SET {update} WHERE {where_keys[0]}={where_vals[0]} '
               f'AND {where_keys[1]}={where_vals[1]}').replace("'NULL'", "NULL")
        self.cursor.execute(qrt)
        self.connection.commit()

    def delete_record(self, table_name: str, field_identifier: dict[str: any]) -> None:
        field_name = '"' + str(list(field_identifier.keys())[0]) + '"'
        field_value = "'" + str(list(field_identifier.values())[0]) + "'"

        qry = f"DELETE FROM {table_name} WHERE {field_name}={field_value};"
        self.cursor.execute(qry)
        self.connection.commit()

    def delete_record_condition_and(self, table_name: str, field_identifier: dict[str: any]) -> None:
        field_names = ['"' + str(list(field_identifier.keys())[i]) + '"' for i in range(2)]
        field_values = ["'" + str(list(field_identifier.values())[i]) + "'" for i in range(2)]

        qry = (f"DELETE FROM {table_name} WHERE {field_names[0]}={field_values[0]}"
               f" AND {field_names[1]}={field_values[1]};")
        self.cursor.execute(qry)
        self.connection.commit()

    def terminate_connection(self) -> None:
        if hasattr(self, 'cursor'):
            if self.cursor:
                self.cursor.close()
        if hasattr(self, 'connection'):
            if self.connection:
                self.connection.close()

    def __del__(self):
        self.terminate_connection()


if __name__ == "__main__":
    pass
