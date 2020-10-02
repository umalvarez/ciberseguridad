#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Security Scan
# Tools and commands: Nikto, Nmap, Curl and Whatweb
# Execute the script on Kali Linux
# Basic code developer for Gobierno del Estado de Queretaro

# Copyright (c) 2020, Marco Antonio Martínez García
# Copyright (c) 2020, Ulises M. Alvarez
# All rights reserved.

# Librerias
import sys, os, subprocess, time, shlex
import os.path as path
from subprocess import check_call,CalledProcessError,Popen,PIPE
from shlex import split

# Clases
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()

def run_command(cmd):
    process = Popen(split(cmd), stdout = PIPE, stderr = PIPE, encoding='utf8')
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None :
            break
        if output :
            print('output ',output.strip())
    rc = process.poll()
    return rc

def default():
   return "Opcion Invalida"

def switch(opevnik):
   sw = {
      1: "-evasion 1",
      2: "-evasion 2",
      3: "-evasion 3",
      4: "-evasion 4",
      5: "-evasion 5",
      6: "-evasion 6",
      7: "-evasion 7",
      8: "-evasion 8",
      9: "-evasion A",
      10: "-evasion B",
      11: "",
   }
   return sw.get(opevnik, default())


# Colores
# \033[cod_formato;cod_color_texto;cod_color_fondom
# Tabla de colores: for COLOR in {1..255}; do echo -en "\e[38;5;${COLOR}m${COLOR} "; done; echo;
crojo = "\033[1;31m"
cend = '\033[0;m'

# Variables
arr_ptos = []
arr_urls = []
dirscan = "./Analisis/"

# Validar que la carpeta /Seguridad/Analisis/ exista
if not path.exists(dirscan):
    # Si no existe se crea la carpeta
    #print("Crear carpeta")
    cmd_dir = "mkdir -p "+ dirscan
    returned_value_dir = os.system(cmd_dir)
    #print('returned value:', returned_value_dir)

# Sistema
psist = input("Nombre de Sistema sin espacios ?\n")
print ("\t")

# Archivo de Analisis
from datetime import datetime
ahora = datetime.now()
anio = ahora.year
mes = '{:02d}'.format(ahora.month)
dia = '{:02d}'.format(ahora.day)
hora = '{:02d}'.format(ahora.hour)
minutos = '{:02d}'.format(ahora.minute)
# Fecha y Hora
pfecha = str(dia) + str(mes) + str(anio)
phora = str(hora) + str(minutos)

# Menus
def menutscan():
    """
    Menu de Tipo de Escaneo
    """
#   os.system('clear')
    print ("Que tipo de analisis desear realizar ?")
    print ("\t1 - Analisis Interno")
    print ("\t2 - Analisis Externo")
    print ("\t3 - salir")

def menuptosnmap():
    """
    Menu de puertos NMAP
    """
#    os.system('clear')
    print ("Que puertos deseas escanear en nmap ?")
    print ("\t1 - Todos")
    print ("\t2 - Puerto(s) especifico(s)")
    print ("\t3 - salir")

def menuevnikto():
    """
    Menu Nikto Metodo de Evasion
    """
#    os.system('clear')
    print ("Seleccione un metodo de evasion para el analisis de NIKTO")
    print ("\t1 - 1 Random URI encoding (non-UTF8)")
    print ("\t2 - 2 Directory self-reference (/./)")
    print ("\t3 - 3 Premature URL ending")
    print ("\t4 - 4 Prepend long random string")
    print ("\t5 - 5 Fake parameter")
    print ("\t6 - 6 TAB as request spacer")
    print ("\t7 - 7 Change the case of the URL")
    print ("\t8 - 8 Use Windows directory separator ()")
    print ("\t9 - A Use a carriage return (0x0d) as a request spacer")
    print ("\t10 - B Use binary value 0x0b as a request spacer")
    print ("\t11 - Ninguno")

# |--- Preguntas ---|

# Ip/Dominio sistema
pinput = input("Coloque la ip del sistema ó dominio del sistema a analizar sin el protocolo HTTP/HTTPS:\n")
print ("\t")

# Puertos
#numptos = int(input('Numero de puertos donde se ejecuta el sistema ?:\n '))
#for i in range(1, numptos+1):
#    print('Escribe el puerto numero ', i, ': ')
#    n = str(input())
#    arr_ptos.append(n)

# Urls
numurls = int(input('Cuantas Urls vas a analizar del servidor: '))
print ("\t")
for i in range(1, numurls+1):
    print('Escribe la URL numero ' , i, ': ')
    n = str(input())
    arr_urls.append(n)
print ("\t")
#numurls = 1 # DEBUG
#arr_urls.append("http://172.43.1.140/digitalizacion/") # DEBUG

