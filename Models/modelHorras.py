import pymysql
import Models.connection as cn
from datetime import timedelta

class ModelHoras():
    def horasPorRangoFecha(self, hora_inicio, hora_fin):
        self.c = cn.DataBase()
        try:
            x='''
               SELECT  sec_to_time(sum(time_to_sec(TIMEDIFF(HORA_FIN, HORA_INICIO))))  AS Horas , OP FROM OPS.Base_TrabajosT 
                where (FECHA BETWEEN \''''+ hora_inicio +'''\' AND  \''''+hora_fin+'''\') and op != 0 and cantidad !=0 and ACTIVO=true  group by op ;
            '''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r = self.c.cursor.fetchall()
            return r
        except pymysql.Error as e: 
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.connection.close()

    def total_horas(self, hora_inicio, hora_fin):
        self.c = cn.DataBase()
        try:
            x='''
               SELECT  sec_to_time(sum(time_to_sec(TIMEDIFF(HORA_FIN, HORA_INICIO))))  AS Horas , OP FROM OPS.Base_TrabajosT 
                where (FECHA BETWEEN \''''+ hora_inicio +'''\' AND  \''''+hora_fin+'''\') and op != 0 and cantidad !=0 and ACTIVO=true  group by op ;
            '''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r = self.c.cursor.fetchall()

            suma_total_horas =timedelta(0)
            for total_hora in  r:
                suma_total_horas += total_hora[0]

            return suma_total_horas
        except pymysql.Error as e: 
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.connection.close()

    def porcentajeHorasRangoFechas(self, total_horas, horas):
        horas=int(horas.total_seconds())
        total_horas= int(total_horas.total_seconds())
        porcenje = (horas* 100) / int(total_horas)
        return porcenje
    