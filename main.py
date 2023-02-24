# This is a sample Python script.
import os
from math import prod

import requests
from datetime import datetime
import json


runDate = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')

creatmapp = []

'''
Class createMapping
'''
class cMapping:
    def __init__(self, mapping, prodID, effDate, attName, attValue):
        self.mapping = mapping
        self.prodID = prodID
        self.effDate = effDate
        self.attName = attName
        self.attValue = attValue

    def getMapping(self):
        return self.mapping

    def getProdId(self):
        return self.prodID

    def getEffDate(self):
        return self.effDate

    def getAttName(self):
        return self.attName

    def getAttValue(self):
        return self.attValue

    def obj_mapping(self, mapping, prodID, effDate, attName, attValue):
        self.mapping = mapping
        self.prodID = prodID
        self.effDate = effDate
        self.attName = attName
        self.attValue = attValue


def generateLogFile(res, filename, operation, productId):

    fp = open(filename, 'a+')
    fp.write("#########################################\n")
    if operation == 'CreateProduct':
        fp.write("\nStatus Code: %s\n" % res.status_code)
        fp.write(res.text)

    if operation == 'deleteProduct' or operation == 'deleteMapping':
        if res.status_code == 200:
            fp.write("ProductID: %s deleted" % productId)
        else:
            fp.write("ProductID: %s" % productId)
        fp.write(res.text)
        fp.write("\nStatus Code: %s" % res.status_code)
    if operation == 'createMapping':
        for result in res:
            fp.write(result.text)
            fp.write("\nStatus Code: %s\n" % result.status_code)
    fp.write("\n#########################################\n")
    fp.close()


def move2Archive(operation):
    path = "archive"
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
    else:
        for file in os.listdir():
            if file.__contains__(operation):
                new_name = 'archive/' + file
                os.rename(file, new_name)
            else:
                pass

def createMapping_curl_aux(array_aux):

    json_str = "{ 'versionNumber' : -1, 'mappings': [ {"
    aux_str = ""
    for i in array_aux:
        aux_str = aux_str + "'" + 'productId' + "'" + ":" + i.getProdId() + ','
        aux_str = aux_str + "'" + 'enabled' + ":" + 'true,'
        aux_str = aux_str + "'" + 'effectiveDate' + "'" + ":" + i.getEffDate() + ','
        aux_str = aux_str + "'" + 'attributeName' + "'" + ":" + i.getAttName() + ','
        aux_str = aux_str + "'" + 'attributeValue' + "'" + ":" + i.getAttValue()

    json_str = json_str + aux_str + "]}"


def createMapping_curl(creatmapp):
    #flag = 0 : Unic json
    #flag = 1 : increment json struture
    #type = a: append
    #       i: insert


    API_ENDPOINT = "http://10.254.3.10:49321/pmapper/v1/mapping"

    headers = {
        "Content-Type": "application/json",
    }

    if len(creatmapp) == 1:
        data = {
            'versionNumber': -1,
            'mappings': [
                {
                    'productId': creatmapp[0].getProdId(),
                    'enabled': True,
                    'effectiveDate': creatmapp[0].getEffDate(),
                    'attributeName': creatmapp[0].getAttName(),
                    'attributeValue': creatmapp[0].getAttValue()
                }
            ]
        }

        json_data = json.dumps(data)
        try:
            r = requests.post(url=API_ENDPOINT, headers=headers, data=json_data)

        except:
            print("Error connecting to " + API_ENDPOINT)
            exit(-1)
    else:
        dict = {
            'versionNumber' : -1,
        }

        mapping = []
        map_aux = {}

        map_aux.update({'productId': creatmapp[0].getProdId()})
        map_aux.update({'enabled': True})
        map_aux.update({'effectiveDate': creatmapp[0].getEffDate()})
        map_aux.update({'attributeName': creatmapp[0].getAttName()})
        map_aux.update({'attributeValue': creatmapp[0].getAttValue()})

        for i in creatmapp:
            map_aux = {}
            map_aux.update({'productId' : i.getProdId()})
            map_aux.update({'enabled' : True})
            map_aux.update({'effectiveDate' : i.getEffDate()})
            map_aux.update({'attributeName' : i.getAttName()})
            map_aux.update({'attributeValue' : i.getAttValue()})
            mapping.append(map_aux)

        dict.update({'mappings' : mapping})
        json_data = json.dumps(dict)

        try:
            r = requests.post(url=API_ENDPOINT, headers=headers, data=json_data)
        except:
            print("Error connecting to " + API_ENDPOINT)
            exit(-1)

    return r

