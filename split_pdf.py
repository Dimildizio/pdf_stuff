from PyPDF2 import PdfFileWriter, PdfFileReader

def split_pdf(filename, pagelist):
    mypdf = PdfFileReader(open(filename, "rb"))

    try:
        assert max(pagelist) <= mypdf.numPages
        writers = []
        for pagenum in range(len(pagelist)):
            writers.append(PdfFileWriter())
        for n in range(len(writers)):
            start = 0 if n == 0 else pagelist[n-1]
            print(n, start, pagelist[n])
            for page in range(start, pagelist[n]):
                writers[n].addPage(mypdf.getPage(page))
            new_filename = filename[:-4] + '_part' + str(n+1) + '.pdf'
            with open(new_filename, 'wb') as f:
                writers[n].write(f)

    except AssertionError as e:
        print("Error: You want to cut more pages than your pdf has")

if __name__ == '__main__':
    fname = 'oxford.pdf'
    pages2cut = [75, 139, 161, 189, 193, 211]
    split_pdf(fname, pages2cut)