import os
import sys
import shutil
import PyPDF2

# NOTICE: This program will check for all PDFS in specified root directory and sub-directories. Make sure there aren't any other PDFS in these directories.
# Also, PyPDF2 is not optimized for all PDFS. Some PDFS may not be read/fully read.

rootDir = sys.argv[1]
filterDirName = sys.argv[2]
keyWords = sys.argv[3:]
pdfDict = {}

try: 
    os.mkdir(filterDirName)
except OSError:
    print('ERROR: That sub-directory already exists in this directory')
    sys.exit()



def checkPDFKeyWords(title, pdfText, destPath):
    text = pdfText
    print(text)
    wordRep = 0
    for word in keyWords:
        wordRep += text.count(word)
    if wordRep == 0:
        return
    else:
        pdfDict[title] = wordRep


def extractPDF(title, pdfFile, destPath):
    pdfText = ''
    pdfFile = open(pdfFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    numOfPages = pdfReader.numPages
    if numOfPages > 2: # If The PDF is Long, Don't Extract It
        return
    for page in range(pdfReader.numPages):
        pdfPage = pdfReader.getPage(page)
        pdfText += pdfPage.extractText()
    checkPDFKeyWords(title, pdfText, destPath)
    
       
def findPDF():
    for dirs, subdirs, files in os.walk(rootDir):
        for file in files:
            if(file.endswith('.pdf')):
                base = os.path.basename(file)
                extractPDF(base, file, os.path.abspath(dirs))

findPDF()




