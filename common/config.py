"""
All system constants and default values for some system variables are collected here.
Externally, this module is known as sysConstants.

"""
'''
drop_server
===========
dropServer has 3 port 
Port 1 is to accept the command xml stream by TCP
Port 2 is to send some xml stream to SUT according to the command by TCP
Port 3 is to receive some xml stream from SUT by TCP, the xml streams will be write to some file.

dropClient
==========
dropClient 
1. send the command xml stream to dropServer accroding to the input parameters
2. receive the result (success/failure) of the command from dropServer


What kind of command is specified?
 ========================================
 Request:
 ========================================
 Start:
 <cmd>
     <action>start</action>
 </cmd>

 Stop:
 <cmd>
     <action>stop</action>
 </cmd>

intChgX2:
<cmd>
    <action>intCfgX2</action>
    <x2IP>127.0.0.1</x2IP>
    <x2Port>11111<x2Port> 
</cmd>

intChgX2X3:
<cmd>
    <action>intCfgX2X3</action>
    <x2IP>127.0.0.1</x2IP>
    <x2Port>11111<x2Port>
    <x3IP>127.0.0.1</x3IP>
    <x3Port>22222<x3Port>    
</cmd>


audReq:
<cmd>
    <action>audTgtUri</action> 
    <uri>sip:123@163.com</uri>
</cmd>

audAll:
<cmd>
    <action>audAllTgt</action> 
</cmd>
addTarget:
<cmd>
    <action>addTgtUri</action>
    <uri>sip:123@163.com</uri>
    <ccReq>True</ccReq>
    <lirid>1234</lirid>
</cmd>


 removeTarget:
 <cmd>
     <action>remTgtUri</action>
     <uri>sip:123@163.com</uri>
 </cmd>
 
 updateTarget:
 <cmd>
     <action>updTgtUri</action>
     <uri>sip:123@163.com</uri>
     <ccReq>true</ccReq>
     <lirid>1234</lirid>
 </cmd>
 
 ========================================
 Response:
 ========================================
 <cmd>
     <result>success/failure</result>
 </cmd>   
'''
TargetTypes = ['uri', 'wuri', 'fni']
ActionDict = {'start' : [],
              'stop' : [],
              'intCfgX2' : ['x2IP', 'x2Port'],
              'intCfgX2X3' : ['x2IP', 'x2Port', 'x3IP', 'x3Port'],
              'audTgtUri' : [TargetTypes[0]],
              'audAllTgt' : [],
              'addTgtUri' : [TargetTypes[0], 'ccReq', 'lirid'],
              'remTgtUri' : [TargetTypes[0]],
              'updTgtUri' : [TargetTypes[0], 'ccReq', 'lirid'],
              'addTgtWildcardUri' : [TargetTypes[1], 'ccReq', 'lirid'],
              'remTgtWildcardUri' : [TargetTypes[1]],
              'updTgtWildcardUri' : [TargetTypes[1], 'ccReq', 'lirid'],
              'audTgtWildcardUri' : [TargetTypes[1]],
              'addTgtFNI' : [TargetTypes[2], 'ccReq', 'lirid'],
              'remTgtFNI' : [TargetTypes[2]],
              'updTgtFNI' : [TargetTypes[2], 'ccReq', 'lirid'],
              'audTgtFNI' : [TargetTypes[2]],
              
              }
import socket
def convertip(StrIP):
    return ("%02X%02X%02X%02X" % tuple(map(lambda x:ord(x), socket.inet_aton(StrIP))))


class Version(object):
    def __init__(self, major=1, minor=0):
        self.major = major
        self.minor = minor


localhost_ip = '127.0.0.1'

ipAddress_LITT = "127.0.0.1"
ipAddress_IAP  = "127.0.0.1"

x1InterfacePort = 21999
x2InterfacePort = 22345
x3InterfacePort = 32345
cmdServerPort = 33333

x2InterfaceLog = "./x2.log"
pingEnable = True
ping_timeout = 60
ping_delay = 30


#-------------------------------------------------
# LIC Object Identifier
# Values:    long values separated by .
# Example:    0.4.0.127.0.5.3.4.1
Lic_ObjectId = "0.4.0.127.0.5.3.4.1"
Lic_ProtObjectId = "0.4.0.127.0.5.3.1.1"
Lic_ProtVersion = Version(1,0)
Lic_AckRequired = False

#-------------------------------------------------
# LI_ADM Versions
# Values:    long values separated by | (pipe)
# Example:    1.0
LI_ADM_ObjectId = "0.4.0.127.0.5.3.1.1"
LI_ADM_Versions = Version(1,0)
LI_ADM_AckSupported = False

#-------------------------------------------------
# LI_IRI Versions
# Values:    long values separated by | (pipe)
# Example:    1.0
LI_IRI_ObjectId = "0.4.0.127.0.5.3.2.1"
LI_IRI_Versions = Version(1,0)
LI_IRI_AckSupported = True

#-------------------------------------------------
# LI_CC Versions
# Values:    long values separated by | (pipe)
# Example:    1.0
LI_CC_ObjectId = "0.4.0.127.0.5.3.3.1"
LI_CC_Versions  = Version(1,0)
LI_CC_AckSupported = False



#-------------------------------------------------
# AlarmMessages
# Values:    true, false

AlarmMessages = False

#-------------------------------------------------
# DataBaseSize
# Values:    [integer value]

DataBaseSize = 30000

#-------------------------------------------------
# InterfaceCOnfigurationResponseResult
# Values:    success, protocolError, otherFailure

InterfaceConfigurationResponseResult = "success"

#-------------------------------------------------
# MaxSupportedNumberOf_LI_ADM_Messages
# Values:    [integer value]

MaxSupportedNumberOf_X1_Messages = 3

#-------------------------------------------------
# MaxSupportedNumberOf_LI_IRI_Messages
# Values:    [integer value]

MaxSupportedNumberOf_X2_Messages = 4

#-------------------------------------------------
# SendingNodeType:
# Values:    mrf

#SendingNodeType = "mrf"

#-------------------------------------------------
# SendingNodeVersion:
# Values:    [integer value]

#MajorVersion = 3
#MinorVersion = 0

if __name__ == '__main__':
    ip = convertip('127.0.0.1')
    print ip
    print convertip(ip)