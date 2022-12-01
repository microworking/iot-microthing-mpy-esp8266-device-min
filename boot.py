# This file is executed on every boot (including wake-boot from deepsleep)
#import webrepl
#webrepl.start()
#import uos
#uos.dupterm(None, 1) # disable REPL on UART(0)
#esp.osdebug(None)
import os
import sys
import gc
gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
import esp
import machine
import micropython
import time
import utime
import ubinascii
import network
import socket
import urequests
import ujson
import ussl
from machine import Timer
from machine import Pin, Signal
from umqttsimple import MQTTClient
gc.collect()
exec(open('commonhelper.py').read(),globals())
exec(open('httphandler.py').read(),globals())
exec(open('actionhandler.py').read(),globals())
exec(open('mqttservice.py').read(),globals())
exec(open('actionrequest.py').read(),globals())
exec(open('actionresponse.py').read(),globals())
exec(open('healthcheck.py').read(),globals())
exec(open('main.py').read(),globals())