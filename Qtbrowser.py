from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

import sys

class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#标题
		self.setWindowTitle('My Browser')
		#图标
		self.setWindowIcon(QIcon('icons/sunny.png'))
		self.show()
		#地址栏
		self.urlbar = QLineEdit()
		#响应回车
		self.urlbar.returnPressed.connect(self.navigate_to_url)

		#标签栏
		self.tabs = QTabWidget()
		self.tabs.setDocumentMode(True)
		self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
		self.tabs.currentChanged.connect(self.current_tab_changed)
		self.tabs.setTabsClosable(True)
		self.tabs.tabCloseRequested.connect(self.close_current_tab)

		self.add_new_tab(QUrl('http://www.baidu.com'), 'Homepage')

		self.setCentralWidget(self.tabs)

		new_tab_action = QAction(QIcon('icons/sunny.png'), 'New Page', self)
		new_tab_action.triggered.connect(self.add_new_tab)

		#添加导航栏
		navigation_bar = QToolBar('Navigation')
		navigation_bar.setIconSize(QSize(16, 16))
		self.addToolBar(navigation_bar)

		#前进、后退、停止、刷新按钮
		back_button = QAction(QIcon('icons/back.png'), 'Back', self)
		next_button = QAction(QIcon('icons/next.png'), 'Forward', self)
		stop_button = QAction(QIcon('icons/stop.png'), 'stop', self)
		reload_button = QAction(QIcon('icons/reload.png'), 'reload', self)

		back_button.triggered.connect(self.tabs.currentWidget().back)
		next_button.triggered.connect(self.tabs.currentWidget().forward)
		stop_button.triggered.connect(self.tabs.currentWidget().stop)
		reload_button.triggered.connect(self.tabs.currentWidget().reload)

		#按钮添加到导航栏
		navigation_bar.addAction(back_button)
		navigation_bar.addAction(next_button)
		navigation_bar.addAction(stop_button)
		navigation_bar.addAction(reload_button)

		navigation_bar.addSeparator()
		navigation_bar.addWidget(self.urlbar)

	#响应回车
	def navigate_to_url(self):
		q = QUrl(self.urlbar.text())
		if q.scheme() == '':
			q.setScheme('http')
		self.tabs.currentWidget().setUrl(q)

	def renew_urlbar(self, q, browser=None):
		#如果不是当前窗口展示的网页则不刷新url
		if browser != self.tabs.currentWidget():
			return
		#当前链接更新到地址栏
		self.urlbar.setText(q.toString())
		self.urlbar.setCursorPosition(0)

	# 添加新标签页
	def add_new_tab(self, qurl=QUrl(''), label='Blank'):
		#
		browser = QWebEngineView()
		browser.setUrl(qurl)
		i = self.tabs.addTab(browser, label)

		self.tabs.setCurrentIndex(i)

		browser.urlChanged.connect(lambda qurl, browser=browser: self.renew_urlbar(qurl, browser))

		browser.loadFinished.connect(lambda _, i=i, browser=browser:
									self.tabs.setTabText(i, browser.page().title()))

	#双击打开新标签
	def tab_open_doubleclick(self, i):
		if i == -1:
			self.add_new_tab()
	#
	def current_tab_changed(self, i):
		qurl = self.tabs.currentWidget().url()
		self.renew_urlbar(qurl, self.tabs.currentWidget())

	def close_current_tab(self, i):
		#只剩一个则不关闭
		if self.tabs.count() < 2:
			return
		self.tabs.removeTab(i)


#创建应用
app = QApplication(sys.argv)
#创建主窗口
window = MainWindow()
#显示窗口
window.showMaximized()
#运行
app.exec_()
