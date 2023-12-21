import pandas as pd
import mysql.connector as sql
import numpy as np
import os
import Models.connection as cn
from datetime import datetime
from sqlalchemy import create_engine

class Produccion:
    def __init__(self):
        usr = 'mvaltamirano'
        pw = '#4Dmin_Aayn*'
        svr = 'arp-assembled.c8ev10pyuzpv.us-east-1.rds.amazonaws.com'
        pto = '3306'
        schem = 'OPS'
        metodo = 'mysql_native_password'
        cnx = 'mysql+mysqlconnector://{0}:{1}@{2}:{3}/{4}?auth_plugin={5}'
        cnx = cnx.format(usr, pw, svr, pto, schem, metodo)
        self.m_mysql = create_engine(cnx)
        self.encabezados=['NOMBRE','OP','PAGO','ID_SUPER']
        self.encabeza_0 = ['MAQUILADOR','ID_TRABAJO','OP','FECHA','CANTIDAD','PRECIO','ID_SUPER','SUPERVISOR']
        self.superv = [21,30,35]

    def totalProduccion(self, op):
        try:
                qry_OPs = f"""select
                    `E`.`NOMBRE` as MAQUILADOR,
                    `T`.`ID_BTRABAJOT` as ID_TRABAJO,
                    `T`.`OP` as OP,
                    `C`.`CLIENTE` as CLIENTE,
                    `T`.`PRODUCTO` as PRODUCTO,
                    `T`.`TRABAJO` as TRABAJO,
                    `T`.`FECHA` as FECHA,
                    `T`.`CANTIDAD` as CANTIDAD,
                    `T`.`PRECIO` as PRECIO,
                    `T`.`ID_CEMPLEADO` as ID_SUPER,
                    `S`.`NOMBRE` as SUPERVISOR
                from
                    `Base_MaquilaT` M,`Base_TrabajosT` T,`Catalogo_ClientesT` C,`Catalogo_Empleados` S,
                    `Catalogo_EmpleadosT` E
                where
                    `M`.`ID_CEMPLEADOT` = `E`.`ID_CEMPLEADOT`
                    and `M`.`ID_BTRABAJOT` = `T`.`ID_BTRABAJOT`
                    and `T`.`ID_CCLIENTET` = `C`.`ID_CCLIENTET`
                    and `T`.`ID_CEMPLEADO` = `S`.`ID_CEMPLEADO`
                    and `T`.`OP` = {op}
                    and `T`.`ACTIVO` = true
                ;"""

                # Generara Dataframe
                df_op = pd.read_sql_query(qry_OPs,self.m_mysql)
                df_op['FECHA'] = df_op['FECHA'].astype('datetime64[ns]')

                if not df_op.empty:
                    # Pagos con CANTIDAD en 0 - Ajustes
                    campos = ['ID_TRABAJO','PRECIO']
                    df_op_0 = df_op.query("CANTIDAD==0")[campos]
                    PxA = df_op_0.drop_duplicates()['PRECIO'].sum() # Pago por ajustes

                    # Pagos a Maquiladores
                    campos = ['ID_TRABAJO','CANTIDAD','PRECIO']
                    df_op_P = df_op.query("CANTIDAD>0")[campos]
                    df_op_P = df_op_P.drop_duplicates()
                    df_op_P['PAGADO'] = df_op_P['CANTIDAD']*df_op_P['PRECIO']
                    PxM = df_op_P['PAGADO'].sum() #Pago por Maquila

                    # Pagos a Supervisoras
                    df_xFec = df_op['FECHA']
                    df_xFec = df_xFec.drop_duplicates()

                    pagadoXOPSup = []
                    fecs =[]

                    for dia in df_xFec:
                        fecs.append(datetime.strftime(dia,"%Y-%m-%d"))
                    
                    for fec in fecs:
                        df_super = df_op.query(f"FECHA == '{fec}'")[self.encabeza_0]

                        pagos = []
                        for trabajo in df_super.itertuples():
                            cant_maq = int(df_super.query(f"ID_TRABAJO=={trabajo[2]}")['ID_TRABAJO'].value_counts().iloc[0])
                            new_record = [trabajo[1],trabajo[3],trabajo[5]*trabajo[6]/cant_maq,trabajo[7]]
                            pagos.append(new_record)

                        df_pagoXOP = pd.DataFrame(pagos)
                        df_pagoXOP.columns = self.encabezados

                        for sup in self.superv:
                            df_pagoXSup = df_pagoXOP.query(f"ID_SUPER=={sup}").groupby('NOMBRE')[['PAGO']].sum()
                            if not df_pagoXSup.empty:
                                maquilador = df_pagoXSup[df_pagoXSup['PAGO']==df_pagoXSup['PAGO'].max()].index
                                pagadoXOPSup.append(
                                    df_pagoXOP.query(f"ID_SUPER=={sup} and OP=={op} and NOMBRE=='{maquilador[0]}'")['PAGO'].sum()
                                )

                    PxS = sum(pagadoXOPSup) # Pago por supervisión

                    return PxA,PxM,PxS
        except ValueError:
            pass