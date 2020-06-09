from PyPDF3 import PdfFileMerger

def mergepdf(files):
    merger = PdfFileMerger()
    for file in files:
        merger.append(open(file, "rb"))
	output = open("document-output.pdf", "wb")
	merger.write(output)
