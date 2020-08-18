from pathlib import Path
import difflib
import os



def load_files(file1, file2):
    global text, text2, lines, f, f2

    #Web1
    f = open(file1, encoding = "ISO-8859-1")
    text = f.readlines()

    #Web2
    f2 = open(file2, encoding = "ISO-8859-1")    
    text2 = f2.readlines()

    diff = difflib.unified_diff(text, text2, fromfile='file1', tofile='file2', lineterm='', n=0)
    lines = list(diff)[1:]    
    f.close()
    f2.close()

    #to see manually the changes
    '''for i in difflib.unified_diff(text, text2, fromfile='file1', tofile='file2', lineterm='', n=0):
        print(i)'''

           

#To obtain the indexes of the lines where the changes have been done we split the corresponding line (for example @@ -105 +105 @@)
def getIndex(i):    
    global firstI,secondI,firstL,secondL

    first=(i[i.index("-")+1:i.index("+")])
    second=(i[i.index("+")+1:-2])

    (firstI,firstL) = {True: first.split(",", 1), False: (first,0)}[first.find(",")!=-1]
    (secondI,secondL) = {True: second.split(",", 1), False: (second,0)}[second.find(",")!=-1]
    (firstI, firstL, secondI, secondL) = (int(firstI), int(firstL), int(secondI), int(secondL))
    

def whatIs(line,start):    
    i=1
    minus=0
    plus=0
    while(start+i<len(line) and line[start+i][0] !="@" ):  #We count all the minuses and pluses (separately)   
        if line[start+i][0] =='-':minus+=1; 
        elif line[start+i][0] =='+': plus+=1; 
        i+=1

    if plus==0: return "deleted"    
    elif minus==0: return "added"
    elif plus==minus:return "changes"
    else: return "both"

def modHtml(numText,color):
    global text, text2
    if numText==1:
        text[firstI-1] = f'<fieldset style="background-color:{color}";>{text[firstI-1]}'  
        text[firstI+firstL-1] = f'{text[firstI+firstL-1]}</fieldset>'        
    else:
        text2[secondI-1] = f'<fieldset style="background-color:{color}";>{text2[secondI-1]}'  
        text2[secondI+secondL-1] = f'{text2[secondI+secondL-1]}</fieldset>'
        

def generate_HTML(file1,file2):        
    if(len(lines)==0):return False #There is no changes  
    else:   
        for i in lines:        
            if i[0] == '@':        
                getIndex(i)
                
                what= whatIs(lines,lines.index(i))    
                if(what=="deleted"):                     
                    modHtml(1,"#f3a7a7")
                    
                elif(what=="added"):                    
                    modHtml(2,"#bff3a7")
                    
                elif(what=="changes"):                     
                    modHtml(2,"#f3e9a7")
                    
                    
                else: #Deleted and changes, both                
                    modHtml(2,"#bff3a7")
                    modHtml(1,"#f3a7a7")         
                    
                    

        f = open(file1, "a")
        f.writelines(text)
        f2 = open(file2, "a")
        f2.writelines(text2)        
        f.close()
        f2.close()
        return True





