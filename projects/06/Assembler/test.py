class Assembler:
	def __init__(self):
		pass
		
	def assemble(self, infile, outfile):
		parser = Parser.Parser(infile)
		code = Code.Code()
		while parser.hasMoreCommands:
			parser.advance()
			if parser.commandType == 1:
				outfile.write(code.getA(parser.current_command) + '\n')
			else: outfile.write(code.getC(parser.dest, parser.comp, parser.jump) + '\n')
				