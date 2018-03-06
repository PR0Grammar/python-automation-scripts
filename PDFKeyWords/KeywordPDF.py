import os
import sys
import PyPDF2

# NOTICE: This program will check for all PDFS in specified root directory and sub-directories. Make sure there aren't any other PDFS in these directories.
# Also, PyPDF2 is not optimized for all PDFS. Some PDFS may not be read/fully read.

filterDirName = sys.argv[1] #dir where to move pdfs
numOfPagesLimit = int(sys.argv[2]) #Max num of pages per PDF
keyWords = [word.lower() for word in sys.argv[3:]] #keywords to look for
filteredPdfList = [] #contains all pdfs titles, word count rep, and dir

try: 
    os.mkdir(filterDirName)
except OSError:
    print('ERROR: That sub-directory already exists in this directory')
    sys.exit()


def mvFileWithOrder(title, sourcePath, destPath, order):
    os.rename(sourcePath+'/'+title, destPath+'/'+order+title)


def checkKeyWords(text):
    lowercasedText = text.lower()
    wordRep = 0
    for word in keyWords:
        wordRep += text.count(word)
    return wordRep


def extractPDFText(pdfFile):
    pdfText = ''
    pdfFile = open(pdfFile, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFile)
    numOfPages = pdfReader.numPages
    if numOfPages > numOfPagesLimit: # Don't include PDFS that pass limit
        return
    for page in range(pdfReader.numPages):
        pdfPage = pdfReader.getPage(page)
        pdfText += pdfPage.extractText()
    return pdfText

    
def findAllPDF():
    pdfList = []
    for dirs, subdirs, files in os.walk('.'):
        for file in files:
            if(file.endswith('.pdf')):
                title = os.path.basename(file)
                dirOfPdf = os.path.abspath(dirs)
                pdfList.append([title, dirOfPdf])
    return pdfList


order = 0
pdfList = findAllPDF()

for pdf in pdfList:
    extractedText = extractPDFText(pdf[1]+'/'+pdf[0]) #extract text of (path/to/file/file.pdf)
    if extractedText is None:
        continue
    filteredPdfList.append([pdf[0], checkKeyWords(extractedText), pdf[1]])
    
filteredPdfList = sorted(filteredPdfList, key = lambda x: (x[1],x[1]), reverse=True) #Sort filtered pdf list by descending order of word rep. count
for pdf in filteredPdfList:
    order += 1
    mvFileWithOrder(pdf[0], pdf[2], os.path.abspath(filterDirName), str(order)) #Move and rename file to created dir ordered from highest word rep. count
