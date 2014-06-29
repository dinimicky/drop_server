'''
Created on 2013-8-23

@author: ezonghu
'''
from common import config
def start():
    Start = '''
    <LIC-Msg>
    <lic-ModuleID>%s</lic-ModuleID>
    <prot-ModuleID>%s</prot-ModuleID>
    <payload>
    <protocolNegotiation>
    <protocolProposal>
    <LIC-ProtocolProposal>
    <protocol>%s</protocol>
    <proposedProtocolVersions>
    <ProtocolVersion><major>%d</major><minor>%d</minor></ProtocolVersion>
    </proposedProtocolVersions>
    %s
    </LIC-ProtocolProposal>
    <LIC-ProtocolProposal>
    <protocol>%s</protocol>
    <proposedProtocolVersions>
    <ProtocolVersion><major>%d</major><minor>%d</minor></ProtocolVersion>
    </proposedProtocolVersions>
    %s
    </LIC-ProtocolProposal>
    <LIC-ProtocolProposal>
    <protocol>%s</protocol>
    <proposedProtocolVersions>
    <ProtocolVersion><major>%d</major><minor>%d</minor></ProtocolVersion>
    </proposedProtocolVersions>
    %s
    </LIC-ProtocolProposal>
    </protocolProposal>
    </protocolNegotiation>
    </payload>
    </LIC-Msg>
    '''
    ack = '<ack-request-supported/>'   
    return Start % (config.Lic_ObjectId, config.Lic_ProtObjectId, 
                    config.LI_ADM_ObjectId, config.LI_ADM_Versions.major, config.LI_ADM_Versions.minor, ack if config.LI_ADM_AckSupported else "",
                    config.LI_IRI_ObjectId, config.LI_IRI_Versions.major, config.LI_IRI_Versions.minor, ack if config.LI_IRI_AckSupported else "",
                    config.LI_CC_ObjectId, config.LI_CC_Versions.major, config.LI_CC_Versions.minor, ack if config.LI_CC_AckSupported else "")

def stop():
    Stop = '''
    <LIC-Msg>
          <lic-ModuleID>%s</lic-ModuleID>
          <prot-ModuleID>%s</prot-ModuleID>
          <protVersion><major>%d</major><minor>%d</minor></protVersion>
          <payload>
            <extPDU>
              <LI-ADM-Event>
                <lI-ADM-MessageSequence>
                  <endSessionRequest/>
                </lI-ADM-MessageSequence>
              </LI-ADM-Event>
            </extPDU>
          </payload>
    </LIC-Msg>
    '''
    return Stop % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor)
def intCfgX2(X2IP="C0A80E1D", X2Port=22345):
    IntCfg = '''
    <LIC-Msg>
    <lic-ModuleID>%s</lic-ModuleID>
    <prot-ModuleID>%s</prot-ModuleID>
    <protVersion><major>%d</major><minor>%d</minor></protVersion>
    <payload>
    <extPDU>
    <LI-ADM-Event>
    <lI-ADM-MessageSequence>
    <interfConfRequest>
    <maxNumberOf-LI-ADM-Messages>%d</maxNumberOf-LI-ADM-Messages>
    <maxNumberOf-LI-IRI-Messages>%d</maxNumberOf-LI-IRI-Messages>
    <x2InterfaceAddress><ipV4>%s</ipV4></x2InterfaceAddress>
    <x2InterfacePort>%d</x2InterfacePort>
    </interfConfRequest>
    </lI-ADM-MessageSequence>
    </LI-ADM-Event>
    </extPDU>
    </payload>
    </LIC-Msg>
    '''
    return IntCfg % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                     config.MaxSupportedNumberOf_X1_Messages, config.MaxSupportedNumberOf_X2_Messages,
                     X2IP, X2Port)

def intCfgX2X3(X2IP="C0A80E1D", X2Port=22345, 
          X3IP="C0A80E1D", X3Port=32345
          ):
    IntCfg = '''
    <LIC-Msg>
    <lic-ModuleID>%s</lic-ModuleID>
    <prot-ModuleID>%s</prot-ModuleID>
    <protVersion><major>%d</major><minor>%d</minor></protVersion>
    <payload>
    <extPDU>
    <LI-ADM-Event>
    <lI-ADM-MessageSequence>
    <interfConfRequest>
    <maxNumberOf-LI-ADM-Messages>%d</maxNumberOf-LI-ADM-Messages>
    <maxNumberOf-LI-IRI-Messages>%d</maxNumberOf-LI-IRI-Messages>
    <x2InterfaceAddress><ipV4>%s</ipV4></x2InterfaceAddress>
    <x2InterfacePort>%d</x2InterfacePort>
    <x3InterfaceAddress><ipV4>%s</ipV4></x3InterfaceAddress>
    <x3InterfacePort>%d</x3InterfacePort>
    </interfConfRequest>
    </lI-ADM-MessageSequence>
    </LI-ADM-Event>
    </extPDU>
    </payload>
    </LIC-Msg>
    '''
    return IntCfg % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                     config.MaxSupportedNumberOf_X1_Messages, config.MaxSupportedNumberOf_X2_Messages,
                     X2IP, X2Port, X3IP,X3Port)

