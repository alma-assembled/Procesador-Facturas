
import pymysql
import Models.connection as cn

class opModel:
    def __init__(self):
        #self.c = cn.DataBase()
        pass

    def ConsultaClienteOp(self, opFolio):
        self.c = cn.DataBase()
        try:           
            x='''SELECT `OPS`.`Catalogo_Clientes`.`RAZON_SOCIAL` 
                    FROM `OPS`.`Catalogo_Domicilios`,
                    `OPS`.`Base_OP`,
                    `OPS`.`Catalogo_Clientes`
                    WHERE `OPS`.`Base_OP`.`FOLIO`= '''+opFolio+'''
                    AND `OPS`.`Base_OP`.`ID_CDOMICILIO` = `OPS`.`Catalogo_Domicilios`.`ID_CDOMICILIO` 
                    AND `OPS`.`Catalogo_Domicilios`.`ID_CCLIENTE` = `OPS`.`Catalogo_Clientes`.`ID_CCLIENTE`;'''
            self.c.cursor.execute(x)
            self.c.connection.commit()
            r=self.c.cursor.fetchone()
            return r
        except  pymysql.Error as e:
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.cursor.close()

    
    def ConsultaProductos(self, op):
        self.c = cn.DataBase()
        try:           
          x='''SELECT `OPS`.`Base_Maquilas`.`PRODUCTO` AS `PRODUCTO` 
            FROM `OPS`.`Base_Maquilas`,`OPS`.`Base_OP` 
            WHERE `OPS`.`Base_Maquilas`.`ID_BOP`=`OPS`.`Base_OP`.`ID_BOP` 
            AND `OPS`.`Base_OP`.`FOLIO`= '''+op+'''
            AND `OPS`.`Base_Maquilas`.`ACTIVO` = TRUE 
            UNION SELECT `OPS`.`Base_Corrugados`.`NOMBRE` AS `PRODUCTO` 
            FROM `OPS`.`Base_Corrugados`,`OPS`.`Base_OP` 
            WHERE `OPS`.`Base_Corrugados`.`ID_BOP`=`OPS`.`Base_OP`.`ID_BOP` 
            AND `OPS`.`Base_OP`.`FOLIO`= '''+op+'''
            AND `OPS`.`Base_Corrugados`.`ACTIVO` = TRUE 
            UNION SELECT `OPS`.`Base_PC_Impresos`.`NOMBRE` AS `PRODUCTO` 
            FROM `OPS`.`Base_PC_Impresos`,`OPS`.`Base_OP` 
            WHERE `OPS`.`Base_PC_Impresos`.`ID_BOP`=`OPS`.`Base_OP`.`ID_BOP` 
            AND `OPS`.`Base_OP`.`FOLIO`= '''+op+'''
            AND `OPS`.`Base_PC_Impresos`.`ACTIVO` = TRUE;'''
          self.c.cursor.execute(x)
          self.c.connection.commit()
          r=self.c.cursor.fetchall()
          return r
        except  pymysql.Error as e:
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.cursor.close()


    def ConsultaOpByFolio(self, opFolio):
        self.c = cn.DataBase()
        try:           
          x="SELECT ID_BOP,  FOLIO, NOMBRE, FECHA_ENTREGA, FECHA_LIBERACION from `OPS`.`Base_OP` where  `FOLIO`= "+opFolio+";"
          self.c.cursor.execute(x)
          self.c.connection.commit()
          r=self.c.cursor.fetchone()
          return r
        except  pymysql.Error as e:
            print("Error:", e)
        finally:
            if hasattr(self, 'c'):
                self.c.cursor.close()
