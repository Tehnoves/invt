#***************************************************************************************************
'''
АВК ОМА Козырев С.А

23.04.18(старт)  26.04.18(получение данных) 27.04.18 (многопоточность для строгого интервала 2сек)
14.05.18 (finish)  из них 10 дней вынужденный отпуск  итого 10дней
17.05.18  конец отладки  V3.1

V 1.0      V 1.1     V 2.0  V3.0  V3.1

получение данных со СКИДОВ 9 10 и передача их на сервер
запуск асинхронного потока ожидания 5сек получение данных со СКИДов и далее по кругу
передача на сервер

'''
#***************************************************************************************************
from struct import *
from idlelib.multicall import r
import time
from datetime import datetime, date, timedelta   # import time
import snap7
import threading
import requests
import logging
                                            #a=123
                                            #print(bin(a))
                                            #print((-1024).to_bytes(10, byteorder='big', signed=True))
                                            #print(int.bit_length(a) )
                                            #print((1024).to_bytes(2, byteorder='big'))
                                            #print((1024).to_bytes(10, byteorder='big')
                                            #print(int.from_bytes(b'\x00\x10', byteorder='big'))
                                            #print(unpack('>f', b'<#\xd7\n'))
                                            #print(pack('>f',0.01))
                                            #print(pack('>L', 154))
                                            #print(unpack('>bb',b'\x01\x12'))
                                            #print(pack('>h', -12))
                                            #print(unpack('>h',b'\xff\xf4'))
SKID9  = '192.16.100.229'                                           
SKID10 = '192.16.100.232'
a =[1,2,3,4]

def two_sec ():
    global l
    time.sleep(5)
    l = 1

class Siemens (object):

    def __init__ ( self, host ):
        self.client = snap7.client.Client ()
        self.client.connect (host, 0x0, 0x0)  # 0,2

    def read_input ( self, i , adr):
        r = self.client.read_area (snap7.types.areas['DB'], adr, i, 2)  # PE
        return r[0]

    def read_markers ( self, i ):
        r = self.client.read_area (snap7.types.areas['MK'], 410, i, 2)  # 1064
        return r[0]


    def read_bit ( self, a ):
        r = self.client.read_area (snap7.types.areas['MK'], 0, a, 2)
        return r[0] 


    def write_output ( self, area, data ):
        data = bytearray ([0x01])
        r = self.client.write_area (snap7.types.areas['PA'], 0, 0, data)
        return r


    def close ( self ):
        self.client.disconnect ()
    
tmp = datetime.now()    
logger = logging.getLogger("диагностика")
logger.setLevel(logging.INFO)
    
    # create the logging file handler
fh = logging.FileHandler("new_snake.log")
 
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
    # add handler to logger object
