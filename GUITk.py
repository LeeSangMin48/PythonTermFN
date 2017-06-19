from tkinter import font
from internetMovie import *
from tkinter import*
from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk
#import mailcpy
import tkinter.messagebox

g_Tk = Tk()
g_Tk.geometry("855x700+750+200")
DataList = []
imgList = []
imgNumber = 0
mailList = []
def InitTopText():
    TempFont = font.Font(g_Tk, size=20, weight='bold', family = 'Consolas')
    MainText = Label(g_Tk, font = TempFont, text="[영화 정보 검색 앱 App]")
    MainText.pack()
    MainText.place(x=30)

def InitSearchListBox():

    global searchListbox
    ListBoxScrollbar = Scrollbar(g_Tk)
    ListBoxScrollbar.pack()
    ListBoxScrollbar.place(x=355, y=40)
    TempFont = font.Font(g_Tk, size=15, weight='bold', family='Consolas')
    searchListbox = Listbox(g_Tk, font=TempFont, activestyle='none',
                            width=30, height=1, borderwidth=5, relief='ridge')
    searchListbox.insert(1, "영화 제목으로 영화 검색")
    searchListbox.insert(2, "영화 제목으로 섬네일이미지 검색")
    searchListbox.insert(3, "메일 주소와 비밀번호 입력")
    searchListbox.insert(4, "나에게 메일보내기(gmail)")
    searchListbox.pack()
    searchListbox.place(x=10, y=50)
    ListBoxScrollbar.config(command=searchListbox.yview)

def InitInputLabel():
    global InputLabel
    TempFont = font.Font(g_Tk, size=15, weight='bold', family = 'Consolas')
    InputLabel = Entry(g_Tk, font = TempFont, width = 27, borderwidth = 5, relief = 'ridge')
    InputLabel.pack()
    InputLabel.place(x=10, y=90)

def InitSearchButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    SearchButton = Button(g_Tk, font = TempFont, text="실행",  command=SearchButtonAction)
    SearchButton.pack()
    SearchButton.place(x=330, y=90)

def SearchButtonAction():

    global searchListbox

    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)
    iSearchIndex = searchListbox.curselection()[0]
    if iSearchIndex == 0:
        searchMovie()
    elif iSearchIndex == 1:
        searchThumbnail()
    elif iSearchIndex == 2:
        sendMail()
    elif iSearchIndex == 3:
        sendMail()
    RenderText.configure(state='disabled')


def searchMovie():
    global DataList
    DataList.clear()
    if(getMovieDataFromTitle(InputLabel.get())==None):
        RenderText.insert(INSERT, "에러, 다시 검색해주세요")
    else:
        DataList = getMovieDataFromTitle(InputLabel.get())
        for i in range(len(DataList["title"])):
            RenderText.insert(INSERT, "[")
            RenderText.insert(INSERT, i + 1)
            RenderText.insert(INSERT, "] ")
            RenderText.insert(INSERT, "영화 제목: ")
            RenderText.insert(INSERT, DataList["title"][i])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "섬네일 주소: ")
            RenderText.insert(INSERT, DataList["thumbnail"][i])
            RenderText.insert(INSERT, "\n")
            RenderText.insert(INSERT, "트레일러 주소: ")
            RenderText.insert(INSERT, DataList["trailer"][i])
            RenderText.insert(INSERT, "\n\n")

def searchThumbnail():
    global DataList
    DataList.clear()
    global imgList
    imgList.clear()
    global imgNumber
    imgNumber = 0
    DataList = getMovieDataFromTitle(InputLabel.get())
    imgList = DataList["thumbnail"]
    url = imgList[imgNumber]
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    img = ImageTk.PhotoImage(im)
    RenderImg.configure(image = img)
    RenderImg.image = img

def InitRenderText():
    global RenderText

    RenderTextScrollbar = Scrollbar(g_Tk)
    RenderTextScrollbar.pack()
    RenderTextScrollbar.place(x=375, y=100)

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderText = Text(g_Tk, width=49, height=35, borderwidth=5, relief='ridge', yscrollcommand=RenderTextScrollbar.set)
    RenderText.pack()
    RenderText.place(x=10, y=135)
    RenderTextScrollbar.config(command=RenderText.yview)
    RenderTextScrollbar.pack(side=RIGHT, fill=BOTH)

    RenderText.configure(state='disabled')

def InitRenderImg():
    global RenderImg

    TempFont = font.Font(g_Tk, size=10, family='Consolas')
    RenderImg = Label(g_Tk)
    RenderImg.pack()
    RenderImg.place(x=385, y=40)

def InitNextButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    NextButton = Button(g_Tk, font = TempFont, text="다음",  command=NextButtonAction)
    NextButton.pack()
    NextButton.place(x=220, y=620)

def NextButtonAction():
    global DataList
    DataList.clear()
    global imgList
    imgList.clear()
    global imgNumber
    imgNumber +=1
    DataList = getMovieDataFromTitle(InputLabel.get())
    imgList = DataList["thumbnail"]
    url = imgList[imgNumber]
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    img = ImageTk.PhotoImage(im)
    RenderImg.configure(image=img)
    RenderImg.image = img

def InitBackButton():
    TempFont = font.Font(g_Tk, size=12, weight='bold', family = 'Consolas')
    BackButton = Button(g_Tk, font = TempFont, text="뒤로",  command=BackButtonAction)
    BackButton.pack()
    BackButton.place(x=80, y=620)

def BackButtonAction():
    global DataList
    DataList.clear()
    global imgList
    imgList.clear()
    global imgNumber
    imgNumber -=1
    DataList = getMovieDataFromTitle(InputLabel.get())
    imgList = DataList["thumbnail"]
    url = imgList[imgNumber]
    with urllib.request.urlopen(url) as u:
        raw_data = u.read()

    im = Image.open(BytesIO(raw_data))
    img = ImageTk.PhotoImage(im)
    RenderImg.configure(image=img)
    RenderImg.image = img

def sendMail():
    global host, port
    global DataList
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    global searchListbox
    iSearchIndex = searchListbox.curselection()[0]
    if iSearchIndex == 2:
        sendAD, passwd, recipAD = InputLabel.get().split(",")
    if iSearchIndex == 3:
        sendAD, passwd == InputLabel.get().split(",")
        #mailcpy.strcpy(recipAD, sendAD)
    Text = DataList
    msg = MIMEText(urllib.parse.quote(Text), "html", _charset="utf-8")
    msg['Subject'] = "result"
    msg['From'] = sendAD
    msg['To'] = recipAD
    s = smtplib.SMTP(host, port)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(sendAD, passwd)  # 로긴을 합니다.
    s.sendmail(sendAD, [recipAD], msg.as_string())
    s.close()

InitTopText()
InitSearchListBox()
InitInputLabel()
InitSearchButton()
InitRenderText()
InitRenderImg()
InitNextButton()
InitBackButton()
g_Tk.mainloop()