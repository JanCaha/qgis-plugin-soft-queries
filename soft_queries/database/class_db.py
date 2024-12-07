import sqlite3
from pathlib import Path
from typing import Dict

from FuzzyMath.class_fuzzy_number import FuzzyNumber

from ..utils import python_object_to_string, string_to_python_object


class FuzzyDatabase:
    def __init__(self):
        self.path_database = Path(__file__).parent / "plugin.db"

        self.db_connection = sqlite3.connect(self.path_database)

        self.db_cursor = self.db_connection.cursor()

    def get_fuzzy_variables(self) -> Dict[str, FuzzyNumber]:
        sql = "SELECT variable_name, python_object FROM fuzzy_variables"

        self.db_cursor.execute(sql)

        data = self.db_cursor.fetchall()

        data_dict = {}

        for row in data:
            data_dict.update({row[0]: string_to_python_object(row[1])})

        return data_dict

    def add_fuzzy_variable(self, fuzzy_variable_name: str, fuzzy_number: FuzzyNumber) -> None:
        sql = "INSERT INTO fuzzy_variables VALUES (?,?)"

        self.db_connection.execute(sql, [fuzzy_variable_name, python_object_to_string(fuzzy_number)])

        self.db_connection.commit()

    def delete_fuzzy_variable(self, fuzzy_variable_name: str) -> None:
        sql = "DELETE FROM fuzzy_variables WHERE variable_name=?"

        self.db_connection.execute(sql, [fuzzy_variable_name])

        self.db_connection.commit()

    def get_fuzzy_variable(self, fuzzy_variable_name: str) -> FuzzyNumber:
        sql = "SELECT python_object FROM fuzzy_variables WHERE variable_name=?"

        self.db_cursor.execute(sql, [fuzzy_variable_name])

        data = self.db_cursor.fetchone()

        if data:
            return string_to_python_object(data[0])
        else:
            return None
