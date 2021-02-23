#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict

import pymysql


class DatabaseHelper:
    def __init__(self, **kvs):
        self._conn = None
        self._db = kvs.get("db", "demo")
        self._port = kvs.get("port", 3306)
        self._user = kvs.get("user", "root")
        self._host = kvs.get("host", "localhost")
        self._passwd = kvs.get("passwd", "root")

    def connect(self):
        self._conn = pymysql.connect(
            host=self._host,
            user=self._user,
            passwd=self._passwd,
            db=self._db,
            port=self._port,
            charset="utf8",
        )
        self._conn.autocommit(True)

    # pylint: disable=broad-except
    def ping(self):
        try:
            self._conn.ping()
            self._conn.commit()
        except Exception as err:
            print("db ping info: ", err)
            try:
                self._conn.ping(reconnect=True)
                self._conn.commit()
            except Exception:
                print("db connecting...")
                self.connect()
                print("connected")

    def query(self, sql, args=None):
        self.ping()

        with self._conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, args)
            return cursor.fetchall()

    def update(self, sql, args=None):
        self.ping()

        affected_lines = 0
        with self._conn.cursor() as cursor:
            affected_lines = cursor.execute(sql, args)
            self._conn.commit()

        return affected_lines

    def insert(self, table, kvs: Dict):
        """See documentions here:
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        """
        self.ping()

        with self._conn.cursor() as cursor:
            insert_keys = kvs.keys()
            insert_keys_string = ", ".join([f"`{key}`" for key in insert_keys])
            insert_values_string = ", ".join([f"%%({key})s)" for key in insert_keys])

            sql = f"INSERT INTO {table} ({insert_keys_string}) VALUES ({insert_values_string})"

            cursor.execute(sql, kvs)
            self._conn.commit()

    def insert_many(self, sql, data_list):
        """See documentions here:
        https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-executemany.html
        """
        self.ping()
        with self._conn.cursor() as cursor:
            cursor.executemany(sql, data_list)
            self._conn.commit()

    def close(self):
        self._conn.close()
