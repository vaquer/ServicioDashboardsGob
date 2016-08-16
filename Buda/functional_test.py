# -*- coding: utf-8 -*-
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestEstadoActualEstadisticas(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_estado_estadisticas(self):
        """
        Como usuario quiero ser capaz de ver el estado actual
        en las estadísticas de cada una de las instituciones 
        de la APF y conocer detalles de esta con respecto 
        a la ley de apertura de datos.
        """
        self.browser.get('http://0.0.0.0:8000/tablero-instituciones/')

        # Verificar carga de interfaz de usuario
        self.assertEquals(self.browser.title, 'Tabla Comparativa')

        # Verificar cantidades y tipo de dato
        self.assertTrue(int(self.browser.find_element_by_css_selector('p#downloadsTotal').text.replace(',', '')) > 0)
        self.assertTrue(int(self.browser.find_element_by_css_selector('p#resourcesTotal').text.replace(',', '')) > 0)
        self.assertTrue(int(self.browser.find_element_by_css_selector('p#dependencesTotal').text.replace(',', '')) > 0)

        # Verificar Top 5 Datos
        tabla_top_5_datos = self.browser.find_element_by_css_selector('table#top-5-datos')
        filas = tabla_top_5_datos.find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')

        # Verificando cantidad de datos
        self.assertEquals(len(filas), 6)

        # Verificando datos en la tabla
        contador = 1
        cantidad_anterior = 0
        for fila in filas:
            if fila.text:
                self.assertTrue(fila.find_element_by_css_selector('td.datosTitle').text.strip())
                self.assertTrue(fila.find_element_by_css_selector('td.datosTitle').text.strip() == fila.find_element_by_css_selector('td.datosTitle').get_attribute('title').strip())
                # Verifcando el orden del Top 5
                if cantidad_anterior > 0:
                    self.assertTrue(int(fila.find_element_by_css_selector('td.text-center').text.strip().replace(',', '')) <= cantidad_anterior)
                cantidad_anterior = int(fila.find_element_by_css_selector('td.text-center').text.strip().replace(',', ''))
            contador =+ 1

        # Verificar Top 5 Instituciones
        tabla_top_5_institucion = self.browser.find_element_by_css_selector('table#top-5-institucion')
        filas = tabla_top_5_datos.find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')

        # Verificando cantidad de datos
        self.assertEquals(len(filas), 6)

        # Verificando datos en la tabla
        contador = 1
        cantidad_anterior = 0
        for fila in filas:
            if fila.text:
                self.assertTrue(fila.find_element_by_css_selector('td.datosTitle').text.strip())
                self.assertTrue(fila.find_element_by_css_selector('td.datosTitle').text.strip() == fila.find_element_by_css_selector('td.datosTitle').get_attribute('title').strip())
                # Verifcando el orden del Top 5
                if cantidad_anterior > 0:
                    self.assertTrue(int(fila.find_element_by_css_selector('td.text-center').text.strip().replace(',', '')) <= cantidad_anterior)
                cantidad_anterior = int(fila.find_element_by_css_selector('td.text-center').text.strip().replace(',', ''))

            contador =+ 1

        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_1/paso1.png')
        input_buscar = self.browser.find_element_by_css_selector('input#searchbox')

        # Verificando estado inicial campo de busqueda 
        self.assertEquals(input_buscar.get_attribute('placeholder'), u'Busca una institución')

        # Verificando elementos en tabla comparativa
        tabla_comparativa = self.browser.find_element_by_css_selector('table#apf_table')
        tbody_tabla_comparativa = tabla_comparativa.find_element_by_css_selector('tbody')
        titulos_tabla_comparativa = tabla_comparativa.find_element_by_css_selector('thead').find_elements_by_css_selector('td')
        filas_tabla_comparativa = tbody_tabla_comparativa.find_elements_by_css_selector('tr')

        # Verificando existencia de instituciones en el tablero
        self.assertTrue(len(filas_tabla_comparativa) > 0)

        columnas = [
            {'nombre': u'Institución', 'tipo': str},
            {'nombre': u'Ranking', 'tipo': int},
            {'nombre': u'Datos', 'tipo': int},
            {'nombre': u'Calif. Apertura', 'tipo': str},
            {'nombre': u'Descargas', 'tipo': str},
            {'nombre': u'Calidad', 'tipo': str}
        ]

        # Verificando titulos en la tabla 
        contador = 0
        for columna in titulos_tabla_comparativa:
            self.assertIn(columnas[contador]['nombre'], columna.text)
            contador += 1
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_1/paso2.png')

        # Verificando paginacion de tabla
        botones_paginacion = [boton.get_attribute('data-dt-idx') for boton in self.browser.find_elements_by_css_selector('a.paginate_button')]
        tbody_tabla_comparativa = tabla_comparativa.find_element_by_css_selector('tbody')

        for pagina in botones_paginacion[:5]:
            boton = self.browser.find_element_by_css_selector('a.paginate_button[data-dt-idx="{0}"]'.format(pagina))
            if boton.text not in 'Anterior' and boton.text not in 'Siguiente':
                pagina = boton.text
                self.assertEquals(int(boton.text), int(boton.get_attribute('data-dt-idx')))
                boton.click()
                self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_1/paso3_{0}.png'.format(pagina))
                # self.assertIn('current', self.browser.find_element_by_css_selector('a.paginate_button[data-dt-idx="{0}"]'.format(pagina)).get_attribute('class'))

        # Verificando busqueda
        input_buscar.send_keys('SE')
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_1/paso4.png')
        for fila in self.browser.find_element_by_css_selector('table#apf_table').find_element_by_css_selector('tbody').find_elements_by_css_selector('tr'):
            self.assertIn('SE', fila.find_element_by_css_selector('td.depenTitle').text)

        input_buscar.clear()
        input_buscar.send_keys('AG')
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_1/paso5.png')
        for fila in self.browser.find_element_by_css_selector('table#apf_table').find_element_by_css_selector('tbody').find_elements_by_css_selector('tr'):
            self.assertIn('AG', fila.find_element_by_css_selector('td.depenTitle').text)

        input_buscar.send_keys(Keys.RETURN)
        input_buscar.send_keys(Keys.RETURN)
        time.sleep(1)
        # Verificando apertura de detalle
        elemento_dependencia = self.browser.find_element_by_css_selector('table#apf_table').find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')[0]
        texto_dependencia = elemento_dependencia.text
        elemento_dependencia.click()
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_1/paso6.png')

    def test_verificar_detalle_institucion(self):
        """
        Podré ver los datos de dos maneras,
        una vista comparativa y una vista
        con más detalle de cada institución
        """
        self.browser.get('http://0.0.0.0:8000/tablero-instituciones/')

        # Verificar carga de interfaz de usuario
        self.assertEquals(self.browser.title, 'Tabla Comparativa')
         # Verificando existencia de instituciones en el tablero
        tabla_comparativa = self.browser.find_element_by_css_selector('table#apf_table')
        tbody_tabla_comparativa = tabla_comparativa.find_element_by_css_selector('tbody')
        titulos_tabla_comparativa = tabla_comparativa.find_element_by_css_selector('thead').find_elements_by_css_selector('td')
        filas_tabla_comparativa = tbody_tabla_comparativa.find_elements_by_css_selector('tr')
        self.assertTrue(len(filas_tabla_comparativa) > 0)
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_2/paso1.png')
        columnas = [
            {'nombre': u'Institución', 'tipo': str},
            {'nombre': u'Ranking', 'tipo': int},
            {'nombre': u'Datos', 'tipo': int},
            {'nombre': u'Calif. Apertura', 'tipo': str},
            {'nombre': u'Descargas', 'tipo': str},
            {'nombre': u'Calidad', 'tipo': str}
        ]

        input_buscar = self.browser.find_element_by_css_selector('input#searchbox')
        # Verificando titulos en la tabla 
        contador = 0
        for columna in titulos_tabla_comparativa:
            self.assertIn(columnas[contador]['nombre'], columna.text)
            contador += 1

        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_2/paso2.png')
        # Verificando paginacion de tabla
        botones_paginacion = [boton.get_attribute('data-dt-idx') for boton in self.browser.find_elements_by_css_selector('a.paginate_button')]
        tbody_tabla_comparativa = tabla_comparativa.find_element_by_css_selector('tbody')

        for pagina in botones_paginacion[:5]:
            boton = self.browser.find_element_by_css_selector('a.paginate_button[data-dt-idx="{0}"]'.format(pagina))
            if boton.text not in 'Anterior' and boton.text not in 'Siguiente':
                pagina = boton.text
                self.assertEquals(int(boton.text), int(boton.get_attribute('data-dt-idx')))
                boton.click()
                self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_2/paso3_{0}.png'.format(pagina))
                # self.assertIn('current', self.browser.find_element_by_css_selector('a.paginate_button[data-dt-idx="{0}"]'.format(pagina)).get_attribute('class'))

        # Verificando busqueda
        input_buscar.send_keys('SE')
        for fila in self.browser.find_element_by_css_selector('table#apf_table').find_element_by_css_selector('tbody').find_elements_by_css_selector('tr'):
            self.assertIn('SE', fila.find_element_by_css_selector('td.depenTitle').text)
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_2/paso4.png')
            
        self.browser.find_element_by_css_selector('table#apf_table').find_element_by_css_selector('tbody').find_elements_by_css_selector('tr')[0].click()
        self.browser.save_screenshot('/home/frank/Functional Test/Entregable_13/Historia_2/paso5.png')

if __name__ == "__main__":
    unittest.main()
