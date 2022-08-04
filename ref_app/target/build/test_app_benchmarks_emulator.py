﻿#-------------------------------------------------------------------------------
# Name:        test_app_benchmarks_emulator.py
# Purpose:
#
# Author:      Christopher Kormanyos
#
# Created:     02/04/2021
#
# Copyright:   Copyright Christopher Kormanyos 2007 - 2022
#
# Licence:     Distributed under the Boost Software License,
#              Version 1.0. (See accompanying file LICENSE_1_0.txt
#              or copy at http://www.boost.org/LICENSE_1_0.txt)
#-------------------------------------------------------------------------------

#!/usr/bin/env python2

# import python packages
import gdb
import time
import logging
import sys


#-------------------------------------------------------------------------------
# --- class: qemu_emulator
#-------------------------------------------------------------------------------
class qemu_emulator:
    def __init__(self, tcp_port, iterations):
        self.tcp_port   = tcp_port
        self.iterations = iterations

    def initialize(self):
        self.connect_to_server(self.tcp_port)
        self.create_log_file()
        self.load_elf()

    def execute(self, command, from_tty = False, to_string = False):
        gdb.execute('{}'.format(command), from_tty, to_string)

    # Create log file
    def create_log_file(self):
        logging.basicConfig(filename='emu-target.log',level=logging.DEBUG, filemode='w')
        logging.info('------- Running GDB Test -----')

    # Connect to server
    def connect_to_server(self, tcp_port):
        self.execute('target remote localhost:{}'.format(tcp_port))
        self.execute('monitor reset')
        self.execute('set confirm off')

    # Load object data base
    def load_elf(self):
        self.execute('load')

    # Run the benchmark
    def run(self):
        self.execute('continue')

    def next(self):
        self.execute('next')

    def set_gdb_break_point(self):
        my_bp = gdb.Breakpoint('app_benchmark_get_standalone_result')
        return my_bp

    def delete_gdb_break_point(self, bp):
        bp.delete()

    def get_gdb_result(self):
       my_result = gdb.parse_and_eval("app_benchmark_standalone_result")
       return my_result

    # Check the gdb return value
    def check_ret_val_and_quit_gdb(self, gdb_val):
        val_as_str = str(gdb_val)
        val_as_hex = hex(int(val_as_str))

        # print the return value
        print("Result value as hex: " + val_as_str)

        if val_as_hex == "0xf00dcafa":
            sys.exit(0)
        else:
            sys.exit(-1)


#-------------------------------------------------------------------------------
# --- GDB Script starts here
# See also https://embeddedartistry.com/blog/2020/11/09/metal-gdb-controlling-gdb-through-python-scripts-with-the-gdb-python-api/
#-------------------------------------------------------------------------------

# Script Config
tcp_port   = 9999
iterations = 64

#create an object
obj = qemu_emulator(tcp_port, iterations)

# Initialize
obj.initialize()

# Set break point
bp1 = obj.set_gdb_break_point()

# Run the benchmark
obj.run()

# Get gdb result
my_value = obj.get_gdb_result()
time.sleep(0.5)

# Delete break point
obj.delete_gdb_break_point(bp1)

# Check the gdb result and quit
obj.check_ret_val_and_quit_gdb(my_value)