# Tipo de analisis
while True:
    menutscan()
    ptsist = input("Selecciona una opcion -> ")
    if ptsist == '1':
        ptsist = "interno"
    else:
        ptsist = "externo"
    break
print ("\t")
#ptsist = "interno" # DEBUG

#Puertos NMAP
while True:
    menuptosnmap()
    popc_ptsnmap = input("Selecciona una opcion -> ")
    break
print ("\t")

if popc_ptsnmap == '1':
    # Todos los puertos
    ptsnmap = "-p-"
else:
    # Puertos especificos
    ptsnmap = input("Escriba el puerto a escanear o los puertos a escanear separados por comas por ejemplo 80,443,22:\n" + cend)
    ptsnmap = "-p " + ptsnmap

##ptsnmap = "-p-" # DEBUG

# Metodo evasion Nikto
menuevnikto()
opevnik = int(input("Seleccione una opcion -> "))
evnik = switch(opevnik)
print ("\t")
#evnik = "" # DEBUG
#print(evnik)

# |--- INICIO DE ARCHIVO ---|
# Creacion de Archivo
parchivo = dirscan + psist + '_' + pfecha + '_' + phora + '_' + ptsist +'.txt'
f = open(parchivo, 'w')
orig_stdout = sys.stdout
sys.stdout = Tee(sys.stdout, f)
#with open(parchivo , 'w') as f:
#sys.stdout = f     # Sin mostrar salida en consola

# |--- ENCABEZADO ---|
print("############################################################################")
print("Analisis de Seguridad del sistema " + psist)
print("Realizado el dia " + str(dia) + "/" + str(mes) + "/" + str(anio) + " a las " + hora + ":" + minutos + " hrs")
print("Nombre del sistema: " + psist)
print("Ip/Dominio del sistema: " + pinput)
print ("Cantidad de Url(s): " + str(numurls) ,str(arr_urls))
print ("Puerto(s) Nmap: " + ptsnmap)

# |--- BODY---|
print("############################################################################")
# Ejecucion de comandos
print("Iniciando Analisis de Seguridad...\n")

# SERVIDOR
# Ejecucion de comandos nmap
"""
# Ssl-enum-ciphers
print("\nNmap Ssl-enum-ciphers")
print("============================================================================")
print("nmap -sV --script ssl-enum-ciphers "+ ptsnmap + " " + pinput)
#cmd_nmap_ciphers = "nmap -sV --script ssl-enum-ciphers "+ ptsnmap + " " + pip
#returned_value_ciphers = os.system(cmd_nmap_ciphers)
#print('returned value:', returned_value_ciphers)
try:
    t = str(time.ctime())
    print(t)
    run_command("nmap -sV --script ssl-enum-ciphers "+ ptsnmap + " " + pinput)
    #out = subprocess.check_output(['nmap',  '-sV', '--script','ssl-enum-ciphers',ptsnmap,pip])
    #msg = "{t}\nChecking for connected devices:\n{out}".format(t=t, out=out)
    ##out = subprocess.check_output("nmap -sV --script ssl-enum-ciphers "+ ptsnmap + " " + pip, shell=True)
    #print(type(out))
    ##out = out.decode("utf-8")
    #print(type(out))
    ##print(t)
    ##print(out)
    #f.write(t)
    #f.write(out)
except subprocess.CalledProcessError as cmdexc:
    print ("Error code:", cmdexc.returncode, cmdexc.output)
"""

# Nmap scan
print("\nNmap Scan")
print("============================================================================")
print("nmap -A -T4 -Pn --script=ssl-enum-ciphers,http-security-headers,http-waf-detect,vuln "+ ptsnmap + " " + pinput)
#cmd_nmap = "nmap -A -T4 -Pn "+ ptsnmap + " " + pip"
#returned_value_nmap = os.system(cmd_nmap)
#print('returned value:', returned_value_nmap)
try:
    t = str(time.ctime())
    print(t)
    run_command("nmap -A -T4 -Pn --script=ssl-enum-ciphers,http-security-headers,http-waf-detect,vuln "+ ptsnmap + " " + pinput)
    ##out = subprocess.check_output("nmap -A -T4 -Pn "+ ptsnmap + " " + pip, shell=True)
    ##out = out.decode("utf-8")
    ##print(t)
    ##print(out)
except subprocess.CalledProcessError as cmdexc:
    print ("Error code:", cmdexc.returncode, cmdexc.output)