logger.addHandler(fh)
logger.info("Program started сгодня: "+str(tmp))       
while True: 
    l = 0
    my_thread = threading.Thread(target=two_sec, name='two', args=())
    my_thread.start()      
    try:    
        
        tmp = datetime.now()
        
        s7 = Siemens (SKID9)
        print ('SKID9  - подключен')
        a[0] =  (s7.read_input (20, 333))
        a[1] =  (s7.read_input (21, 333))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        print(' вес компонента 1 : ',tt,' кг')
        #logger.info(" вес K1: " + str(tmp)+"  :"+ tt+"кг")   # +"  :"+ tt "= +"кг"
        buf = tt
        a[0] =  (s7.read_input (22, 333))
        a[1] =  (s7.read_input (23, 333))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf + '$' +tt
        #print (buf)
        print(' вес компонента 2 : ',tt,' кг')
        a[0] =  (s7.read_input (24, 333))
        a[1] =  (s7.read_input (25, 333))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf + '$' +tt
        #print (buf)
        print(' вес компонента 3 : ',tt,' кг')
        a[0] =  (s7.read_input (26, 333))
        a[1] =  (s7.read_input (27, 333))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' вес компонента 4 : ',tt,' кг')
        a[0] =  (s7.read_input (28, 333))
        a[1] =  (s7.read_input (29, 333))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' вес компонента 5 : ',tt,' кг')
        a[0] =  (s7.read_input (42, 31))
        a[1] =  (s7.read_input (43, 31))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' температура      : ',tt,' °C')                   #   DB31.DBW42 = piw288
        print(' ')
        
       
        a[0] =  (s7.read_markers (410))
        a[1] =  (s7.read_markers (411))
        #print(a[0])
        #print(a[1])
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' вес варочной                : ',tt,' кг')
        
        a[0] =  (s7.read_input (38, 41))
        a[1] =  (s7.read_input (39, 41))
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' буфер 1 вес : ',tt,' кг')
        a[0] =  (s7.read_input (38, 51))
        a[1] =  (s7.read_input (39, 51))
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' буфер 2 вес : ',tt,' кг')
        a[0] =  (s7.read_input (38, 61))
        a[1] =  (s7.read_input (39, 61))
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' буфер 3 вес : ',tt,' кг')
        a[0] =  (s7.read_input (10, 333))
        a[1] =  (s7.read_input (11, 333))
        #print(a[0])
        #print(a[1])
        ab=unpack('!H',pack('!B',a[0])+pack('!B',a[1]))
        #print (ab)
        #t=unpack('>B',pack('B',(a[0])))
        #print(t)
        tt='{:0=+5d}'.format(int((ab[0]*1000)/0x7fff))                    # 27.04.18
        buf = buf +'$'+tt
        #print (buf)
        print(' СКОРОСТЬ МЕШАЛКИ : ',tt,' %')
        
        '''
            СКИД9 : 192.16.100.229

        компонент 1		DB333.DBW20  
        компонент 2		DB333.DBW22
        компонент 3		DB333.DBW24
        компонент 4		DB333.DBW26
        компонент 5		DB333.DBW28
        температура /10	PIW288              # DB31.DBW42 = piw288
        Вес текущий		MW410
        буфер 1 вес		DB41.DBW38
        буфер 2 вес		DB51.DBW38
        буфер 3 вес		DB61.DBW38
        скорость мешалки	DB333.DBW10


        '''
        s7.close()
        #payload ={'key1':(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')}
        #payload #={'key1':('-0123$-0124$+0125$+0126$-0127$-0223$-0224$+0225$+0226$-0227$-0323')}payload
        payload={'key1':(buf)}
        #logger.info(" вес K1: " + str(tmp)+"  :"+ buf)                                                  #print(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')
        r = requests.get('http://10.3.2.19/skid9.php',params=payload)    	
    except:
        print ('Нет подключения  СКИД9 ')
        logger.info(" П О Т Е Р Я   С В Я З И  СКИД9    :"  + str(tmp)) 
    
    try:   
        s7 = Siemens (SKID10)
        '''
        СКИД10 : 192.16.100.232

        температура варки /10     PIW280                DB31.DBW30 = piw280
        задание температр варки   DB33.DBW76
        скорость мешалки	      DB33.DBW72
        температура  сироп задан  DB33.DBW74
        вес сиропа   /100	      DB21.DBW30
        температура сиропа  /10   PIW286                DB21.DBW46 = piw286
        вакуум текущее            MD182

        '''        
       
        print ('SKID10 - подключен')
        
        a[0] =  (s7.read_input (30, 31))                            # DB31.DBW30 = piw280
        a[1] =  (s7.read_input (31, 31))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = tt
        #print (buf)
        print(' температуры варки         : ',tt,' °C')         #   DB31.DBW30 = piw280
        
        a[0] =  (s7.read_input (76, 33))                            # задание температр варки   DB33.DBW76
        a[1] =  (s7.read_input (77, 33))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        
        print(' задание температуры варки : ',tt,' °C')
        
        a[0] =  (s7.read_input (72, 33))
        a[1] =  (s7.read_input (73, 33))
        #print(a)
        ab=unpack('!H',pack('!B',a[0])+pack('!B',a[1]))
        #t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(int((ab[0]*1000)/0x7fff))                    # 27.04.18                           # 27.04.18
        buf = buf +'$'+tt
        #print (buf)
        print(' СКОРОСТЬ МЕШАЛКИ          : ',tt,' %') 
        
        a[0] =  (s7.read_input (46, 21))                        #  DB21.DBW46 = piw286
        a[1] =  (s7.read_input (47, 21))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf) 
        print(' температуры сиропа        : ',tt,' °C')         #  DB21.DBW46 = piw286 
        
        
        a[0] =  (s7.read_input (74, 33))                        #  температура  сироп задан  DB33.DBW74
        a[1] =  (s7.read_input (75, 33))
        t=unpack('>H',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' задание температуры сиропа: ',tt,' °C')
        
        
               
        a[0] =  (s7.read_input (30, 21))                        #  DB21.DBW30
        a[1] =  (s7.read_input (31, 21))
        #print(a)
        t=unpack('>h',pack('B',(a[0]))+pack('B',(a[1])))
        tt='{:0=+5d}'.format(t[0])
        buf = buf +'$'+tt
        #print (buf)
        print(' вес сиропа                : ',tt,' кг')
        
        a[0] =  (s7.read_markers (182))
        a[1] =  (s7.read_markers (183))
        a[2] =  (s7.read_markers (184))
        a[3] =  (s7.read_markers (185))
              
        t=unpack('>f',pack('B',(a[0]))+pack('B',(a[1]))+pack('B',(a[2]))+pack('B',(a[3])))
        tt='{:0=+7.3f}'.format(t[0])
        #print(tt)
        buf = buf +'$'+tt
        #print (buf)
        print(' вакуум                    : ',tt,' bar')
        
        #payload ={'key1':(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')}
        #payload ={'key1':('-0123$-0124$+0125$+0126$-0127$-0223$-0224')}
        payload={'key1':(buf)}                                                                                                #print(t_qt_+'$+0000'+'$'+t_qqt_+'$'+t_t_+'$'+tt_t_+'$'+ttt_t_+'$'+tttt_t_+'$01')
        r = requests.get('http://10.3.2.19/skid10.php',params=payload)	       
       
        s7.close()
    except:
        print ('Нет подключения  СКИД10')    
        logger.info(" П О Т Е Р Я   С В Я З И  СКИД10   :"  + str(tmp)) 
    #time.sleep(5)
    while l == 0:
            continue
    print (" after 2sek :",(datetime.now()).ctime())  