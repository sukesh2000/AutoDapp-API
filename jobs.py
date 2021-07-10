from pytezos import ContractInterface
from pytezos.operation.result import OperationResult
from pytezos import pytezos
from rq.decorators import job
from server.main.rq_helpers import redis_connection
from server.config import DevelopmentConfig
import os

pytezos = pytezos.using(key=DevelopmentConfig.KEY, shell=DevelopmentConfig.SHELL)
maincont = pytezos.contract(DevelopmentConfig.MAINCONTRACT)

def originate(contract):
    cont = pytezos.origination(script=contract.script()).autofill().sign().inject(_async=False)
    while True:
        try:
            opg = pytezos.shell.blocks[cont['branch']:].find_operation(cont['hash'])
            res = OperationResult.from_operation_group(opg)
            return res[0].originated_contracts[0]
        except Exception:
            continue


@job('default', connection=redis_connection)
def storedetails(caseno, name, age,  gender, date):
    try:
        storedContract = pytezos.contract(maincont.storage['main'][caseno]())
        return storedContract.address
    except Exception:
        pass
    contract = pytezos.contract(originate(ContractInterface.from_file(os.path.join('server', 'main', 'contracts', 'h36casedetails.tz'))))
    maincont.default({"address":contract.address, "caseno":caseno}).inject(_async=False)
    contract.register({'age':age, 'date':date, 'gender':gender, 'name':name}).inject(_async=False)
    while True:
        try:
            storedContract = pytezos.contract(maincont.storage['main'][caseno]())
            return storedContract.address
        except Exception:
            continue


@job('default', connection=redis_connection, timeout='30m')
def storedoc(doctype, caseno):
    casedetails = pytezos.contract(maincont.storage['main'][caseno]())
    try:
        casedetails.storage['cont'][doctype]()
        return "Already stored {}".format(doctype)
    except Exception:
        pass
    doc = ''
    with open(os.path.join('uploads', doctype), 'r') as d:
        doc = str(d.read())
        d.close()
    chunk_size = 16000
    chunks = len(doc)
    lst = [doc[i:i+chunk_size] for i in range(0, chunks, chunk_size)]
    print(len(lst), len(lst[0]))
    for i in lst:
        contract = pytezos.contract(originate(ContractInterface.from_file(os.path.join('server','main','contracts','h36base64.tz'))))
        casedetails.registerdoc({"address": contract.address,"doc": doctype}).inject(_async=False)
        contract.default(i).inject(_async=False)
        print(contract.address)
    print("\n")
    return "Stored {}".format(doctype)


def retrieve_data(caseno, doctype):
    casedetails = pytezos.contract(maincont.storage['main'][caseno]())
    lst = casedetails.storage['cont'][doctype]()[::-1]
    string = str()
    for i in lst:
        string += pytezos.contract(i).storage()
    
    data = {'name':casedetails.storage['name'](), 'age':casedetails.storage['age'](), 
            'date':casedetails.storage['date'](), 'gender':casedetails.storage['gender'](), doctype:string}
    return data


def getcases():
    return maincont.storage['contracts']()
