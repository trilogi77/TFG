#! /usr/bin/python
#Packet sniffer in python for Linux
#Sniffs only incoming TCP packet

import socket, sys
from struct import *
from datetime import datetime,timedelta
import mysql.connector as mariadb
global mariadb_connection
mariadb_connection = mariadb.connect(user='Javier', password='ContrasenaTFG',host='localhost', database='TFG')
global cursor
cursor= mariadb_connection.cursor()

global idLista
idLista=0
global tamano
tamano=[]
global puerto
puerto=[]
global IpSource
IpSource=[]
global numero
numero=[]
global hora
hora=datetime.now()
minuto=timedelta(minutes=1)
global horaProxima
horaProxima=datetime.now()+minuto
print horaProxima
print hora
translate =''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])
def dump(src, length=16):
    result=''
    while src:
       s,src = src[:length],src[length:]
       hex = ' '.join(["%02X"%ord(x) for x in s])
       s = s.translate(translate)
       result += "%-*s %s\n" % (length*3,hex,s)
    return result


#create an INET, STREAMing socket
try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message '+ msg[1]
        sys.exit()


def reiniciarVariables():
    global idLista
    idLista=0
    global tamano
    tamano=[]
    global puerto
    puerto=[]
    global IpSource
    IpSource=[]
    global numero
    numero=[]
    global hora
    hora=datetime.now()
    minuto=timedelta(minutes=1)
    global horaProxima
    horaProxima=datetime.now()+minuto
    print horaProxima
    print hora


def Carga(IpSource, puerto, tamano, numero, hora):
    f=open('logs/UDP.log', 'ab')
    for count in range(0,idLista):
        anadir="""Insert into Trafico values(%s, %s, %s, %s, %s, %s)"""
        protocolo="UDP"
        try:
            datos=(IpSource[count], puerto[count], tamano[count], numero[count], hora, protocolo)
            cursor.execute(anadir, datos)
            mariadb_connection.commit()
            f.write("["+hora.strftime("%H:%M:%S")+"]"+"Carga:  "+ str(datos) +"---- "+"\n\n")
        except Exception as e:
            f.write( "["+hora.strftime("%H:%M:%S")+"]"+ "error de carga inesperado:  " + str(e))
    f.close()
    reiniciarVariables()





if __name__ == '__main__':
    print "empieza el while"
    while True:
        packet = s.recvfrom(65565)
        msg, sender= packet
        packet = packet[0]
        ip_header = packet[0:20]
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
        iph_length = ihl * 4
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
        tcp_header = packet[iph_length:iph_length+20]
        #now unpack them :)
        tcph = unpack('!HHLLBBHHH' , tcp_header)
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
        if idLista==0:
            tamano.append(int(len(msg)))
            puerto.append(dest_port)
            IpSource.append(s_addr)
            numero.append(1)
            idLista=idLista+1
        else:
            for count in range(0,idLista):

                if IpSource[count] == s_addr and  puerto[count]==dest_port:

                    tamano[count]=tamano[count]+int(len(msg))
                    numero[count]=numero[count]+1
                    break
                else:
                    if count==idLista-1:
                        tamano.append(int(len(msg)))
                        puerto.append(dest_port)
                        IpSource.append(s_addr)
                        numero.append(1)
                        idLista=idLista+1
        h_size = iph_length + tcph_length * 4
        data_size = len(packet) - h_size
        data = packet[h_size:]
        hora=datetime.now()
        if hora>=horaProxima:
            print "CARGA"
            Carga(IpSource, puerto, tamano, numero, hora) #call the function to charge in database
