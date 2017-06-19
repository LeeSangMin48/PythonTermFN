from http.client import HTTPConnection

conn = None
regKey = 'daaae38eedaa6adf9766e73211c81cb1'
server = "apis.daum.net"
host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
port = "587"

def userURIBuilder(server, **user):
    str = "https://" + server + "/contents/movie" + "?"
    for key in user.keys():
        str += key + "=" + user[key] + "&"
    return str


def connectOpenAPIServer():
    global conn, server
    conn = HTTPConnection(server)

def getMovieDataFromTitle(title):
    import urllib
    global server, regKey, conn
    if conn == None:
        connectOpenAPIServer()
    uri = userURIBuilder(server, apikey=regKey, q=urllib.parse.quote(title), output="xml")  # 다음 검색 URL
    conn.request("GET", uri)

    req = conn.getresponse()
    print(req.status)
    if int(req.status) == 200:
        return extractMovieData(req.read())
    else:
        return None


def extractMovieData(strXml):
    thumbnailList = []
    titleList = []
    trailerList = []
    from xml.etree import ElementTree
    tree = ElementTree.fromstring(strXml)
    print(strXml)
    # Movie 엘리먼트를 가져옵니다.
    itemElements = tree.getiterator("item")  # return list type
    print(itemElements)
    for item in itemElements:
        thumbnailElements = item.getiterator("thumbnail")
        titleElements = item.getiterator("title")
        trailerElements = item.getiterator("trailer")
        for thumbnail in thumbnailElements:
            thumbnailContent = thumbnail.find("content")
            thumbnailList += [thumbnailContent.text]
        for title in titleElements:
            titleContent = title.find("content")
            titleList += [titleContent.text]
        for trailer in trailerElements:
            trailerContent = trailer.find("link")
            if (trailerContent.text != None):
                trailerList += [trailerContent.text]
            else:
                trailerList += ["None"]
    print(titleList, thumbnailList, trailerList)
    if len(titleList) > 0:
        return {"title": titleList, "thumbnail": thumbnailList, "trailer": trailerList}