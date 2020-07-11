#! python3

#TO-DO
#Change filename to close items
#Fix the jump thing
#Symbol table

import os, sys, re

class Parser:
	def __init__(self, infile):
		self.infile = infile
		self.current_command = ''
		self.index = 0
		self.cmd_type = -1

	def hasMoreCommands(self):
		if self.index < len(self.infile):
			return True
		else: return False
		
	def advance(self):
		if self.hasMoreCommands() == True:
			self.current_command = self.infile[self.index]
		self.index += 1
	
	atype = re.compile('[@]\d+$')
	def commandType(self):
		try:
			if self.atype.match(self.current_command)[0]:
				return 1
		except:
			return 2
	
	def dest(self):	
		try:
			return self.current_command.split("=")[0]
		except:
			return "null"
		
	def comp(self):
		try:
			return self.current_command.split("=")[1]
		except:
			return self.current_command.split(";")[0]
	
	def jump(self):
		try:
			return self.dest.split(";")[1]
		except:
			return "null"
	
	
class Code:
	def __init__(self):
		pass
		
	def getA(self, a):
		return '0' + bin(int(a.split("@")[1]))[2:].zfill(15)
	
	def getC(self, dest, comp, jump):
		return '111' + self.getComp(comp) + self.getDest(dest) + self.getJump(jump)
	
	comp_codes = { 	'0':'0101010',  '1':'0111111',  '-1':'0111010', 'D':'0001100', 
                    'A':'0110000',  '!D':'0001101', '!A':'0110001', '-D':'0001111', 
                    '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110', 
                    'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111', 
                    'D&A':'0000000','D|A':'0010101', 'M':'1110000', '!M':'1110001', 
                    '-M':'1110011', 'M+1':'1110111', 'M-1':'1110010', 'D+M':'1000010',
					'D-M':'1010011','M-D':'1000111', 'D&M':'1000000', 'D|M':'1010101' }
	def getComp(self, comp):
		return self.comp_codes[comp]
	
	dest_codes = {	"null": "000", "M": "001", "D": "010", "A": "100", "MD": "011",
					"AM": "101", "AD": "110", "AMD": "111"}
	def getDest(self, dest):
		return self.dest_codes[dest]
	
	jump_codes = { 	"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100",
					"JNE": "101", "JLE": "110", "JMP": "111"}
	def getJump(self, jump):
		return self.dest_codes[jump]
		
	 
class Assembler:
	def __init__(self):
		pass
		
	def assemble(self, infile, outfile):
		parser = Parser(infile)
		code = Code()
		while parser.hasMoreCommands():
			parser.advance()
			if parser.commandType() == 1:
				outfile.write(code.getA(parser.current_command) + '\n')
			else: outfile.write(code.getC(parser.dest(), parser.comp(), parser.jump()) + '\n')
			
			
def main():
	inname = sys.argv[1]
	outname = inname.replace('.asm', '.hack')
	
	infile = open(sys.argv[1],'r').read().split('\n')
	outfile = open(outname, 'w')
	
	#remove whitespaces and comments
	comment = re.compile(r'//.*$')
	while("" in infile): 
		infile.remove("")
	for line in reversed(infile):
		try:
			infile.remove(comment.match(line)[0])
		except:
			continue
	
	print(infile)	
	assembler = Assembler()
	assembler.assemble(infile, outfile)
	
	outfile.close()
	
if __name__=="__main__":
	main()