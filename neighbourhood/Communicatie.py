import httplib

def SendInformation(URL,Message):
    connectie = httplib.HTTPConnection(URL)
    UniqueURL = '/IncomingInformation/' + Message
    connectie.request('POST',UniqueURL)
    response = connectie.getresponse().status
    return str(response)


def GetInformation(URL,Message):
    connectie = httplib.HTTPConnection(URL)
    UniqueURL = '/OutgoingInformation/'+ Message
    connectie.request('GET',UniqueURL)
    response = connectie.getresponse()
    return response.read()

