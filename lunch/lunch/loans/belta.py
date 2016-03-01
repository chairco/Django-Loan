#-*- coding:utf-8 -*-
from suds.client import Client
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.INFO)

'''
url='http://sh-sftest-01/KIRIN_MULTIDB_FAE_WIP/KIRIN_MULTIDB_FAE_WIP.asmx?WSDL'
client = Client(url)

# ISN INFO
result = client.service.ISNINFODATA('C7CQ9001DD7V')
print(result.string)
result = client.service.ISNINFODATA('C7CQ9004GX69')
print(result.string)

# MOD
result = client.service.MODDATA('C7CR309EH2FQ')
print(result.string)

# PDCAERROR
result = client.service.PDCADATA(ISN='C7CQD00ZGX6C', GRPNM="CT1")
print(result.string)
result = client.service.PDCADATA(ISN='C7CQD0KJGX6C', GRPNM='SA-FACT2')
print(result.string)

# UTK
result = client.service.UTKDATA('C7CQD00KGX6C')
print(str(result.string).encode('utf-8').decode('utf-8'))
#print(result.string[0])
#print(str(result.string[1]).encode('utf-8').decode('utf-8'))

result = client.service.UTKDATA('C7CQD00GGX6C')
print(str(result.string).encode('utf-8').decode('utf-8'))
'''
'''
devices = Device.objects.filter(request=loan)
for device in devices:
    pass
'''

def sfis_connect():
    from suds.client import Client
    url='http://sh-sftest-01/KIRIN_MULTIDB_FAE_WIP/KIRIN_MULTIDB_FAE_WIP.asmx?WSDL'
    try:
        client = Client(url)
    except Exception as e:
        sfis_connect()
    return client

class Sfis(object):

    def __init__(self, *args, **kwargs):
        super(Sfis, self).__init__()
        self.args = args
        self.client = Client(
            url='http://sh-sftest-01/KIRIN_MULTIDB_FAE_WIP/KIRIN_MULTIDB_FAE_WIP.asmx?WSDL'
        )

    def isninfo(self, isns=list()):
        for isn in isns:
            result = self.client.service.ISNINFODATA(isn)
            if len(result.string) == 1:
                print(result.string[0])
            else:
                header = str(result.string[0]).split(',')
                content = str(result.string[1]).replace('{', '').replace('}', '').split(',')
                value = dict(zip(header, content))
                print(value)

if __name__ == '__main__':
    isns = ['C7CQ9001DD7V', 'C7CQ9004GX69', 'C7CQ9004GX6']
    s = Sfis()
    s.isninfo(isns)