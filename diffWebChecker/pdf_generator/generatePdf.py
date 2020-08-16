
from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter, pdf, PdfFileMerger
import pdfkit, difflib
import threading

def generate_PDF_from_HTML(HTMLfile,pdfFile):    
    #We create the pdfs of each web version
    pdfkit.from_file(HTMLfile,pdfFile) 
       

def generate_pdf_from_two_pdf(file1,file2,out):
        #we merge both pdfs and put the pages together to ease comparing them
    oldFile = PdfFileReader(open(file1,'rb'))
    newFile = PdfFileReader(open(file2,'rb'))


    writerOld = PdfFileWriter()
    writerNew = PdfFileWriter()

    writerOld.appendPagesFromReader(oldFile) 
    writerNew.appendPagesFromReader(newFile) 

    numberOld=writerOld.getNumPages()
    numberNew=writerNew.getNumPages()

    if numberNew>numberOld:
        while(writerNew.getNumPages()>writerOld.getNumPages()):
            writerOld.addBlankPage()
    elif(numberNew<numberOld):
        while(writerOld.getNumPages()>writerNew.getNumPages()):
            writerNew.addBlankPage()


    writer = PdfFileWriter()
    
    for i in range(writerOld.getNumPages()):        
        oldFilePage = writerOld.getPage(i)
        newFilePage = writerNew.getPage(i)
        translated_page = pdf.PageObject.createBlankPage(None, writerOld.getPage(0).mediaBox.getHeight(), writerNew.getPage(0).mediaBox.getWidth())   
        translated_page.mergeScaledTranslatedPage(oldFilePage, 0.7, 0, 0) 
        translated_page.mergeScaledTranslatedPage(newFilePage, 0.7, 420, 0)
        writer.addPage(translated_page)



    with open(out, 'wb') as f:
        writer.write(f)

