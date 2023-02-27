# This is a sample Python script.
import os
from math import prod

import requests
from datetime import datetime
import json



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

'''
Class createProduct
'''
class cProduct:
    def __init__(self, productId, productName,productType, description, effectiveDateprod,user, applicationName, universeName, name, value, attributeTypeDate):
        self.productId = productId
        self.productName = productName
        self.productType = productType
        self.description = description
        self.effectiveDateprod = effectiveDateprod
        self.user = user
        self.applicationName = applicationName
        self.universeName = universeName
        self.name = name
        self.value = value
        self.attributeTypeDate = attributeTypeDate


    def getProductId(self):
        return self.productId

    def getProductName(self):
        return self.productName

    def getProductType(self):
        return self.productType

    def getDescription(self):
        return self.description

    def getEffectiveDateprod(self):
        return self.effectiveDateprod

    def getUser(self):
        return self.user

    def getApplicationName(self):
        return self.applicationName

    def getUniverseName(self):
        return self.universeName

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getAttributeTypeDate(self):
        return self.attributeTypeDate

    def obj_createProduct(self, productId, productName,productType, description, effectiveDateprod,user, applicationName, universeName, name, value, attributeTypeDate):
        self.productId = productId
        self.productName = productName
        self.productType = productType
        self.description = description
        self.effectiveDateprod = effectiveDateprod
        self.user = user
        self.applicationName = applicationName
        self.universeName = universeName
        self.name = name
        self.value = value
        self.attributeTypeDate = attributeTypeDate.replace("\n","")


def generateLogFile(res, filename, operation, productId):
    fp = open(filename, 'a+')
    fp.write("#########################################\n")
    if operation == 'CreateProduct' or operation == 'createMapping':
        for result in res:
            fp.write(result.text)
            fp.write("\nStatus Code: %s\n" % result.status_code)
            fp.write("\n----------------------------------------\n")
    if operation == 'deleteProduct':
        if res.status_code == 200:
            fp.write("ProductID: %s deleted" % productId)
        fp.write(res.text)
        fp.write("\nStatus Code: %s" % res.status_code)
    if operation == 'deleteMapping':
            fp.write("canonicalId : %s " % productId)
            fp.write("Status Code: %s\n" % res.status_code)

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

def createMapping_curl(creatmapp):
    #flag = 0 : Unic json
    #flag = 1 : increment json struture
    #type = a: append
    #       i: insert


    API_ENDPOINT = "http://10.254.3.10:49121/pmapper/v1/mapping"

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
        print("")
        for i in creatmapp:
            print("getProdId: " + i.getProdId() + " getEffDate: " + i.getEffDate()  + " attributeName: " + i.getAttName() + "attributeValue: " + i.getAttValue() )

        json_data = json.dumps(data)
        try:
            r = requests.post(url=API_ENDPOINT, headers=headers, data=json_data)
            print("Response: " + r.text)
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
    creatmapp = []
    #global creatmapp
    input_fileName = 'CreateMapping_1.csv'
    lines = readFile(input_fileName)
    runDate = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')
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


def deleteMapping_curl(canonicalId):
    API_ENDPOINT = "http://10.254.3.10:49121/pmapper/v1/mapping/"
    CURL = API_ENDPOINT + canonicalId
    try:
        r = requests.delete(url=API_ENDPOINT, data=CURL)
        return r
    except:
        print("DELETE PRODUCT: Erro connecting to " + API_ENDPOINT)
        exit(-1)

def deleteMapping():
    input_fileName = 'DeleteMapping.csv'
    lines = readFile(input_fileName)
    runDate = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    operation = "deleteMapping"
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
            canonicalId = elem[0]
            res = deleteMapping_curl(canonicalId)
            generateLogFile(res, filename, operation, canonicalId)