def addTgtUri(seqNbr = 1,
          uri="sip:user_a@cscf.com", lirid = 1, cCRequired = True
          ):
    AddTgtUri = '''
    <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <extPDU>
      <LI-ADM-Event>
      <lI-ADM-MessageSequence>
        <addTargetRequest>
          <seqNbr>%d</seqNbr>
          <targetInfo>
            <targetId><uri>%s</uri></targetId>
            %s
            <lIRID>%d</lIRID>
          </targetInfo>
        </addTargetRequest>
      </lI-ADM-MessageSequence>
      </LI-ADM-Event>
    </extPDU>
      </payload>
    </LIC-Msg>    
    '''
    return AddTgtUri % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                        seqNbr, uri, '<cCRequired/>' if cCRequired else "", lirid )

        
def updTgtUri(seqNbr = 1,
          uri="sip:user_a@cscf.com", lirid = 1, cCRequired = True
          ):
    UpdTgtUri = '''
    <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <extPDU>
      <LI-ADM-Event>
      <lI-ADM-MessageSequence>
        <updateTargetRequest>
          <seqNbr>%d</seqNbr>
          <targetInfo>
            <targetId><uri>%s</uri></targetId>
            %s
            <lIRID>%d</lIRID>
          </targetInfo>
        </addTargetRequest>
      </lI-ADM-MessageSequence>
      </LI-ADM-Event>
    </extPDU>
      </payload>
    </LIC-Msg>    
    '''
    return UpdTgtUri % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                        seqNbr, uri, '<cCRequired/>' if cCRequired else "",lirid)
def remTgtUri(seqNbr = 1,
          uri="sip:user_a@cscf.com"):
    RemTgtUri = '''
    <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <extPDU>
      <LI-ADM-Event>
      <lI-ADM-MessageSequence>
        <removeTargetRequest>
          <seqNbr>%d</seqNbr>
          <targetId><uri>%s</uri></targetId>
        </removeTargetRequest>
      </lI-ADM-MessageSequence>
      </LI-ADM-Event>
    </extPDU>
      </payload>
    </LIC-Msg>
    '''
    return RemTgtUri % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                        seqNbr, uri)
    
def audTgtUri(SeqNbr=1, 
              uri="sip:user_a@cscf.com"):
    AudTgtUri = '''
    <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <extPDU>
      <LI-ADM-Event>
      <lI-ADM-MessageSequence>
        <auditRequest>
          <seqNbr>%d</seqNbr>
          <targetInfo>
            <targetId><uri>%s</uri></targetId>
          </targetInfo>
        </auditRequest>
      </lI-ADM-MessageSequence>
      </LI-ADM-Event>
    </extPDU>
      </payload>
    </LIC-Msg>
    '''
    return AudTgtUri % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                        SeqNbr, uri)

def audAllTgt(SeqNbr=1):
    AudAllTgt = '''
    <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <extPDU>
      <LI-ADM-Event>
      <lI-ADM-MessageSequence>
        <auditRequest>
          <seqNbr>%d</seqNbr>
          <allTargets/>
        </auditRequest>
      </lI-ADM-MessageSequence>
      </LI-ADM-Event>
    </extPDU>
      </payload>
    </LIC-Msg>
    '''
    return AudAllTgt % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                        SeqNbr)

def pingX1Req(SeqNbr=1):
    Ping = '''
     <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <ping>
      <pingType><pingRequest/></pingType>
      <seqNbr>%d</seqNbr>
    </ping>
      </payload>
    </LIC-Msg>   
    '''
    return Ping % (config.Lic_ObjectId, config.Lic_ProtObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor, 
                   SeqNbr)

def pingX2Resp(SeqNbr=1):
    Ping = '''
    <LIC-Msg>
      <lic-ModuleID>%s</lic-ModuleID>
      <prot-ModuleID>%s</prot-ModuleID>
      <protVersion><major>%d</major><minor>%d</minor></protVersion>
      <payload>
    <ping>
      <pingType><pingResponse/></pingType>
      <seqNbr>%d</seqNbr>
    </ping>
      </payload>
    </LIC-Msg>
    '''
    return Ping % (config.Lic_ObjectId, config.LI_IRI_ObjectId, config.Lic_ProtVersion.major, config.Lic_ProtVersion.minor,  
                   SeqNbr)