def createMapping():
    global creatmapp
    input_fileName = 'CreateMapping_1.csv'
    lines = readFile(input_fileName)

    productArr = []
    result = []

    create_prod = "createMapping"
    filename = "Output_createMapping_" + runDate + ".xml"
    print("File created: " + filename)

    j=0
    for i in lines:
        # ignore the first row
        elem = i.split(";")
        if j == 0:
            j = j + 1
            pass
        else:
            mappingId = elem[0]
            prodId = elem[1]
            effDate = elem[2]
            attName = elem[3]
            attValue = elem[4].replace("\n","")
            mapObj = cMapping(mappingId, prodId, effDate, attName, attValue)
            productArr.append(mapObj)


    i=0
    j=1
    prev = 0
    mapp_i = productArr[i].getMapping()
    mapp_j = productArr[j].getMapping()

    if mapp_i == mapp_j:
        creatmapp.append(productArr[i])
    else:
        creatmapp.append(productArr[i])
    i = j
    j += 1
    while j<=len(productArr):
        if j == len(productArr):
            mapp_i = productArr[i].getMapping()
            mapp_prev = productArr[prev].getMapping()
            if mapp_prev == mapp_i:
                creatmapp.append(productArr[i])
            else:
                res = createMapping_curl(creatmapp)
                result.append(res)
                creatmapp = []
                creatmapp.append(productArr[i])
                res = createMapping_curl(creatmapp)
                result.append(res)
            j+=1
        else:
            mapp_i = productArr[i].getMapping()
            mapp_j = productArr[j].getMapping()
            mapp_prev = productArr[prev].getMapping()
            if mapp_i == mapp_j and mapp_prev == mapp_i:
                creatmapp.append(productArr[i])
                prev = i
                i=j
                j+=1
            else:
                if mapp_prev == mapp_i:
                    creatmapp.append(productArr[i])
                else:
                    res = createMapping_curl(creatmapp)
                    result.append(res)
                    creatmapp = []
                    creatmapp.append(productArr[i])

                prev = i
                i=j
                j+=1


    generateLogFile(result, filename, create_prod, 1)


def deleteMapping_curl(productId):

    API_ENDPOINT = "http://100.254.3.10:49321/v1/product"
    data = {
        'productId': productId
    }

    try:
        r = requests.delete(url=API_ENDPOINT, data=data)
        return r
    except:
        print("DELETE PRODUCT: Erro connecting to " + API_ENDPOINT)
        exit(-1)

def deleteMapping():
    input_fileName = 'DeleteMapping.csv'
    lines = readFile(input_fileName)

    operation = "DeleteMapping"
    filename = "Output_deleteMapping_" + runDate + ".xml"
    print("File created: " + filename)

    j = 0
    for i in lines:
        elem = i.split(";")
        # ignore the first row
        if j == 0:
            j = j + 1
            pass
        else:
            productId = elem[0]
            res = deleteProduct_curl(productId)
            generateLogFile(res, filename, operation, productId)

