import unittest
import requests
import json
import sqlite3

class HistoryTests(unittest.TestCase):
    #Clase de pruebas para el endpoint /historial

    @classmethod
    def setUpClass(cls) -> None:
        #Para el setUp buscamos la información que existe en la base de datos.
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
        #Para el tearDown cerramos la conexión con la base de datos.
        cls.connection.close()

    def test_get_history(self):
        #Revisa si el endpoint devuelve correctamente lo que esta en la base de datos.
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()
        self.assertEqual(actual_data, self.expected_data)

    def test_get_history_blank(self):
        #Comprobamos que el sistema no se cae en caso de que la base de datos este vacía.
        #*Solo va a dar respuesta positiva cuando la base de datos esta vacía.
        response = requests.get(self.url) 
        self.assertEqual(response.status_code, 200)
        actual_data = response.json()
        self.assertEqual(actual_data, "El historial está vacío")


class SearchTests(unittest.TestCase):
    #Clase de pruebas para el endpoint /busqueda

    @classmethod
    def setUpClass(cls) -> None:
        #Guardamos el estado de la base de datos antes de hacer las pruebas. Además seteamos algunos datos acá para mantener orden.
        cls.url = "http://localhost:3000/busqueda"
        cls.conn = sqlite3.connect('talleres.db')
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute('SELECT * FROM talleres')
        cls.state = cls.cursor.fetchall()
        cls.payload_st = {"description": "taller"}
        cls.payload_yoga = {"description": "taller de yoga"}

    @classmethod
    def tearDownClass(cls) -> None:
        #Devolvemos la base de datos al estado que estaba antes de hacer las pruebas y cerramos conexión.
        del cls.url
        del cls.payload_st
        del cls.payload_yoga
        cls.cursor.execute('DELETE FROM talleres')
        for row in cls.state:
            cls.cursor.execute('INSERT INTO talleres VALUES (?, ?, ?, ?, ?, ?, ?)', row)
        cls.conn.commit()
        cls.conn.close()


    def test_post_busqueda_notem(self):
        #Si no se específica la temática el sistema debe informar al usuario que no entrego suficiente información.
        response = requests.post(self.url, json=self.payload_st)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json() == "ChatGPT no encontro la tematica del taller." or response.json() == "ChatGPT no siguio el formato establecido.")
    
    def test_post_busqueda(self):
        #Búsqueda válida, se verifica que siga el formato que se solicita (Una lista de diccionarios).
        response = requests.post(self.url, json=self.payload_yoga)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertIsInstance(response.json()[1], dict)

if __name__ == '__main__':
    unittest.main()