def createProduct_curl(createprod):

    API_ENDPOINT = "http://10.254.3.10:49121/v1/product"

    headers = {
        "Content-Type": "application/json",
    }

    if len(createprod) == 1:
        if createprod[0].getName() == "" and createprod[0].getValue() == "":
            data = {
                'productId': createprod[0].getProductId(),
                'productName': createprod[0].getProductName(),
                'productType': createprod[0].getProductType(),
                'description': createprod[0].getDescription(),
                'enabled': True,
                'effectiveDate': createprod[0].getEffectiveDateprod(),
                "versionNumber": -1,
                'user': createprod[0].getUser(),
                'applicationName': createprod[0].getApplicationName(),
                'universeName': createprod[0].getUniverseName()
            }
        else:
            data = {
                'productId': createprod[0].getProductId(),
                'productName': createprod[0].getProductName(),
                'productType': createprod[0].getProductType(),
                'description': createprod[0].getDescription(),
                'enabled': True,
                'effectiveDate': createprod[0].getEffectiveDateprod(),
                "versionNumber": -1,
                'user': createprod[0].getUser(),
                'applicationName': createprod[0].getApplicationName(),
                'universeName': createprod[0].getUniverseName(),
                'attributes': [{
                    'name': createprod[0].getName(),
                    'value': createprod[0].getValue(),
                    'effectiveDate': createprod[0].getAttributeTypeDate().replace("\n",""),
                    'enabled': True
                }],
            }

        json_data = json.dumps(data)
        try:
            r = requests.post(url=API_ENDPOINT, headers=headers, data=json_data)
            print("Response: " + r.text)
        except:
            print("Error connecting to " + API_ENDPOINT)
            exit(-1)
    else:
        product = []
        map_aux = {}
        print("ENTREI")

        dict = {'productId': createprod[0].getProductId(),
                'productName': createprod[0].getProductName(),
                'productType': createprod[0].getProductType(),
                'description': createprod[0].getDescription(),
                'enabled': True,
                'effectiveDate': createprod[0].getEffectiveDateprod(),
                'versionNumber': -1,
                'user': createprod[0].getUser(),
                'applicationName': createprod[0].getApplicationName(),
                'universeName': createprod[0].getUniverseName()
                }

        for i in createprod:
            map_aux = {}
            map_aux.update({'name': i.getName()})
            map_aux.update({'value': i.getValue()})
            map_aux.update({'effectiveDate': i.getAttributeTypeDate().replace("\n","")})
            map_aux.update({'enabled': True})
            product.append(map_aux)



        dict.update({'attributes': product})


        json_data = json.dumps(dict)

        print(json_data)
        try:
            r = requests.post(url=API_ENDPOINT, headers=headers, data=json_data)
        except:
            print("Error connecting to " + API_ENDPOINT)
            exit(-1)

    return r


def createProduct():
    createprod= []
    input_fileName = 'Createproduct_1.csv'
    lines = readFile(input_fileName)
    runDate = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')
    operation = "CreateProduct"
    filename = "Output_createProduct_" + runDate + ".xml"
    print("File created: " + filename)
    productArr = []
    result = []

    j = 0
    for i in lines:
        # ignore the first row
        elem = i.split(";")
        if j == 0:
            j = j + 1
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
            mapObj = cProduct(productId, productName, productType, description, effectiveDateprod,user,applicationName,universeName,name,value,attributeTypeDate)
            productArr.append(mapObj)

    i = 0
    j = 1
    prev = 0
    mapp_i = productArr[i].getProductId()
    mapp_j = productArr[j].getProductId()

    if mapp_i == mapp_j:
        createprod.append(productArr[i])
    else:
        createprod.append(productArr[i])
    i = j
    j += 1
    while j <= len(productArr):
        if j == len(productArr):
            mapp_i = productArr[i].getProductId()
            mapp_prev = productArr[prev].getProductId()
            if mapp_prev == mapp_i:
                createprod.append(productArr[i])
                #print("J: " + str(j))
                #createprod.append(productArr[j])
                res = createProduct_curl(createprod)
                result.append(res)
            else:
                res = createProduct_curl(createprod)
                result.append(res)
                createprod = []
                createprod.append(productArr[i])
                res = createProduct_curl(createprod)
                result.append(res)
            j += 1
        else:
            mapp_i = productArr[i].getProductId()
            mapp_j = productArr[j].getProductId()
            mapp_prev = productArr[prev].getProductId()
            if mapp_i == mapp_j and mapp_prev == mapp_i:
                createprod.append(productArr[i])
                prev = i
                i = j
                j += 1
            else:
                if mapp_prev == mapp_i:
                    createprod.append(productArr[i])
                else:
                    res = createProduct_curl(createprod)
                    result.append(res)
                    createprod = []
                    createprod.append(productArr[i])

                prev = i
                i = j
                j += 1

    #generateLogFile(result, filename, create_prod, 1)
    generateLogFile(result, filename, operation, 1)



def deleteProduct_curl(productId, productName, productType, applicationName):

    API_ENDPOINT = "http://10.254.3.10:49121/v1/product"

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
    runDate = datetime.today().strftime('%Y-%m-%d_%Hh%Mm%Ss')
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
        f1.close()
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