Start_Resp = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.1.1</prot-ModuleID>
   <payload>
      <protocolNegotiation>
         <protocolSelectionResult>
            <protocolSelectionList>
               <LIC-ProtocolSelection>
                  <protocol>0.4.0.127.0.5.3.1.1</protocol>
                  <selectedProtocolVersion>
                     <major>1</major>
                     <minor>0</minor>
                  </selectedProtocolVersion>
               </LIC-ProtocolSelection>
               <LIC-ProtocolSelection>
                  <protocol>0.4.0.127.0.5.3.2.1</protocol>
                  <selectedProtocolVersion>
                     <major>1</major>
                     <minor>0</minor>
                  </selectedProtocolVersion>
               </LIC-ProtocolSelection>
               <LIC-ProtocolSelection>
                  <protocol>0.4.0.127.0.5.3.3.1</protocol>
                  <selectedProtocolVersion>
                     <major>1</major>
                     <minor>0</minor>
                  </selectedProtocolVersion>
               </LIC-ProtocolSelection>
            </protocolSelectionList>
         </protocolSelectionResult>
      </protocolNegotiation>
   </payload>
</LIC-Msg>
'''
IntCfgX2_Resp = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.1.1</prot-ModuleID>
   <protVersion>
      <major>1</major>
      <minor>0</minor>
   </protVersion>
   <payload>
      <extPDU>
<LI-ADM-Event>
   <lI-ADM-MessageSequence>
      <interfConfResponse>
         <sendingNodeInfo>
            <sendingNodeType><mgc/></sendingNodeType>
            <sendingNodeVersion>
               <majorVersion>19</majorVersion>
               <minorVersion>3</minorVersion>
            </sendingNodeVersion>
         </sendingNodeInfo>
         <result><success/></result>
         <maxNumberOf-LI-ADM-Messages>5</maxNumberOf-LI-ADM-Messages>
         <warrant-info-valid/>
      </interfConfResponse>
   </lI-ADM-MessageSequence>
</LI-ADM-Event></extPDU>
   </payload>
</LIC-Msg>
'''
IntCfgX2X3_Resp = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.1.1</prot-ModuleID>
   <protVersion>
      <major>1</major>
      <minor>0</minor>
   </protVersion>
   <payload>
      <extPDU>
<LI-ADM-Event>
   <lI-ADM-MessageSequence>
      <interfConfResponse>
         <sendingNodeInfo>
            <sendingNodeType><mgc/></sendingNodeType>
            <sendingNodeVersion>
               <majorVersion>19</majorVersion>
               <minorVersion>3</minorVersion>
            </sendingNodeVersion>
         </sendingNodeInfo>
         <result><success/></result>
         <maxNumberOf-LI-ADM-Messages>5</maxNumberOf-LI-ADM-Messages>
         <warrant-info-valid/>
      </interfConfResponse>
   </lI-ADM-MessageSequence>
</LI-ADM-Event></extPDU>
   </payload>
</LIC-Msg>
'''    
X1_Ping_Resp = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.1.1</prot-ModuleID>
   <protVersion>
      <major>1</major>
      <minor>0</minor>
   </protVersion>
   <payload>
      <ping>
         <pingType><pingResponse/></pingType>
         <seqNbr>1</seqNbr>
      </ping>
   </payload>
</LIC-Msg>
'''
X1_Alarm = '''
<LIC-Msg>
   <lic-ModuleID>0.4.0.127.0.5.3.4.1</lic-ModuleID>
   <prot-ModuleID>0.4.0.127.0.5.3.1.1</prot-ModuleID>
   <protVersion>
      <major>1</major>
      <minor>0</minor>
   </protVersion>
   <payload>
      <extPDU>
<LI-ADM-Event>
   <lI-ADM-MessageSequence>
      <alarmNotification>
         <alarmDescription><x2communicationFault/></alarmDescription>
      </alarmNotification>
   </lI-ADM-MessageSequence>
</LI-ADM-Event></extPDU>
   </payload>
</LIC-Msg>
'''
if __name__ == "__main__":
    print start()
    print intCfgX2()
    print intCfgX2X3()
    print audAllTgt()
    print audTgtUri()
    print addTgtUri()
    print updTgtUri()
    print remTgtUri()
    print stop()
    
    print pingX1Req()
    print pingX2Resp()