################################################################################
 # MIT License
 #
 # Copyright (c) 2019 surfaceS
 #
 # Permission is hereby granted, free of charge, to any person obtaining a copy
 # of this software and associated documentation files (the "Software"), to deal
 # in the Software without restriction, including without limitation the rights
 # to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 # copies of the Software, and to permit persons to whom the Software is
 # furnished to do so, subject to the following conditions:
 #
 # The above copyright notice and this permission notice shall be included in all
 # copies or substantial portions of the Software.
 #
 # THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 # IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 # FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 # AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 # LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 # OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 # SOFTWARE.
 ################################################################################
"""
 The ``Oscilloscope`` module
 ======================

 *Author:* [Jérémy Jayet](mailto:jeremy.jayet@epfl.ch)
 *Last modification:* 28.03.2019

 This module is a class to handle an oscilloscope connected with on the LAN.

 Support
 -------

 + LeCroy Wavesurfer 3024.

 """



BAUD_RATE = 115200
PORT = 1861

import visa
from pyvisa.resources import MessageBasedResource

import logging as log
import string
import numpy as np

log.basicConfig(level=log.DEBUG)

class Oscilloscope():
    def __init__(self, parent=None):
        pass

    def connect(self, ip:string="128.178.201.10"):
        # DOES NOT WORK
        # TODO: fix

        #visa.log_to_screen()

        self.rm = visa.ResourceManager()
        #self.osc = self.rm.open_resource(f'VICP::{ip}::INSTR', resource_pyclass=MessageBasedResource)
        self.osc = self.rm.open_resource(f'TCPIP0::{ip}::INSTR')
        self.osc.timeout = 5000
        #self.osc.set_visa_attribute(visa.attributes.VI_ATTR_IO_PROT,visa.constants.VI_PROT_4882_STRS)
        #self.osc.io_protocol = 4
        self.osc.clear()

        log.debug("HEADER disabling")
        self.write("COMM_HEADER OFF")
        log.debug("HEADER disabled")
        self.write(r"""vbs 'app.settodefaultsetup' """)
        #self.osc.read()

    def printID(self):
        #self.osc.write('AUTO_SETUP')
        log.debug("Getting identifier of the osc")
        r = self.query('*IDN?', 2)

        print(r)
        return r

    def write(self, command:string):
        self.osc.write(command)
        r = self.query(r"""vbs? 'return=app.WaitUntilIdle(5)' """)
        log.debug(r)

    def query(self, command:string, timeout:int=None):
        r = self.osc.query(command,timeout)

        log.info(r)
        return r


    def acquire(self):
        """
         function directly created from
         ``Oscilloscopes Remote Control and Automation Manual``

         .. todo:: Make it better.
         """

        self.write(r"""vbs 'app.acquisition.triggermode = "stopped" ' """)
        self.write(r"""vbs 'app.acquisition.trigger.edge.level = 0.435' """)
        self.write(r"""vbs 'app.acquisition.triggermode = "single" ' """)
        self.write(r"""vbs 'app.acquisition.horizontal.maximize = "50" ' """)
        self.write(r"""vbs 'app.measure.clearall ' """)
        self.write(r"""vbs 'app.measure.clearsweeps ' """)

        self.write(r"""vbs 'app.measure.showmeasure = true ' """)
        self.write(r"""vbs 'app.measure.statson = true ' """)
        self.write(r"""vbs 'app.measure.p1.view = true ' """)
        self.write(r"""vbs 'app.measure.p1.paramengine = "1" ' """)
        self.write(r"""vbs 'app.measure.p1.source1 = "C1" ' """)

        for i in range(0,10):
            r = self.query(r"""vbs? 'return=app.acquisition.acquire( 0.1 , True )' """)
            r = self.query(r"""vbs? 'return=app.WaitUntilIdle(5)' """)
            if r==0:
                print(f'Time out from WaitUntilIdle, return = {r}')

        variable = self.query(r"""vbs? 'return=app.measure.p1.out.result.value' """)
        print(f'variable = {variable}')


    def disconnect(self):
        self.osc.close()
        self.rm.close()
