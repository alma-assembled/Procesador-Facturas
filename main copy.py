import os
import platform
import msvcrt
from colorama import init, Fore, Back, Style
from Models.opModel import opModel 
from Models.CuentasCobrar import ModelFacturasCobrar , CuentasPorCobrar 
from Models.modelHorras import ModelHoras
from datetime import timedelta
from Models.CuentrasPagar import ModelFacturasPagar
from Models.produccion import Produccion

class main ():
    def __init__(self) -> None:
        mi_os = platform.system()
        if mi_os == "Windows":
            self.pantalla_limpia = 'cls'
        elif mi_os == "Linux":
            self.pantalla_limpia = 'clear'
        self.pantalla_limpia = 'cls'   

    def porcentaje(self, cantidad, subtotal):
        '''
            Calcula el porcentaje de una cantidad con respecto a un subtotal.

            Args:
                cantidad (float): La cantidad para la cual se calculará el porcentaje.
                subtotal (float): El subtotal con respecto al cual se calculará el porcentaje.

            Returns:
                float: El porcentaje calculado. Si el subtotal es cero, retorna 0.
        ''' 
        if subtotal != 0:
            porcentaje = (cantidad * 100) / subtotal
            return porcentaje
        else:
            # Evitar la división por cero, retorna 0 si el subtotal es cero
            return 0
     
    def main(self):
        self.modelOp = opModel()
        self.modelCobrar = ModelFacturasCobrar()
        self.modelPagar = ModelFacturasPagar()
        self.ModelFacturas = CuentasPorCobrar()
        self.modelHoras = ModelHoras()
        self.produccion = Produccion()

        while True:
            try:
                os.system(self.pantalla_limpia)

                print(Fore.WHITE + ". . : :RESUMEN DE UTILIDAD DE OPS: : . .\n")
                print(f"1. RESUMEN OP")
                print("2. POCENTAJE POR OP")
                print(f"9. SALIR")
                numero = int(input("\nElige una opcion...\n"))


                if numero ==  1 :
                    op_folio = str(input("INGRESA EL FOLIO DE LA OP: "))
                    print("--------------------------------------")
                    opDatos=self.modelOp.ConsultaOpByFolio(op_folio)
                    print(Fore.WHITE +"Folio: "+Fore.GREEN + str(opDatos[1]))
                    print(Fore.WHITE +"Cliente: "+Fore.GREEN + self.modelOp.ConsultaClienteOp(op_folio)[0])  
                    print(Fore.WHITE +"Nombre: "+Fore.GREEN + str(opDatos[2]))
                    print(Fore.WHITE +"Fecha liberacion: "+Fore.GREEN + str(opDatos[4]))                    
                    print(Fore.WHITE +"Fecha entega: "+Fore.GREEN + str(opDatos[3]))

                    print(Fore.WHITE +"------------Productos ---------")
                    productos = self.modelOp.ConsultaProductos(op_folio)
                    for producto in  productos : 
                        print(Fore.GREEN +producto[0])
                    
                    print(Fore.WHITE +"------Productos Facturados-----")
                    productosFacturados, json = self.modelCobrar.facturasCobraroP(op_folio)
                    for producto in  productosFacturados :
                        if producto[2] == 'E':
                            print(Fore.WHITE +str( producto[5]))
                            print(Fore.WHITE +"Cantidad: "+Fore.GREEN + str(producto[6]))
                            print(Fore.WHITE +"Precio unitario: "+Fore.GREEN + str(producto[7]))
                            print(Fore.WHITE +"Subtotal : "+Fore.GREEN + str(producto[8]))
                            print("")
                        elif producto[2] == 'NC':
                            print("Nota credito:")
                            print(Fore.WHITE +str(producto[5]))
                            print("")

                    print(Fore.WHITE +"------------Gastos---------")
                    datos_pagar, jsonPagar =  self.modelPagar.facturasPagarDetalles(op_folio)
                    
                    ajustes, maquila, produccion  = self.produccion.totalProduccion("714")
                    
                    print("Ajustes : $",ajustes)
                    print("Maquila : $",maquila)
                    print("Produccion: $",produccion)
                    print(Fore.WHITE +"-----------Utilidad--------")
                    FacturasCobro = self.ModelFacturas.totalFacturasCobro(op_folio)
                    FacturasPago = 0
                    utilidad = FacturasCobro-FacturasPago
                    print("Subtotal: $"+ str(utilidad))
                    print("Porcentaje utilidad: "+str(self.porcentaje(utilidad,FacturasCobro))+"%")
                    
                elif numero ==2:
                    hora_inicio = '2023-09-01'
                    hora_fin = '2023-09-30'

                    suma_total_horas = self.modelHoras.total_horas(hora_inicio, hora_fin)
                    totales_horas = self.modelHoras.horasPorRangoFecha(hora_inicio, hora_fin)

                    suma = 0
                    for total_hora in  totales_horas :
                        horas = total_hora[0]
                        porcentaje = self.modelHoras.porcentajeHorasRangoFechas(suma_total_horas,horas)
                        print("op: ",total_hora[1], "porcentaje: ",porcentaje,"%")
                        suma+=porcentaje
                    print(suma,"%")
                elif numero == 9:
                    os.system(self.pantalla_limpia)
                    print("\nA D I O S\n")
                    break
                print(Fore.RED + "\nPresiona cualquier tecla para continuar...")
                msvcrt.getch()
            except ValueError:
                continue


if __name__ == "__main__":
     _main=main()
     _main.main()