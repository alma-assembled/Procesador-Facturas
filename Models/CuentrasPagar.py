import connection as cn
import pymysql

class consulta() :
    def datos(self):
        self.c = cn.DataBase()
        try:
            x='''
                SELECT  
                        OPCXP.ID_BOP,
                        OPCXP.ID_BCONCEPTOCXP,
                        OPCXP.PORCENTAJE, 
                        CXP.SUBTOTAL,
                        FCXP.ESTATUS, 
                        FCXP.ID_CMONEDA
                FROM     OPS.Base_ConceptosCxP CXP,
                        OPS.Base_ConceptosOPsCxP OPCXP,
                        OPS.Base_FacturasCxP  FCXP
                WHERE  OPCXP.ACTIVO = 1
                AND CXP.ACTIVO = 1
                AND FCXP.ACTIVO = 1
                AND OPCXP.ID_BOP = 852  
                AND OPCXP.ID_BCONCEPTOCXP = CXP.ID_BCONCEPTOCXP
                AND CXP.ID_BFACTURACXP = FCXP.ID_BFACTURACXP;
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

    def tipoCambio(self):
        self.c = cn.DataBase()
        try:
            x='''
                SELECT 
                TIPO_CAMBIOFACTURACION, 
                TIPO_CAMBIOPAGO
                FROM OPS.Base_TiposCambioCxP 
                WHERE
                  ID_BFACTURACXP = 852 AND ACTIVO=1 ;
            '''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r = self.c.cursor.fetchone()
            return r
        except pymysql.Error as e:
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.connection.close()


class main:

    def __init__(self):
        self.model= consulta()

    def totalFacturas(self):

        list = self.model.datos()
        total_normales = 0  
        for fila in list:
            if fila.estatus == 'N':
              subtotal = self.procentaje(100, 5000)  
            tipo_moneda = 152 #moneda USD
            if fila.ID_CMONEDA == tipo_moneda :
                subtotal = self.conversion(subtotal)


    def procentaje(self, porcentaje, subtotal):
        x = (subtotal * porcentaje) / 100 
        return x

    def conversion(self, subtotal):
        x= self.model.tipoCambio()
        tipoCambioFactura = x[0]
        tipoCambioPago = x[1]

        if tipoCambioPago > 0 :
            cambio = subtotal * tipoCambioPago
        else:
            cambio = subtotal * tipoCambioFactura 
        return cambio
        