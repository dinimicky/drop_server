## drop_server
### dropServer has 3 port
> Port 1 is to accept the command xml stream by TCP
> Port 2 is to send some xml stream to SUT according to the command by TCP
> Port 3 is to receive some xml stream from SUT by TCP, the xml streams will be write to some file.

## dropClient
### dropClient
> 1. send the command xml stream to dropServer accroding to the input parameters
> 2. receive the result (success/failure) of the command from dropServer


## What kind of command is specified?
### Request:
> Start:
> ```xml
>    <cmd>
>       <action>start</action>
>    </cmd>
>```


>  Stop:
> ```xml
>  <cmd>
>      <action>stop</action>
>  </cmd>
> ```

> intCfgX2:
> ```xml
> <cmd>
>     <action>intChgX2</action>
>     <x2IP>192.168.1.1</x2IP>
>     <x2Port>22345</x2Port>
> </cmd>
> ```

> intCfgX2X3:
> ```xml
> <cmd>
>     <action>intChgX2X3</action>
>     <x2IP>192.168.1.1</x2IP>
>     <x2Port>22345</x2Port>
>     <x3IP>192.168.1.1</x3IP>
>     <x3Port>32345</x3Port>
> </cmd>
> ```


> audReq:
> ```xml
> <cmd>
>     <action>audReq</action>
>     <uri>sip:123@163.com</uri>
> </cmd>
> ```

> audAll:
> ```xml
> <cmd>
>     <action>audAll</action>
> </cmd>
> ```

> addTarget:
> ```xml
> <cmd>
>     <action>addTgt</action>
>     <uri>sip:123@163.com</uri>
>     <ccReq>True</ccReq>
>     <lirid>1234</lirid>
> </cmd>
> ```

>  removeTarget:
> ```xml
>  <cmd>
>      <action>remTgt</action>
>      <uri>sip:123@163.com</uri>
>  </cmd>
> ```

>  updateTarget:
> ```xml
>  <cmd>
>      <action>updTgt</action>
>      <uri>sip:123@163.com</uri>
>      <ccReq>true</ccReq>
>      <lirid>1234</lirid>
>  </cmd>
> ```

###  Response:

```xml
 <cmd>
     <result>success/failure</result>
     <comment/>
 </cmd>   
```
