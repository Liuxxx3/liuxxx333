from bs4 import BeautifulSoup
from urllib import request
import re
import time
import xlsxwriter

def getHTMLText(download_url):
    i=0
    row=1
    col=0
    try:
        while i<1000:
            head = {}
            shi=[0 for x in range(0, 10000)]
            daiyun=[0 for x in range(0, 10000)]
            qian=[0 for x in range(0, 10000)]
            hou=[0 for x in range(0, 10000)]

            head[
                'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
            download_req = request.Request(url=download_url, headers=head)
            download_response = request.urlopen(download_req)
            download_html = download_response.read().decode('utf-8', 'ignore')
            soup_texts = BeautifulSoup(download_html, 'lxml')
            texts = soup_texts.find(id='Label_Msg', class_='content_Case')
            soup_text = BeautifulSoup(str(texts), 'lxml')
            txt=str(soup_text)
            shi[i]=txt[84:103]
            daiyun[i]=re.findall(r"\d+",txt)[6]
            qian[i]=re.findall(r"\d+",txt)[7]
            hou[i]=re.findall(r"\d+",txt)[8]
            worksheet.write(row, col,shi[i])    #写入数据
            worksheet.write(row, col+1, daiyun[i])
            worksheet.write(row, col+2,qian[i])
            worksheet.write(row, col+3,hou[i])
            time.sleep(60)
            i=i+1
            row+=1
    except:
        return ""

if __name__ == "__main__":
    workbook = xlsxwriter.Workbook('biaoge' + '.xlsx') #创建新表
    worksheet = workbook.add_worksheet()
    
    bold = workbook.add_format({'bold': True})  #建立粗体格式
    
    worksheet.write('A1', '时间', bold)        #写入标题，粗体
    worksheet.write('B1', '代运车辆数', bold)
    worksheet.write('C1', '前半小时进场车辆数', bold)
    worksheet.write('D1', '前半小时离场车辆数', bold)
    worksheet.set_column('A:A', 40)            #改变列宽度
    worksheet.set_column('B:B',40)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D',40)
    getHTMLText('http://www.whalebj.com/xzjc/default.aspx')
    workbook.close()






