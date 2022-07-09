import requests
import csv
from bs4 import BeautifulSoup
import wx 
List = []

def OnClicked(event):
	List.clear() 
	e=t_input.GetValue()
	print("sukebei_test_start")
	bool =True
	search(e,List,bool)
	print("sukebei_test_end")

def f_click(event): 
	List.clear()
	e=t_input.GetValue()
	print("nyaa_test_start")
	bool =False
	search(e,List,0)
	print("nyaa_test_end")
	
def get_magnet(url,List):
	response = requests.get(url)
	response.encoding = 'UTF-8' 
	soup = BeautifulSoup(response.text, 'lxml')
	articles = soup.find_all("tr",)
	articles = articles[1:]
	for i in articles:
		td = i.find_all("td")
		title = td[1].find("a").getText()
		x = i.find("td","text-center").find_all("a")
		magnet = x[0].get("href") if "magnet" in x[0].get("href") else x[1].get("href")
		List.append([title,magnet])
	
def search(keyword,List,bool):
	page = 1
	num = int(page_input.GetValue()) #修改終止頁數
	if bool == True:
		url = "https://sukebei.nyaa.si/?f=0&c=2_2&q="+ keyword + "&p=" + str(page)
	else:
		url = "https://nyaa.si/?f=0&c=2_2&q="+ keyword + "&p=" + str(page)	
	for i in range(num):
		buff=str(i+1)
		print("Page "+buff+" has been finished!")
		text2.SetLabel("正在搜尋中.... Page "+buff)
		page = i+1
		if bool ==True:
			url = "https://sukebei.nyaa.si/?f=0&c=2_2&q="+ keyword + "&p=" + str(page)
		else:
			url = "https://nyaa.si/?f=0&c=2_2&q="+ keyword + "&p=" + str(page)
		get_magnet(url,List)
	a=""
	for i in List:
		a +=i[0]
		a+="\n"
		a+=i[1]
		a+="\n"
		a+="-----------------------------------------------------------------------------"
		a+="\n"
	buf=str(len(List))
	t_text.SetValue(a)
	text2.SetLabel("總共搜尋到了"+buf+"筆資料")

def SaveClicked(event): 
	filename = "磁力連結_" + t_input.GetValue() + ".csv"
	with open(filename, "w", encoding = "utf-8-sig") as data1:
		for i in List:
			for j in i:
				data1.write("%s,"% (j))
			data1.write("\n")


app = wx.App() 
window = wx.Frame(None, title = "磁力搜索器", size = (500,580)) 
panel = wx.Panel(window) 

t_input =wx.TextCtrl(panel,pos=(20,50),size=(350,45))
font_in = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, 'Arial')
t_input.SetFont(font_in)

page_input =wx.TextCtrl(panel,pos=(420,50),size=(50,45))
font_in = wx.Font(20, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, 'Arial')
page_input.SetFont(font_in)

text1 = wx.StaticText(panel, label='請輸入搜尋名稱:',pos=(20,0))
font = wx.Font(28, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, 'Arial')
text1.SetFont(font)

text_p = wx.StaticText(panel, label='頁數',pos=(400,0))
font = wx.Font(28, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, 'Arial')
text_p.SetFont(font)

t_btn = wx.Button(panel, -1, "暗黑搜尋模式",pos=(170,100))
t_btn.SetSize((150, 50)) 
t_btn.Bind(wx.EVT_BUTTON,OnClicked)

f_btn = wx.Button(panel, -1, "普通搜尋模式",pos=(10,100))
f_btn.SetSize((150,50))
f_btn.Bind(wx.EVT_BUTTON,f_click)

s_btn = wx.Button(panel, -1, "儲存為CSV檔",pos=(330,100))
s_btn.SetSize((150,50))
s_btn.Bind(wx.EVT_BUTTON,SaveClicked)

text2 = wx.StaticText(panel, label='',pos=(0,150))
text2.SetFont(font)

t_text = wx.TextCtrl(panel,size = (480,300),pos=(0,210),style = wx.TE_MULTILINE)

window.Show(True) 
app.MainLoop() 
