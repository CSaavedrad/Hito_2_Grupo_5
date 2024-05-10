import unittest
import requests
import json
import sqlite3

class HistoryTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        cls.connection = sqlite3.connect('talleres.db')
        cls.cursor = cls.connection.cursor()
        cls.url = "http://localhost:3000/historial"
        cls.cursor.execute('SELECT * FROM talleres')
        rows = cls.cursor.fetchall()
        cls.expected_data = []
        for row in rows:
            columns = [column[0] for column in cls.cursor.description]
            cls.expected_data.append(dict(zip(columns, row)))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.connection.close()

    def test_get_history(self):

        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()
        self.assertEqual(actual_data, self.expected_data)

    def test_get_history_blank(self):
        
        response = requests.get(self.url) 
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()
        self.assertEqual(actual_data, [])


class SearchTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.url = "http://localhost:3000/busqueda"
        cls.conn = sqlite3.connect('talleres.db')
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('SELECT * FROM talleres')
        cls.state = cls.cursor.fetchall()
        cls.payload_st = {"description": "taller"}
        cls.payload_yoga = {"description": "taller de yoga"}

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.url
        del cls.payload_st
        del cls.payload_yoga
        cls.cursor.execute('DELETE FROM talleres')
        for row in cls.state:
            cls.cursor.execute('INSERT INTO talleres VALUES (?, ?, ?, ?, ?, ?, ?)', row)
        cls.conn.commit()
        cls.conn.close()


    def test_busqueda_endpoint_sin_tematica(self):
        response = requests.post(self.url, json=self.payload_st)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json() == "ChatGPT no encontro la tematica del taller." or response.json() == "ChatGPT no siguio el formato establecido.")
    
    def test_BusquedaEndpoint(self):
        response = requests.post(self.url, json=self.payload_yoga)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertIsInstance(response.json()[1], dict)




if __name__ == '__main__':
    unittest.main()