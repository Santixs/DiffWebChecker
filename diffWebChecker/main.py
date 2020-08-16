from diffWeb import diffWeb
from telegram_integration import telegramBot
from pdf_generator import generatePdf

import time
from pywebcopy import save_webpage
import pdfkit
from pathlib import Path
import shutil
import os
import subprocess
import threading


url_list = ['http://fi.upm.es/?id=gradoingenieriainformatica', 'http://fi.upm.es/?id=grupoliderazgointernacional']

event = threading.Event()

for url in url_list:

    webName = url[url.find("//")+2:].replace("/","|")
    domainName =url[url.find("//")+2:url.find("/",8)]



    #Path(f"files/htmlFiles/{webName}/newestWeb").mkdir(parents=True, exist_ok=True)
    Path(f"files/pdfFiles/{webName}").mkdir(parents=True, exist_ok=True)  

    print("\n ------------------------------------------------- \n")
    #We download the web and its files
    subprocess.call(["wget", "--no-parent", "--page-requisites", "--html-extension","--convert-link","--quiet",f"-Pfiles/htmlFiles/{webName}/newestWeb(Aux)","-e robots=off", "--cut-dirs=2",url])
    print(url + " : Downloaded")

    
    if(os.path.isdir(f"files/htmlFiles/{webName}/newestWeb")): #If there is a previous version of the web   

        #We find the html file

        path=str(Path(__file__).parent.parent.absolute())+f"/files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}"
        htmlFileName= [f for f in os.listdir(path) if f.endswith('.html')][0]
          
        diffWeb.load_files(f"files/htmlFiles/{webName}/newestWeb/{domainName}/{htmlFileName}",f"files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}/{htmlFileName}")
        if(diffWeb.generate_HTML(f"files/htmlFiles/{webName}/newestWeb/{domainName}/zzdiff.html",f"files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}/zzdiff.html")):

            #If there is changes 
            event.wait(2)        
            shutil.rmtree(f"/files/htmlFiles/{webName}/oldestWeb/", ignore_errors=True) #Delete the oldest
            event.wait(1)       
            if(os.path.isdir(f"files/htmlFiles/{webName}/oldestWeb/newestweb")):shutil.rmtree(f"/files/htmlFiles/{webName}/oldestWeb/newestweb", ignore_errors=True)

            generatePdf.generate_PDF_from_HTML(f"files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}/zzdiff.html",f"files/pdfFiles/{webName}/newest_diff.pdf")
            shutil.move(f"files/htmlFiles/{webName}/newestWeb",f"files/htmlFiles/{webName}/oldestWeb")
            shutil.move(f"files/htmlFiles/{webName}/newestWeb(Aux)",f"files/htmlFiles/{webName}/newestWeb")
            
            event.wait(1)      
            
            generatePdf.generate_PDF_from_HTML(f"files/htmlFiles/{webName}/oldestWeb/{domainName}/zzdiff.html",f"files/pdfFiles/{webName}/oldest_diff.pdf")
            event.wait(1)
            generatePdf.generate_pdf_from_two_pdf(f"files/pdfFiles/{webName}/oldest_diff.pdf",f"files/pdfFiles/{webName}/newest_diff.pdf",f"files/pdfFiles/{webName}/diff.pdf")
            event.wait(1)
            shutil.rmtree(f"/files/htmlFiles/{webName}/oldestWeb/{domainName}/zzdiff.html", ignore_errors=True) #Delete the oldest htmlDiff
            shutil.rmtree(f"/files/htmlFiles/{webName}/newestWeb/{domainName}/zzdiff.html", ignore_errors=True) #Delete the newest htmlDiff

            #Telegram
            telegramBot.new_version(url,f"files/pdfFiles/{webName}/diff.pdf")

        else:
            print("There is no changes")
            shutil.rmtree(f"files/htmlFiles/{webName}/newestWeb(Aux)", ignore_errors=True) #Delete the oldest



    else:
        os.rename(f"files/htmlFiles/{webName}/newestWeb(Aux)",f"files/htmlFiles/{webName}/newestWeb")#The newest is now the oldest

    print("\n ------------------------------------------------- \n")