import praw
import webbrowser
import time
from threading import Thread
# Import PySide classes
import sys
from PySide import QtCore, QtGui, QtWebKit

class RedditAPI:

    def __init__(self):
        self.reddit = praw.Reddit('personal login information')
        print(self.reddit.read_only)
        self.num = 10
        self.sub = "all"
        self.page = 0
        self.setTopPosts()

    def subExists(self,sub):
        exists = True
        try:
            self.reddit.subreddits.search_by_name(sub, exact=True)
        except:
            exists = False
        return exists

    def setSub(self,sub):
        self.sub = sub
        self.setTopPosts()

    def setNum(self,num):
        self.num = num
        self.setTopPosts()

    def setSubAndNum(self,sub,num):
        self.sub = sub
        self.num = num
        self.setTopPosts()

    def setTopPosts(self):
    	posts = []
        url = []
        submissions = self.reddit.subreddit(self.sub).hot(limit=self.num)
    	for submission in submissions:
            posts.append(submission.title)
            url.append(submission.url)
        self.posts = posts
        self.url = url

    def getSub(self):
        return self.sub

    def getNum(self):
        return self.num

    def getUrl(self,i):
        return self.url[i]

    def getPageUrl(self):
        pageURL = []
        if self.page == 0:
            pageURL = self.url
        else:
            i = 0
            while i < 10:
                pageURL.append(self.url[10*self.page+i]) 
                i = i + 1

        return pageURL

    def getPagePosts(self):
        pagePosts = []
        if self.page == 0:
            pagePosts = self.posts 
        else:
            i = 0
            while i < 10:
                pagePosts.append(self.posts[10*self.page+i]) 
                i = i + 1

        return pagePosts

    def incPage(self):
        if self.page == 0:
            self.setNum(100)
        self.page = self.page + 1

    def resetPage(self):
        self.page = 0


#User interface
class MainWindow(QtGui.QWidget):
    
    def __init__(self,API):
        super(MainWindow, self).__init__()
        self.API = API
        self.tempInput = "all"
        self.initUI()

    def initUI(self):
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    	sub = self.API.getSub()
    	num = self.API.getNum()
        titles = self.API.getPagePosts()
        
        self.grid = QtGui.QGridLayout()
        verticalLayout = QtGui.QVBoxLayout()
        horizontalLayout = QtGui.QHBoxLayout()

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.titleLabel = QtGui.QLabel("r/" + sub)
        self.titleLabel.setGeometry(QtCore.QRect(50, 20, 68, 17))
        self.titleLabel.setStyleSheet("QLabel { background-color : none; color : black; }")
        self.titleLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.titleLabel.setFont(font)

        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.lineEdit = QtGui.QLineEdit("Subreddit")
        self.lineEdit.setGeometry(QtCore.QRect(240, 20, 211, 16))
        self.lineEdit.setMaximumSize(QtCore.QSize(300, 50))
        self.lineEdit.textChanged.connect(self.lineEditTextChange)
        self.lineEdit.editingFinished.connect(self.returnPressed)
        self.lineEdit.selectAll()

        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        horizontalLayout.addItem(spacerItem1)
        horizontalLayout.addWidget(self.titleLabel)
        horizontalLayout.addItem(spacerItem2)
        horizontalLayout.addWidget(self.lineEdit)
        verticalLayout.addLayout(horizontalLayout)
        verticalLayout.addItem(spacerItem3)

        self.button = []
        for i in range(len(titles)):
            self.button.append(QtGui.QPushButton(titles[i]))
            verticalLayout.addWidget(self.button[i])
            self.button[i].setMaximumSize(QtCore.QSize(600, 50))
            self.button[i].setStyleSheet("QPushButton {text-align:left}")
            self.button[i].clicked.connect(self.indexer(i))

        scrollButton = QtGui.QPushButton("...")
        verticalLayout.addWidget(scrollButton)
        scrollButton.setMaximumSize(QtCore.QSize(600, 20))
        scrollButton.clicked.connect(self.scrollPosts)

        self.grid.addLayout(verticalLayout, 0, 0, 1, 1)

        topUrl = self.API.getPageUrl()
        self.webView = QtWebKit.QWebView()
        self.webView.load(topUrl[1])
        self.grid.addWidget(self.webView, 0, 1, 1, 1)


        self.setLayout(self.grid)   
        self.move(300, 150)
        self.setWindowTitle('Reddit')  

        self.show()

    def setUI(self):
        num = self.API.getNum()
        sub = self.API.getSub()

        titles = self.API.getPagePosts()

        self.titleLabel.setText("r/" + sub)

        self.lineEdit.setText("Subreddit")
        self.lineEdit.selectAll()

        for i in range(len(titles)):
            self.button[i].setText(titles[i])

        self.viewUrl(0)

    def lineEditTextChange(self,text):
        self.tempInput = text
        #print(self.tempInput)

    def returnPressed(self):
        self.newSub = self.tempInput
        if self.API.subExists(self.newSub) == True:
            self.API.resetPage()
            self.API.setSubAndNum(self.newSub,10)
            self.setUI()
        else:
            self.lineEdit.selectAll()

    def scrollPosts(self):
        self.API.incPage()
        self.setUI()


    #button wrapper
    def indexer(self,i):
        def subIndexer():
            self.viewUrl(i)
        return subIndexer

    #button linker to browser
    def viewUrl(self,i):
        url = self.API.getPageUrl()

        #open in local browser
        #print(webbrowser.open_new(url[i]))
        
        #open in UI browser
        self.webView.load(url[i])


#Chooses subreddit for the day
class Planner: 
							
    def __init__(self):
        pass

    def hourlySub(self,UI):
        i=0
        while True:
            time.sleep(3600)      #Change to 3600 for hourly
            sub = ['rickandmorty','all','EngineeringPorn']   
            UI.setUI(sub[i])
            i = i+1 
            if i == len(sub):
                i = 0


#class KeywordFilter:		#For research purposes
							#Filters for specific keywords (subreddits/all/keywords in subreddits)
#	def __init__(self):


def main():
    #Create API object and configure
    API = RedditAPI()

    #Create a Qt application
    app = QtGui.QApplication(sys.argv)
    UI = MainWindow(API)
	
    #Enter planner thread
    plan = Planner()
    thread = Thread(target = plan.hourlySub,args = [UI])
    thread.start()

	#Enter Qt application main loop
    sys.exit(app.exec_())
    print("done")

if __name__ == '__main__':
    main()
