#PROGRAM READS A FILE WITH HACK_ASSEMBLY LANGUAGE AND WRITES HACK_MACHINE CODE IN ANOTHER FILE
#WORKS AS AN ASSEMBLER ESSENTIALLY FOR NAND2TETRIS COURSEWORK

#unpacks each instruction into underlying field
class Parser():
    def __init__(self, lines =None) -> None:
        if lines is None:
            lines = []  
        self.__file_contents = lines
    
    def get_contents(self):
        return self.__file_contents
    def set_contents(self, lines):
        self.__file_contents = lines
    #remove comments in the parser's list and the lines which are empty after comments are removed
    def remove_comments(self):
        separator = "//"
        temp_list = []
        for line in self.__file_contents:
            line = line.split(separator,1)[0]
            if line == "":
                continue
            temp_list.append(line.replace(' ', '')) #remove all whitespace in string
        self.__file_contents = temp_list
    def delete_line(self, line):
        self.__file_contents.remove(line)

#stores and tracks default symbol variables and user-defined symbols
class SymbolTable():
     def __init__(self) -> None:
        self.symbol_table = {
                'SP'    :     '0',
                'LCL'   :     '1',
                'ARG'   :     '2',
                'THIS'  :     '3',
                'THAT'  :     '4',
                'R0'    :     '0',
                'R1'    :     '1',
                'R2'    :     '2',
                'R3'    :     '3',
                'R4'    :     '4',
                'R5'    :     '5',
                'R6'    :     '6',
                'R7'    :     '7',
                'R8'    :     '8',
                'R9'    :     '9',
                'R10'   :    '10',
                'R11'   :    '11',
                'R12'   :    '12',
                'R13'   :    '13',
                'R14'   :    '14',
                'R15'   :    '15',
                'SCREEN': '16384',
                'KBD'   : '24576',
        }
     def add_symbol(self, key, value):
        self.symbol_table[key] = value
     def is_in_table(self, key):
        for table_key in self.symbol_table.keys():
            if table_key == key:
                return True
        return False

#translates each field into corresponding binary field
class CodeTranslator():
     def __init__(self) -> None:
        self.comp_dict = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "D+1": "0011111",
            "1+D": "0011111",
            "A+1": "0110111",
            "1+A": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "A+D": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "A&D": "0000000",
            "D|A": "0010101",
            "A|D": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "1+M": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "M+D": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "M&D": "1000000",
            "D|M": "1010101",
            "M|D": "1010101",
        }
        self.dest_dict = {
            "": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }
        self.jmp_dict = {
            "": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }
     def is_A_instruction(self, line):
        if line[0] == "@":
           return True
        else:
            return False

     def convert_A_instruction(self, line:str):
        numerical_int = int(line[1:])
        binary = format(numerical_int, 'b')
        bits_16_binary ='0'+binary.zfill(15)
        return bits_16_binary

     def C_instruction_cases(self, line:str):
        if ( (line.find('=') != -1) and (line.find(';') != -1) ):  #if '=' and ';' exist
            return "EQUAL_AND_SEMICOLON"
        elif ( (line.find('=') != -1) ): #if '=' exist
            return "EQUAL"
        elif ( (line.find(';') != -1) ): #if ';' exist
            return "SEMICOLON"
        else:
            print("ERROR!!! Exiting now")
            print("Line with error is: ", line)
            exit(1)

     def convert_C_instruction(self, line:str):
        cases = self.C_instruction_cases(line)
        match cases:
            case "EQUAL_AND_SEMICOLON":
               line.replace(';', '=')
               components = line.split('=')
               assert(len(components) == 3)
               bits_16_binary = '111' + self.comp_dict[components[1]] + self.dest_dict[components[0]] + self.jmp_dict[components[2]]
            case "EQUAL":
                components = line.split('=')
                assert(len(components) == 2)
                bits_16_binary = '111' + self.comp_dict[components[1]] + self.dest_dict[components[0]] + '000'
            case "SEMICOLON":
                components = line.split(';')
                assert(len(components) == 2)
                bits_16_binary = '111' + self.comp_dict[components[0]] + '000' + self.jmp_dict[components[1]]
        return bits_16_binary

#initialises I/O file handling and drives process
def main():
    read_file = open('/home/shane/nand2tetris/projects/06/pong/Pong.asm', 'r')
    write_file = open('/home/shane/nand2tetris/projects/06/Pong.hack', 'w')
    asm_lines = read_file.read().split('\n') #split string into a a list of strings based on new line character 
    Parse = Parser(asm_lines)
    Code_Translator = CodeTranslator()
    Symbol_Table = SymbolTable()
    count = 0
    Parse.remove_comments()
    #FIRST PASS
    for index, line in enumerate(Parse.get_contents()): #to add custom symbols into table 
        if line[0] == '(':
            temp_symbol = line[1:-1]
            Symbol_Table.add_symbol(temp_symbol, str(index-count))
            count+=1 #count var to ensure the address is correct after removing the 

    temp_list = Parse.get_contents()
    avail_symbol_address = 16
    #SECONDPASS
    #To remove (customsymbols) with brackets
    #temp_list[:] to create a copy of temp_list to prevent modifying the list being iterated through 
    #remove() may skip some elements if i remove the list that is being iterated through
    for line in temp_list[:]:  
        if line[0] == '(':
            temp_list.remove(line)

    #THIRDPASS
    #Replace @customsymbols with @numbers
    #if new @variablename, replace with number starting from address no.16 and store this symbol in the symbol_table
    for index, line in enumerate(temp_list):       
        if Code_Translator.is_A_instruction(line):
            if not (line[1:].isnumeric()):
                if Symbol_Table.is_in_table(line[1:]):
                    temp_string = Symbol_Table.symbol_table[line[1:]]
                    temp_list[index] = '@' + temp_string
                else:
                    temp_list[index] = '@' + str(avail_symbol_address)
                    Symbol_Table.add_symbol(line[1:], str(avail_symbol_address))
                    avail_symbol_address+=1
    #store the new modified program code in Parser class member 'file_contents'
    Parse.set_contents(temp_list)

    #translate all the A or C instructions into machine code and write to file
    test_count =0
    for line in Parse.get_contents():
        if Code_Translator.is_A_instruction(line):
            machine_code = Code_Translator.convert_A_instruction(line)
            write_file.write(machine_code+'\n')
            test_count+=1
        else:
            machine_code = Code_Translator.convert_C_instruction(line)
            write_file.write(machine_code+'\n')
            test_count+=1
    read_file.close()
    write_file.close()
    
if __name__ == '__main__':
    main()
