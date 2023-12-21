import json
import decimal
import pymysql
import Models.connection as cn

class  ModelFacturasCobrar() :
    def facturasCobraroP(self, folio_op):
        self.c = cn.DataBase()
        try:
            x='''
                SELECT  
                        FCXC.PAGADA,
                        FCXC.CANCELADA,
                        FCXC.TIPO_COMPROBANTE,
                        FCXC.ID_CMONEDA,
                        CXC.ID_BOP,
                        CXC.DESCRIPCION,
                        CXC.CANTIDAD,
                        CXC.PRECIO_UNITARIO,
                        CXC.IMPORTE
                FROM    
                        OPS.Base_ConceptosCxC CXC,
                        OPS.Base_FacturasCxC  FCXC,
                        OPS.Base_OP BOP
                WHERE  FCXC.ACTIVO = 1
                AND CXC.ACTIVO = 1
                AND BOP.FOLIO = '''+folio_op+'''
                AND BOP.ID_BOP = CXC.ID_BOP
                AND CXC.ID_BFACTURACXC = FCXC.ID_BFACTURACXC ;
            '''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r = self.c.cursor.fetchall()
            #print("R", r)
            # Obtener los nombres de las columnas
            columnas = [columna[0] for columna in self.c.cursor.description]

            # Convertir los resultados a una lista de diccionarios
            datos_json = [dict(zip(columnas, fila)) for fila in r]

            # Convertir la lista de diccionarios a formato JSON
            json_resultado = json.dumps(datos_json, indent=2, default=self.decimal_default)

            return r, json_resultado
            

        except pymysql.Error as e: 
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.connection.close()

        # Función de conversión personalizada para manejar Decimales
    
    def facturasCobraroDetalles(self, folio_op):
        self.c = cn.DataBase()
        try:
            x='''
                SELECT  
                    FCXC.ID_BFACTURACXC,
                    CXC.DESCRIPCION,
                    CXC.PRECIO_UNITARIO,
                    CXC.CANTIDAD,
                    CXC.IMPORTE,
                    FCXC.TIPO_COMPROBANTE,
                    FCXC.ID_CMONEDA,
                    CXC.ID_BOP
                FROM    
                        OPS.Base_ConceptosCxC CXC,
                        OPS.Base_FacturasCxC  FCXC,
                        OPS.Base_OP BOP
                WHERE  FCXC.ACTIVO = 1
                AND CXC.ACTIVO = 1
                AND BOP.FOLIO = '''+folio_op+'''
                AND BOP.ID_BOP = CXC.ID_BOP
                AND CXC.ID_BFACTURACXC = FCXC.ID_BFACTURACXC ;
            '''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r = self.c.cursor.fetchall()
            #print("R", r)
            # Obtener los nombres de las columnas
            columnas = [columna[0] for columna in self.c.cursor.description]

            # Convertir los resultados a una lista de diccionarios
            datos_json = [dict(zip(columnas, fila)) for fila in r]

            # Convertir la lista de diccionarios a formato JSON
            json_resultado = json.dumps(datos_json, indent=2, default=self.decimal_default)

            return r, json_resultado
            

        except pymysql.Error as e: 
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.connection.close()

    def decimal_default(self, obj):
        # Función de conversión personalizada para manejar Decimales
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError
        
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


class CuentasPorCobrar():
    def __init__(self):
        self.model= ModelFacturasCobrar()

    def totalFacturasCobro(self, opFolio):

        list, json = self.model.facturasCobraroP(opFolio)
        subtotalFacturas = 0  
        notasCreddito = 0
        tipo_moneda = 152 #moneda USD
        for conceptoFactura in list:
            importe = conceptoFactura[8]
            if conceptoFactura[3] == tipo_moneda :
                importe = self.conversion(importe)
            if conceptoFactura[2] == 'E':
              subtotalFacturas += importe
            elif conceptoFactura[2] == 'NC':
                notasCreddito += importe

        return subtotalFacturas - notasCreddito

    def conversion(self, subtotal):
        x= self.model.tipoCambio()
        tipoCambioFactura = x[0]
        tipoCambioPago = x[1]

        if tipoCambioPago > 0 :
            cambio = subtotal * tipoCambioPago
        else:
            cambio = subtotal * tipoCambioFactura 
        return cambio