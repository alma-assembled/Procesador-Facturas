
import pymysql

class DataBase():

    def __init__(self):
        self.connection = pymysql.connect(
            host='192.168.1.200',
            #host='arp-assembled.c8ev10pyuzpv.us-east-1.rds.amazonaws.com',
            database ='OPS', 
            user = 'usuario',
            password ='#4ayN23*'
        )

        if(self.connection):
            self.cursor = self.connection.cursor()
            #print("La coneccion es correcta")
        else : 
            #print("La coneccion fallo")
            pass


def main():
    c = DataBase()

    return 0

if __name__=='__main__':
   main()