def deFormatContact(contact):
    return ''.join(ele for ele in contact if ele.isdigit())


def deformatContactAndWriteToOutputFile(outputFile, line):
	deformattedContact = deFormatContact(line)
	if 9<= len(deformattedContact) <= 13:
		if deformattedContact.startswith('0'):
			outputFile.write('82'+deformattedContact[1:]+'\n') #use 82

def padContact(contact):
	padToAdd = ''
	for i in range(8-len(contact)):
		padToAdd += '0'
	return padToAdd + contact


def deformat8DigitContactAndWriteToOutputFile(outputFile, line):
	deformattedContact = deFormatContact(line)
	if 0 < len(deformattedContact) < 8:
		deformattedContact = padContact(deformattedContact)
	if len(deformattedContact) == 8:
		outputFile.write('8210'+deformattedContact+'\n') 


def writeOutliers(outputFile):
	for item in ['0119816934','0114339000','01194033173','011428371','0114283471','01198273837','01907822','0194071181','01194612730','0119406628','01199406628']:
		deformatContactAndWriteToOutputFile(outputFile, item)

def processRawdata(outfile, infilestart, infilelast):
	with open(outfile,'w') as outputFile:
		#writeOutliers(outputFile)
		for i in range(infilestart,infilelast):
			with open(str(i)+'.txt','r') as inputFile:
				for line in inputFile:
					deformat8DigitContactAndWriteToOutputFile(outputFile, line)
	
def removeDuplicates(originFile,destFile,outputFile)			
	originNumbers = set()
	destNumbers = set()
	with open(destFile,'r') as origin:
		for line in origin:
			originNumbers.add(line.strip())
	with open(originFile,'r') as dest:
		for line in dest:
			destNumbers.add(line.strip())

	rest = destNumbers - originNumbers

	with open(outputFile,'w') as output:
		for item in rest:
			output.write(item+'\n') 

if __name__ == '__main__':
	#processRawdata('3rd',21,24)
	#removeDuplicates('3rd.txt', 'alldata.txt', '3rd_newonly.txt')
	pass
