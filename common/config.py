"""
All system constants and default values for some system variables are collected here.
Externally, this module is known as sysConstants.

Usage:
from li.system import *
iapIp  = sysConstants.ipAddress_IAP
x1port = sysConstants.x1InterfacePort
"""

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
pingEnable = False
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