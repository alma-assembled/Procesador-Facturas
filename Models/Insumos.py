import Models.connection as cn
import pymysql
import json
import decimal

class Insumos :
    def insumosOp(self, folioOp):
        self.c = cn.DataBase()
        try:
            x=f'''
            SELECT IA.INSUMO,  CIA.COSTO_UNIDAD, I.CANTIDAD, I.COSTO FROM 
            OPS.Base_InsumosProduccion I,
            OPS.Base_CostosInsumosAlmacen CIA,
            OPS.Catalogo_InsumosAlmacen IA,
            OPS.Base_OP OP
            WHERE 
            OP.FOLIO = {folioOp}
            AND OP.ID_BOP = I.ID_BOP
            AND I.ID_BCOSTOINSUMO = CIA.ID_BCOSTOINSUMO
            AND CIA.ID_CINSUMOALMACEN = CIA.ID_CINSUMOALMACEN ; 
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
          


class InsumosTotal(): 

    def __init__(self):
        self.model= Insumos()

    def totalInsumos(self, op):
        list, jsonInsumos =  self.model.insumosOp(op)
        total_normales = 0 
        subtotal = 0 
        for fila in list:
           subtotal += fila[3]
        return subtotal
    
        