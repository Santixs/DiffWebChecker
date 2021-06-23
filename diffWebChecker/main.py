#!/usr/bin/env python
from diffWeb import diffWeb
from telegram_integration import telegramBot
from pdf_generator import generatePdf

import pdfkit
from pathlib import Path
import shutil
import os
import subprocess


#All the urls that we want to track
url_list = ['http://fi.upm.es/?id=gradoingenieriainformatica', 'http://fi.upm.es/?id=grupoliderazgointernacional']


for url in url_list:

    webName = url[url.find("//")+2:].replace("/","_") # Example: http://fi.upm.es/?id=gradoingenieriainformatica  ->   fi.upm.es_?id=gradoingenieriainformatica
    domainName =url[url.find("//")+2:url.find("/",8)] # Example: http://fi.upm.es/?id=gradoingenieriainformatica  ->   fi.upm.es


    #If the pdfFiles directory for that webpage does not exit, then it is created
    Path(f"files/pdfFiles/{webName}").mkdir(parents=True, exist_ok=True)  

    print("\n ------------------------------------------------- \n")
    #We download the web and its files
    subprocess.call(["wget", "--no-parent", "--page-requisites", "--html-extension","--convert-link","--quiet",f"-Pfiles/htmlFiles/{webName}/newestWeb(Aux)","-e robots=off", "--cut-dirs=2",url])
    print(url + " : Downloaded")

    
    if(os.path.isdir(f"files/htmlFiles/{webName}/newestWeb")): #If there is a previous version of the web, then we make the comparison with the previous version

        
        #We look for the html file in the folder that we have used to store all the data of the web
        path=str(Path(__file__).parent.parent.absolute())+f"/files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}"
        htmlFileName= [f for f in os.listdir(path) if f.endswith('.html')][0]
          
        #We load the 2 html files to make the comparison in the following line and if there is any changes we generate the pdfs
        diffWeb.load_files(f"files/htmlFiles/{webName}/newestWeb/{domainName}/{htmlFileName}",f"files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}/{htmlFileName}")
        if(diffWeb.generate_HTML(f"files/htmlFiles/{webName}/newestWeb/{domainName}/zzdiff.html",f"files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}/zzdiff.html")):#If there is changes 
                              
            shutil.rmtree(f"/files/htmlFiles/{webName}/oldestWeb/", ignore_errors=True) #Delete the oldest version of the web                  
            if(os.path.isdir(f"files/htmlFiles/{webName}/oldestWeb/newestweb")):shutil.rmtree(f"/files/htmlFiles/{webName}/oldestWeb/newestweb", ignore_errors=True) 
            

            generatePdf.generate_PDF_from_HTML(f"files/htmlFiles/{webName}/newestWeb(Aux)/{domainName}/zzdiff.html",f"files/pdfFiles/{webName}/newest_diff.pdf")#We generate the pdf from the html file

            shutil.move(f"files/htmlFiles/{webName}/newestWeb",f"files/htmlFiles/{webName}/oldestWeb") #Since we have downloaded a new version of the web, the name of the previous version, is now "oldestWeb"
            shutil.move(f"files/htmlFiles/{webName}/newestWeb(Aux)",f"files/htmlFiles/{webName}/newestWeb") #Since we have downloaded a new version of the web and there is some changes, the name of the aux version, is now "newestWeb"
                            
            
            generatePdf.generate_PDF_from_HTML(f"files/htmlFiles/{webName}/oldestWeb/{domainName}/zzdiff.html",f"files/pdfFiles/{webName}/oldest_diff.pdf")#We generate the pdf from the html file
            generatePdf.generate_pdf_from_two_pdf(f"files/pdfFiles/{webName}/oldest_diff.pdf",f"files/pdfFiles/{webName}/newest_diff.pdf",f"files/pdfFiles/{webName}/diff.pdf")
            #We generate one pdf from the 2 generated pdfs and with each page one next to the other
            
            shutil.rmtree(f"/files/htmlFiles/{webName}/oldestWeb/{domainName}/zzdiff.html", ignore_errors=True) #Delete the oldest htmlDiff
            shutil.rmtree(f"/files/htmlFiles/{webName}/newestWeb/{domainName}/zzdiff.html", ignore_errors=True) #Delete the newest htmlDiff

            #Telegram ------------------------------------------------------------------
            telegramBot.new_version(url,f"files/pdfFiles/{webName}/diff.pdf")
            #We send a message through the telegram api to a bot with the url and the pdf file generated previously


        else: #if the version of the web downloaded has no changes
            print("There is no changes")
            shutil.rmtree(f"files/htmlFiles/{webName}/newestWeb(Aux)", ignore_errors=True) #Delete that version



    else: #If there is no other version downloaded to compare with it
        os.rename(f"files/htmlFiles/{webName}/newestWeb(Aux)",f"files/htmlFiles/{webName}/newestWeb")#The newest is now the oldest

    print("\n ------------------------------------------------- \n")