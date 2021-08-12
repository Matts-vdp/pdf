# contains all data structures and code for working with the pdf's

import os
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger

# represents 1 pdf containing the pages between startPage and endPage 
# in the pdf located at path
class Pdf():
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.startPage = 0
        self.endPage = self.getNumPages()
    
    def getNumPages(self):
        pdf = PdfFileReader(self.path)
        i = pdf.getNumPages()
        return i
    
    def __str__(self):
        return self.name + " " + str(self.startPage+1) + "-" + str(self.endPage)
    
    # split the pdf in 2 parts a newly created pdf object and this object
    # this is done by changing the start and end pages
    def split(self, page):
        newpdf = Pdf(self.name, self.path)
        newpdf.startPage = self.startPage
        newpdf.endPage = page
        self.startPage = page
        return newpdf
    
# Used to hold all pdf's
class PdfList():
    def __init__(self):
        self.l = []   

    #searches for pdf files in a folder and add them to the list
    def findFiles(self, path):
        for folder, subfs, files in os.walk(path):
            for file in files:
                f = os.path.splitext(file)
                if f[1] == '.pdf':
                    self.l.append(Pdf(f[0], folder + '/' + file))
            break

    #adds a pdf file to the list
    def addFile(self, path):
        f = os.path.basename(path)
        f = os.path.splitext(f)
        if f[1] == '.pdf':
            self.l.append(Pdf(f[0], path))

    #merge all selected items to 1 pdf
    def merge(self, output):
        pdf_writer = PdfFileWriter()
        for pdf in self.l:
            pdfR = PdfFileReader(pdf.path)
            for i in range(pdf.startPage, pdf.endPage):
                page = pdfR.getPage(i)
                pdf_writer.addPage(page)
        with open(output, 'wb') as out:
            pdf_writer.write(out)

    #change the order of a item in the list
    def swap(self, i, up):
        if up:
            self.l[i], self.l[i-1] = self.l[i-1], self.l[i]
        else:
            self.l[i], self.l[i+1] = self.l[i+1], self.l[i]

    def remove(self, i):
        del self.l[i]

    def size(self):
        return len(self.l)
    
    # split the pdf at pdfid in to parts at page
    def split(self, pdfid, page):
        newpdf = self.l[pdfid].split(page)
        self.l.insert(pdfid, newpdf)


