﻿#!/usr/bin/env python2
import gdb
import time
import logging
import sys

def execute(command, from_tty = False, to_string = False):
    gdb.execute('{}'.format(command), from_tty, to_string)

def connect_to_server(tcp_port):
    execute('target remote localhost:{}'.format(tcp_port))
    execute('monitor reset')
    execute('set confirm off')

def load_elf():
    execute('load')

def run():
    execute('continue')

def next():
    execute('next')

def gdbquit():
    execute('quit')

def check_ret_value(ret_val):
    if ret_val == "0xfoodcafe":
        return 0
    else:
        return -1


########################################################################################
#Config
tcp_port   = 9999
iterations = 64


#GDB script
#Connect to server
connect_to_server(tcp_port)

#Create log file
logging.basicConfig(filename='emu-target.log',level=logging.DEBUG, filemode='w')
logging.info('------- Running GDB Test -----')

#Load object data base
load_elf()

#See also https://embeddedartistry.com/blog/2020/11/09/metal-gdb-controlling-gdb-through-python-scripts-with-the-gdb-python-api/

#Run the benchmark and verify the result
bp1 = gdb.Breakpoint('app_benchmark_get_standalone_result')
run()
my_value = gdb.parse_and_eval("app_benchmark_standalone_result")
time.sleep(0.5)
bp1.delete()
gdbquit()

# check the return gdb value
val_as_str = str(my_value)
val_as_hex = str(val_as_str)
check_is_ok = check_ret_value(val_as_hex)

if check_is_ok == 0:
    sys.exit(0)
else:
    sys.exit(-1)