"""
# Nmap scan
print("\nNmap vulscan")
print("============================================================================")
print("nmap -sV --script=vulscan/vulscan.nse "+ pip)
try:
    t = str(time.ctime())
    print(t)
    run_command("nmap -sV --script=vulscan/vulscan.nse "+ pip)
except subprocess.CalledProcessError as cmdexc:
    print ("Error code:", cmdexc.returncode, cmdexc.output)

# Nmap-vulners
print("\nNmap vulners")
print("============================================================================")
print("nmap --script nmap-vulners -sV "+ pip)
try:
    t = str(time.ctime())
    print(t)
    run_command("nmap --script nmap-vulners -sV "+ pip)
except subprocess.CalledProcessError as cmdexc:
    print ("Error code:", cmdexc.returncode, cmdexc.output)

# Nmap vuln
print("\nNmap vuln")
print("============================================================================")
print("nmap -Pn --script vuln "+ pip)
try:
    t = str(time.ctime())
    print(t)
    run_command("nmap -Pn --script vuln "+ pip)
except subprocess.CalledProcessError as cmdexc:
    print ("Error code:", cmdexc.returncode, cmdexc.output)

# SITIO URL
# WAF
print("\nWaf")
print("============================================================================")
for i in range(0, numurls):
    print("wafw00f "+ arr_urls[i])
    #cmd_waf = "wafw00f "+ arr_urls[i]
    #returned_value_waf = os.system(cmd_waf)
    #print('returned value:', returned_value_waf)
    try:
        t = str(time.ctime())
        print(t)
        run_command("wafw00f "+ arr_urls[i])
        ##out = subprocess.check_output("wafw00f "+ arr_urls[i], shell=True)
        ##out = out.decode("utf-8")
        ##print(t)
        ##print(out)
    except subprocess.CalledProcessError as cmdexc:
        print ("Error code:", cmdexc.returncode, cmdexc.output)
"""

# CURL
print("\nCurl")
print("============================================================================")
for i in range(0, numurls):
    print("curl -sk --head "+ arr_urls[i] + " -A firefox")
    #cmd_curl = "curl -sk --head "+ arr_urls[i] + " -A firefox"
    #returned_value_curl = os.system(cmd_curl)
    #print('returned value:', returned_value_curl)
    try:
        t = str(time.ctime())
        print(t)
        run_command("curl -sk --head "+ arr_urls[i] + " -A firefox")
        ##out = subprocess.check_output("curl -sk --head "+ arr_urls[i] + " -A firefox", shell=True)
        ##out = out.decode("utf-8")
        ##print(t)
        ##print(out)
    except subprocess.CalledProcessError as cmdexc:
        print ("Error code:", cmdexc.returncode, cmdexc.output)


# Whatweb
print("\nWhatweb")
print("============================================================================")
for i in range(0, numurls):
    print("whatweb -v -a 3 "+ arr_urls[i])
    #cmd_whatweb = "whatweb -v -a 3 "+ arr_urls[i]
    #returned_value_whatweb = os.system(cmd_whatweb)
    #print('returned value:', returned_value_whatweb)
    try:
        t = str(time.ctime())
        out = subprocess.check_output("whatweb -v -a 3 "+ arr_urls[i], shell=True)
        out = out.decode("utf-8")
        print(t)
        print(out)
    except subprocess.CalledProcessError as cmdexc:
        print ("Error code:", cmdexc.returncode, cmdexc.output)


# Nikto
print("\nNikto")
print("============================================================================")
for i in range(0, numurls):
    print("nikto -useragent Mozilla\/5\.0 "+ evnik +" -h " + arr_urls[i])
    #cmd_nikto = "nikto -h "+ arr_urls[i]
    #returned_value_nikto = os.system(cmd_nikto)
    #print('returned value:', returned_value_nikto)
    try:
        t = str(time.ctime())
        print(t)
        run_command("nikto -useragent Mozilla\/5\.0 "+ evnik +" -h " + arr_urls[i])
#        out = subprocess.check_output("nikto -h "+ arr_urls[i], shell=True)
#        out = out.decode("utf-8")
#        print(t)
#        print(out)
    except subprocess.CalledProcessError as cmdexc:
        print ("Error code:", cmdexc.returncode, cmdexc.output)

# |--- END---|
print("\n############################################################################\n")
print("Finaliza analisis de Seguridad...")
print("Archivo de analisis: " + parchivo)
print("Recuerda realizar tu analisis en el aplicativo Spartan con la(s) Url(s) indicadas " ,str(arr_urls))
print("Recuerda realizar tu analisis en Owasp Zap con la(s) Url(s) indicadas " ,str(arr_urls))

# Resultados
# DEBUG
#print("Sistema: " + psist)
#print("Ip del sistema: " + pip)
#print ("Puerto(s) del Sistema: " ,arr_ptos)
#print ('Url(s): ',arr_urls)
#print ("Tipo de analisis: " + ptsist)
#print("Puertos NMAP a escanear: " + ptsnmap)

# |--- FIN DE ARCHIVO ---|
# Cerrar archivo de analisis
sys.stdout = orig_stdout
f.close()
