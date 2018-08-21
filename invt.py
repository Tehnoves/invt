from   struct import *
import time
import requests
import pymodbus
import serial
import math
from   pymodbus.pdu import ModbusRequest
from   pymodbus.client.sync import ModbusSerialClient as ModbusClient #initialize a serial RTU client instance
from   pymodbus.transaction import ModbusRtuFramer

import logging
i=0
'''
 01.08.18 ОМА АВК Козырев С.А старт разработки
 стыковки IBM PC с INVT для экструдера 7
 03.10.18 The END 
 10.08.18 попытка запуститься под Ubuntu

'''
#logging.basicConfig()
#log = logging.getLogger()
#log.setLevel(logging.DEBUG)

#count= the number of registers to read
#unit= the slave unit this request is targeting
#address= the starting address to read from

client= ModbusClient(method = "rtu", port="/dev/usb6",stopbits = 1, bytesize = 8, parity = 'N', baudrate= 19200)
print (client)

while True:
                                                      #Connect to the serial modbus server
    connection = client.connect()
    print (connection)

                                                      #Starting add, num of reg toc read, slave unit.
    try:                                                                                    
        result = client.read_holding_registers(0x070b,4,unit= 3)
    except:
        print ("Ошибка адреса 0x070b")
   
    print(result)  
    print (client)
    assert (result.registers == [ 1 ] * 8 )    
    print(result.registers[0])   
    t=unpack('!f',pack('!H',result.registers[1])+pack('!H',result.registers[2]))
    print(type(t[0]))
    print(t[0])
    t2 = '{:0=+5d}'.format(math.trunc(result.registers[0]))
    print (t2)
    qt='{:+6.1f}'.format(result.registers[0]*0.1)
    qt_ = '{:0=4d}'.format(result.registers[0])
    #print (qt)
    #print (qt_)
    #print(t)
    i=i+1
    print(i)
    print('   -- INVT  №7  --')	
    print('температура IGBT:',qt,'°C')
    try:                                                                            
        result = client.read_holding_registers(0x070c,4,unit= 3)        # адреса 0x070c  07.12  температура ПЧ
    except:
        print ("Ошибка адреса 0x070c")    
    qt3='{:+6.1f}'.format(result.registers[0]*0.1)
    qt3_ = '{:0=4d}'.format(result.registers[0])
    #print(qt3_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"
    #print(inn)
    
    #print (qt1)
    print('температура   ПЧ:',qt3,'°C')
    try:                                                                            
        result = client.read_holding_registers(0x070e,4,unit= 3)        #   0x070e  07.14  наработка час
    except:
        print ("Ошибка адреса 0x070e")    
    qt1='{:=5d}'.format(result.registers[0])
    qt1_ = '{:0=4d}'.format(result.registers[0])
    #print(qt1_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"
    #print(inn)
    #print (qt1)
    print('время работы      :',qt1,'час')
    try:   
        #   0x110b 17.11  напряжение DC шины   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        result = client.read_holding_registers(0x110b,4,unit= 3)        
    except:
        print ("Ошибка адреса 0x110b")    
    qt2='{:6.1f}'.format(result.registers[0]*0.1)
    qt2_ = '{:0=4d}'.format(result.registers[0])
    #print(qt2_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"
    #print(inn)
    #print (qt1)
    print('напряжение  DC шины:',qt2,'в')
    try:   
        #   0x1101 17.01  выходная частота  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        result = client.read_holding_registers(0x1101,4,unit= 3)        
    except:
        print ("Ошибка адреса 0x1101")    
    qt4='{:6.1f}'.format(result.registers[0]*0.01)
    qt4_ = '{:0=4d}'.format(result.registers[0])
    #print(qt4_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"
    #print(inn)
    #print (qt1)
    print('частота    выходная:',qt4,'гц') 
    try:                                                                            
        result = client.read_holding_registers(0x1103,4,unit= 3)        #   0x1103  17.03  выходное напряжение
    except:
        print ("Ошибка адреса 0x1103")    
    qt5='{:6.1f}'.format(result.registers[0])
    qt5_ = '{:0=4d}'.format(result.registers[0])
    #print(qt5_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"
    #print(inn)
    #print (qt1)
    print('напряжение выходное:',qt5,'в')
    try:                                                                            
        result = client.read_holding_registers(0x1104,4,unit= 3)        #   0x1104
    except:
        print ("Ошибка адреса 0x1104")    
    qt6='{:6.1f}'.format(result.registers[0]*0.1)
    qt6_ = '{:0=4d}'.format(result.registers[0])
    #print(qt6_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"
    #print(inn)
    #print (qt1)
    print('ток        выходной:',qt6,'А')
    try:                                                                            
        result = client.read_holding_registers(0x1105,unit= 3)          #   0x1105
    except:
        print ("Ошибка адреса 0x1104")    
    qt7='{:6.1f}'.format(result.registers[0])
    qt7_ = '{:0=4d}'.format(result.registers[0])
    #print(qt7_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"
    #print(inn)
    #print (qt1)
    print('скорость вращения двигателя:',qt7,'об/мин')
    try:                                                                            
        result = client.read_holding_registers(0x1108,unit= 3)          #   0x1108
    except:
        print ("Ошибка адреса 0x1104")    
    qt8='{:6.1f}'.format(result.registers[0]*0.1)
    qt8_ = '{:0=4d}'.format(result.registers[0])
    #print(qt8_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"
    #print(inn)
    #print (qt1)
    print('мощность  двигателя:',qt8,'%')
    print('  --  Номинальные параметры  --')
    try:                                                                            
        result = client.read_holding_registers(0x1100,unit= 3)          #   0x1100
    except:
        print ("Ошибка адреса 0x1100")    
    qt9='{:6.1f}'.format(result.registers[0]*0.01)
    qt9_ = '{:0=4d}'.format(result.registers[0])
    #print(qt9_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"
    #print(inn)
    #print (qt1)
    print('заданная частота    двигателя:',qt9,'гц')
    try:                                                                            
        result = client.read_holding_registers(0x0202,unit= 3)          #   0x1101
    except:
        print ("Ошибка адреса 0x0202")    
    qt10='{:6.1f}'.format(result.registers[0]*0.01)
    qt10_ = '{:0=4d}'.format(result.registers[0])
    #print(qt10_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"+qt10_+"$"
    #print(inn)
    #print (qt1)
    print('номинальное частота двигателя:',qt10,'гц')
    try:                                                                            
        result = client.read_holding_registers(0x0204,unit= 3)          #   0x1103
    except:
        print ("Ошибка адреса 0x0204")    
    qt11='{:6.1f}'.format(result.registers[0])
    qt11_ = '{:0=4d}'.format(result.registers[0])
    #print(qt11_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"+qt10_+"$"+qt11_+"$"
    #print(inn)
    #print (qt1)
    print('номинальное        напряжение:',qt11,'в')
    try:                                                                            
        result = client.read_holding_registers(0x0203,unit= 3)          #   0x1103
    except:
        print ("Ошибка адреса 0x0203")    
    qt12='{:6.1f}'.format(result.registers[0])
    qt12_ = '{:0=4d}'.format(result.registers[0])
    #print(qt12_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"+qt10_+"$"+qt11_+"$"+qt12_+"$"
    #print(inn)
    #print (qt1)
    print('номинальные обороты двигателя:',qt12,'об/мин')
    try:                                                                            
        result = client.read_holding_registers(0x0205,unit= 3)          #   0x1104
    except:
        print ("Ошибка адреса 0x0205")    
    qt13='{:6.1f}'.format(result.registers[0]*0.1)
    qt13_ = '{:0=4d}'.format(result.registers[0])
    #print(qt13_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"+qt10_+"$"+qt11_+"$"+qt12_+"$"+qt13_+"$"
    #print(inn)
    #print (qt1)
    print('номинальный               ток:',qt13,'А')
    try:                                                                            
        result = client.read_holding_registers(0x0201,unit= 3)          #   0x1105
    except:
        print ("Ошибка адреса 0x0201")    
    qt14='{:6.1f}'.format(result.registers[0])
    qt14_ = '{:0=4d}'.format(result.registers[0]*10)
    #print(qt14_)
    #inn="1411043$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"+qt10_+"$"+qt11_+"$"+qt12_+"$"+qt13_+"$"+qt14_+"$"
    #print(inn)
    #print (qt1)
    print('номинальная мощность двигателя:',qt14,'квт')
    print()
    try:                                                                            
        result = client.read_holding_registers(0x071b,unit= 3)          #   0x071b
    except:
        print ("Ошибка адреса 0x071b")    
    qt15='{:=5d}'.format(result.registers[0])
    qt15_ = '{:0=4d}'.format(result.registers[0])
    #print(qt15_)
    #inn="17002301$"+qt_+"$"+qt3_+"$"+qt1_+"$"+qt2_+"$"+qt4_+"$"+qt5_+"$"+qt6_+"$"+qt7_+"$"+qt8_+"$"+qt9_+"$"+qt10_+"$"+qt11_+"$"+qt12_+"$"+qt13_+"$"+qt14_+"$"+qt15_
    #print(inn)
    #print (qt1)
    
    print('О Ш И Б К А               :',qt15)
    
    payload ={'name':('17002301$'+qt15_+'$'+qt3_+'$'+qt1_+'$'+qt14_+'$'+qt10_+'$'+qt12_+'$'+qt11_+'$'+qt13_+'$'+qt9_+'$'+qt4_+'$'+qt5_+'$'+qt6_+'$'+qt7_+'$'+qt_+'$'+qt8_+'$'+qt2_+'$0099$0007')}
    #print(payload)
    r = requests.get('http://10.3.2.19/Connect/invt.php',params=payload)
    
    '''
        payload ={'name':('17002301+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$'+t2_qt_+'$+0000'+'$'+t2_qqt_+'$01')}
        #print(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')
    r = requests.get('http://10.3.2.19/Connect/invt.php',params=name)	


    //$invt="=17002301$0001$0002$0003$0004$0005$0006$0007$0008$0009$0010$0011$0012$0013$0014$0015";
    
        $size_byte = (int)(substr($invt, 1, 2)); 
        $number_cpu = (int)(substr($invt, 3, 3)); 
        $sost_pack = (int)(substr($invt, 6, 1)); 
        $error = (int)(substr($invt, $a+1, 4)); ++++++++
        $temperature = (int)(substr($invt, $a1+1, 4));  +++++++++++++
        $time_work = (int)(substr($invt, $a2+1, 4));     +++++++++++
        $rated_power = (int)(substr($invt, $a3+1, 4));   +++++++++++
        $rated_frequency = (int)(substr($invt, $a4+1, 4));  ++++++++++++++
        $rated_speed = (int)(substr($invt, $a5+1, 4));        ++++++++++++
        $rated_voltage = (int)(substr($invt, $a6+1, 4));       ++++++++++
        $rated_current = (int)(substr($invt, $a7+1, 4));      ++++++++++
        $setting_frequency = (int)(substr($invt, $a8+1, 4));   ++++++++++~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        $output_frequency = (int)(substr($invt, $a9+1, 4));    ++++++++++
        $output_voltage = (int)(substr($invt, $a10+1, 4));      +++++++++++
        $output_current = (int)(substr($invt, $a11+1, 4));     ++++++++       qt6
        $rotation_speed = (int)(substr($invt, $a12+1, 4));     ++++++++       qt7
        $temperature_IGBT = (int)(substr($invt, $a13+1, 4));  +++++++++       qt 
        $power_engine = (int)(substr($invt, $a14+1, 4));   +++++++++++++BN    qt8 
        $voltage_DC = (int)(substr($invt, $a15+1, 4));                        qt2 
        $power = (int)(substr($invt, $a16+1, 4));
        $number_invt = (int)(substr($invt, $a17+1, 4));
    
    
    '''
    
    
    
    #print(type(result.registers[0]))
    time.sleep(5)
                                                                                        #Closes the underlying socket connection
client.close()
