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
    <action>intChg</action>
    <x2IP>127.0.0.1</x2IP>
    <x2Port>11111<x2Port> 
</cmd>

intChgX2X3:
<cmd>
    <action>intChg</action>
    <x2IP>127.0.0.1</x2IP>
    <x2Port>11111<x2Port>
    <x3IP>127.0.0.1</x3IP>
    <x3Port>22222<x3Port>    
</cmd>


audReq:
<cmd>
    <action>audReq</action> 
    <uri>sip:123@163.com</uri>
</cmd>

audAll:
<cmd>
    <action>audAll</action> 
    <uri>sip:123@163.com</uri>
</cmd>
addTarget:
<cmd>
    <action>addTgt</action>
    <uri>sip:123@163.com</uri>
    <ccReq>True</ccReq>
    <lirid>1234</lirid>
</cmd>


 removeTarget:
 <cmd>
     <action>remTgt</action>
     <uri>sip:123@163.com</uri>
 </cmd>
 
 updateTarget:
 <cmd>
     <action>updTgt</action>
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