def createProduct_curl(productId,productName, productType, description, effectiveDateprod, user,
                applicationName, universeName, name, value, attributeTypeDate):

    API_ENDPOINT = "http://10.254.3.10:49321/v1/product"

    headers = {
        "Content-Type": "application/json",
    }
    if name == "" and value == "":
        data = {
            'productId': productId,
            'productName': productName,
            'productType': productType,
            'description': description,
            'enabled': True,
            'effectiveDate': effectiveDateprod,
            "versionNumber": -1,
            'user': user,
            'applicationName': applicationName,
            'universeName': universeName
        }
    else:
        data = {
            'productId' : productId,
            'productName' : productName,
            'productType' : productType,
            'description' : description,
            'enabled' : True,
            'effectiveDate' : effectiveDateprod,
            "versionNumber": -1,
            'user' : user,
            'applicationName' : applicationName,
            'universeName' : universeName,
            'attributes' : [{
                'name' : name,
                'value' : value,
                'effectiveDate' : effectiveDateprod,
                'enabled': True
            }],
        }

    try:
        r = requests.post(url=API_ENDPOINT, headers=headers, data=json.dumps(data))
    except:
        print("Error connecting to " + API_ENDPOINT)
        exit(-1)

    return r


def createProduct():

    input_fileName = 'Createproduct_1.csv'
    lines = readFile(input_fileName)

    operation = "CreateProduct"
    filename = "Output_createProduct_" + runDate + ".xml"
    print("File created: " + filename)

    j=0
    for i in lines:
        elem = i.split(";")
        #ignore the first row
        if j == 0:
            j = j+1
            pass
        else:
            productId = elem[0]
            productName = elem[1]
            productType = elem[2]
            description = elem[3]
            effectiveDateprod = elem[4]
            user = elem[5]
            applicationName = elem[6]
            universeName = elem[7]
            name = elem[8]
            value = elem[9]
            attributeTypeDate = elem[10]
            res = createProduct_curl(productId,productName, productType, description, effectiveDateprod, user,
                applicationName, universeName, name, value, attributeTypeDate)
            generateLogFile(res, filename, operation, productId)


def deleteProduct_curl(productId, productName, productType, applicationName):

    API_ENDPOINT = "http://10.254.3.10:49321/v1/product"

    if applicationName.__contains__("CM+"):
       applicationName.replace("CM+","CM%2B")

    data = {
        'productId': productId,
        'productName' : productName,
        'productType' : productType,
        'applicationName' : applicationName,
        'versionNumber' : -1
    }

    try:
        r = requests.delete(url=API_ENDPOINT, data=data)
        return r
    except:
        print("DELETE PRODUCT: Erro connecting to " + API_ENDPOINT)
        exit(-1)


def deleteProduct():
    input_fileName = 'Deleteproduct.csv'
    lines = readFile(input_fileName)

    operation = "deleteProduct"
    filename = "Output_deleteProduct_" + runDate + ".xml"
    print("File created: " + filename)

    j = 0

    for i in lines:
        elem = i.split(";")
        # ignore the first row
        if j == 0:
            j = j + 1
            pass
        else:
            productId = elem[0]
            productName = elem[1]
            productType = elem[2]
            applicationName = elem[3].replace("\n","")
            res = deleteProduct_curl(productId, productName, productType, applicationName)
            generateLogFile(res, filename, operation, productId)

def readFile(fileName):
    try:
        print("Opening " + fileName)
        f1 = open(fileName, 'r')
        lines = f1.readlines()
        return lines
    except:
        print("Cannot read file")
        exit(-1)

def menu():

    print("##################################################")
    print("                                                  ")
    print("        Automated Onboarding Bulk Edition         ")
    print("                                                  ")
    print("##################################################")
    print("Please select on of the following options:        ")
    print("Create product        1")
    print("Delete product        2")
    print("Create mapping        3")
    print("Delete mapping        4")
    print("Exit                  0")
    op = int(input("Option: "))
    creatmapp = []

    if op == 1:
        move2Archive('createProduct')
        createProduct()
        #menu()
    elif op == 2:
        move2Archive('deleteProduct')
        deleteProduct()
        menu()
    elif op == 3:
        move2Archive('createMapping')
        createMapping()
        menu()
    elif op == 4:
        move2Archive('deleteMapping')
        deleteMapping()
        menu()
    elif op == 0:
        exit(0)
    else:
        print("Invalid option")
        menu()

if __name__ == '__main__':
    menu()