#-*- coding:utf-8 -*-
from suds.client import Client
import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.INFO)

class Sfis(object):

    def __init__(self, *args, **kwargs):
        super(Sfis, self).__init__()
        self.args = args
        self.client = Client(
            #url='http://sh-sftest-01/KIRIN_MULTIDB_FAE_WIP/KIRIN_MULTIDB_FAE_WIP.asmx?WSDL'
            url='http://psh-sfap-07/KIRIN_MULTIDB_FAE_WIP/KIRIN_MULTIDB_FAE_WIP.asmx?WSDL'
        )

    def isninfo(self, isn):
        result = self.client.service.ISNINFODATA(isn)
        if len(result.string) == 1:
            #print(result.string[0])
            return [1, result.string[0]]
        else:
            header = str(result.string[0]).split(',')
            content = str(result.string[1]).replace('{', '').replace('}', '').split(',')
            value = dict(zip(header, content))
            #print(value)
            return [0, value]

    def utk(self, isn):
        result = self.client.service.UTKDATA(isn)
        if len(result.string) == 1:
           #print(result.string[0])
           return [1, result.string[0]]
        else:
           #print(result.string)
           header = str(result.string[0]).split(',')
           content = str(result.string[1]).replace('{', '').replace('}', '').split(',')
           value = dict(zip(header, content))
           #print(value)
           return [0, value]
   
    def error(self, isn, grpnm):
        result = self.client.service.PDCADATA(ISN=isn, GRPNM=grpnm)
        if len(result.string) == 1:
           #print(result.string[0])
           return [1, result.string[0]]
        else:
           header = str(result.string[0]).split(',')
           content = str(result.string[1]).replace('{', '').replace('}', '').split(',')
           value = dict(zip(header, content))
           #print(value)
           return [0, value]

    def modd(self, isn):
        result = self.client.service.MODDATA(isn)
        if len(result.string) == 1:
           #print(result.string[0])
           return [1, result.string[0]]
        else:
           header = str(result.string[0]).split(',')
           content = str(result.string[1]).replace('{', '').replace('}', '').split(',')
           value = dict(zip(header, content))
           #print(value)
           return [0, value]

if __name__ == '__main__':
    isns = ['C7CRC004H7YQ', 'C7CQ9001DD7V', 'C7CQD00KGX6C', 'C7CQD00ZGX6C']
    s = Sfis()
    for isn in isns:
        s.isninfo(isn)
        s.utk(isn)
        s.error(isn,'CT1')
        s.modd(isn)
