import os
import PyPDF2
import re
import sys

#NOTE: PyPDF2 is not optimized for all PDFs. Some pages or pdfs may go unread.

def mergePdf(pdfList, order):
    try:
        writer = PyPDF2.PdfFileWriter()
        combinedPdf = open('CombinedPdf.pdf','wb')
        for i in order:
            print(pdfList[i][1])
            pdfFile = open(pdfList[i][1],'rb')
            pdfFileReader = PyPDF2.PdfFileReader(pdfFile)
            for pageNum in range (pdfFileReader.numPages):
                page = pdfFileReader.getPage(pageNum)
                writer.addPage(page)
            writer.write(combinedPdf)
            pdfFile.close()
        combinedPdf.close()
        
    except IndexError:
        print('One or more of the indicies for the PDFs is not within the list. Incomplete PDF merge.')
        sys.exit()

def pdfList():
    listOfPdfs = []
    for file in os.listdir('.'):
        filename = os.fsdecode(file)
        if filename.endswith('.pdf'):
            listOfPdfs.append([filename, os.path.abspath(filename)])
    return listOfPdfs
            

def main(): 
    listOfPdfs = pdfList()
    if(len(listOfPdfs) == 0 or len(listOfPdfs) == 1):
        print('There are not enough PDFS to merge.')
        sys.exit()
    print('Here\'s a list of all the PDFs:')
    for i in range(len(listOfPdfs)):
        print(str(i+1) + '.' + listOfPdfs[i][0])
    print('\nEnter which PDFs you would like to merge in order separated by a comma(ie. 1,3,2,5): ')
    pdfSequence = input().split(',')
    sequenceInt = [int(i)-1 for i in pdfSequence] #Convert all elements to int, subtract by one to get indicies
    mergePdf(listOfPdfs, sequenceInt)
    
    

if __name__ == '__main__':
     main()
