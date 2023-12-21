import Models.connection as cn
import pymysql
import json
import decimal

class ModelFacturasPagar() :
    def facturasPagarDetalles(self,folioOp):
        self.c = cn.DataBase()
        try:
            x=f'''
            SELECT  
                    FCXP.ID_BFACTURACXP,
                    CXP.DESCRIPCION,
                    OPCXP.PORCENTAJE, 
                    CXP.PRECIO,
                    CC.CUENTA,
                    CG.GASTO,
                    FCXP.TIPO_COMPROBANTE,
                    BOP.FOLIO AS OP_FOLIO
            FROM     OPS.Base_ConceptosCxP CXP,
                    OPS.Base_ConceptosOPsCxP OPCXP,
                    OPS.Base_FacturasCxP  FCXP,
                    OPS.Base_OP BOP,
                    OPS.Catalogo_Gastos CG,
                    OPS.Catalogo_CuentasContables CC
            WHERE  OPCXP.ACTIVO = 1
            AND CXP.ACTIVO = 1
            AND FCXP.ACTIVO = 1
            AND BOP.FOLIO = {folioOp}
            AND BOP.ID_BOP =  OPCXP.ID_BOP
            AND OPCXP.ID_BCONCEPTOCXP = CXP.ID_BCONCEPTOCXP
            AND CXP.ID_BFACTURACXP = FCXP.ID_BFACTURACXP
            AND OPCXP.ID_CGASTO = CG.ID_CGASTO
            AND CXP.ID_CCUENTACONTABLE = CC.ID_CCUENTACONTABLE;
            '''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r = self.c.cursor.fetchall()

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


class CuentasPorpagar(): 

    def __init__(self):
        self.model= ModelFacturasPagar()

    def totalFacturas(self, op):
        list,  json = self.model.facturasPagarDetalles(op)
        total_normales = 0 
        subtotal = 0 
        for fila in list:
            if fila[6] == 'I':
              subtotal += fila[3] #self.procentaje(fila[2], fila[3])  
            tipo_moneda = 152 #moneda USD
            if 102 == tipo_moneda :
                subtotal = self.conversion(subtotal)
        return subtotal
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
        