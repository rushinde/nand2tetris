#! python3

import os, sys, re

class SymbolTable:
	def __init__(self):
		pass
	
	symbols = {	'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4, 
				'SCREEN':16384, 'KBD':24576, 'R0':0, 'R1':1, 'R2':2,
				'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9,
				'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15}
		
	def addEntry(self, symbol, address):
		self.symbols[symbol] = address
	
	def contains(self, symbol):
		return symbol in self.symbols
	
	def getAddress(self, symbol):
		return self.symbols[symbol]
	
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
	
	#atype = re.compile('[@]\w+$')
	def commandType(self):
		#if self.atype.match(self.current_command)[0]:
		if self.current_command[0] == "@":
			return 1
		else:
			return 2
	
	#def symbol(self):
	#	self.current_command.replace("(","")
	#	self.current_command.replace(")","")
	
	def dest(self):	
		if "=" not in self.current_command:
			return "null"
		else: return self.current_command.split("=")[0]
		
		
	def comp(self):
		if "=" not in self.current_command:
			return self.current_command.split(";")[0]
		else: return self.current_command.split("=")[1]
		
	
	def jump(self):
		if ";" not in self.current_command:
			return "null"
		return self.current_command.split(";")[1]	
	
class Code:
	def __init__(self):
		pass
	
	atypenum = re.compile('[@]\d+$')	
	def getA(self, a):
		st = SymbolTable()
		try:
			if self.atypenum.match(a)[0]:
				return '0' + bin(int(a.split("@")[1]))[2:].zfill(15)
		except:	
			return '0' + bin(int(st.symbols[a.split("@")[1]]))[2:].zfill(15)
		
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
		return self.jump_codes[jump]
		
	 
class Assembler:
	def __init__(self):
		pass
	
	atypenum = re.compile('[@]\d+$')	
	def pass1(self, infile):
		parser = Parser(infile)
		code = Code()
		st = SymbolTable()
		for keys in st.symbols:
			print(st.symbols[keys])
		while parser.hasMoreCommands():
			parser.advance()
			print(parser.current_command)
			if parser.current_command[0] == '(':
				if st.contains(parser.current_command[1:-1]):
					infile.remove(parser.current_command)
					continue
				else:
					parser.index -= 1
					st.addEntry(parser.current_command[1:-1], parser.index)
					infile.remove(parser.current_command)
		
	def pass2(self, infile, outfile):
		parser = Parser(infile)
		code = Code()
		st = SymbolTable()
		self.i = 16
		for keys in st.symbols:
			print(keys)
			print(st.symbols[keys])
		
		while parser.hasMoreCommands():
			parser.advance()
			if parser.commandType() == 1:
				try: 
					if self.atypenum.match(parser.current_command)[0]:
						outfile.write(code.getA(parser.current_command) + '\n')	
				except:
					if st.contains(parser.current_command.split("@")[1]):
						outfile.write(code.getA(parser.current_command) + '\n')
					else:
						st.addEntry(parser.current_command.split("@")[1], self.i)
						self.i += 1
						outfile.write(code.getA(parser.current_command) + '\n')
			elif parser.commandType() == 2:
				outfile.write(code.getC(parser.dest(), parser.comp(), parser.jump()) + '\n')
			#elif: parser.commandType() == 3:
				#outfile.write(code.getA(parser.symbol) + '\n')
		
	def assemble(self, infile, outfile):
		self.pass1(infile)
		#print(infile)
		self.pass2(infile, outfile)
			
			
def main():
	inname = sys.argv[1]
	outname = inname.replace('.asm', '.hack')
	
	infile = open(sys.argv[1],'r').read().split('\n')
	outfile = open(outname, 'w')
	
	#remove whitespaces and comments
	comment = re.compile('//.*$')
	while("" in infile): 
		infile.remove("")	
	infile = [comment.sub('', x) for x in infile if not comment.match(x)]
	infile = [x.strip() for x in infile]
	#for line in reversed(infile):
		#try:
			#comment.sub('', line)
			#print(line)
			
			#print(comment.search(line)[0])
			#infile.remove(comment.search(line)[0])
		#except:
			#continue
	
	print(infile)	
	assembler = Assembler()
	assembler.assemble(infile, outfile)
	
	outfile.close()
	
if __name__=="__main__":
	main()