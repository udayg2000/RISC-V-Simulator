import ALU, IAG, memory, register
import sys

TERMINATION_CODE = 0xFFFFFFFF
iag = IAG.IAG(0)
alu = ALU.ALU()
pmi = memory.ProcessorMemoryInterface(4)
reg = register.register_module()

# global variables
IR = opcode = imm = funct3 = funct7 = 0
branch = 0
PC_Temp = 0

def fetch():
    global IR, PC_Temp
    pmi.mem_read = True
    pmi.dataType = 2
    pmi.update(alu.rz, iag.PC, alu.rm, 1) # set MAR to PC
    IR = pmi.getMDR() # get instruction corresponding to PC
    PC_Temp = iag.PC
    return

def decode():
    global opcode, funct3, funct7, imm, branch
    opcode = ((1<<7) - 1) & IR
    rd = (((1<<12) - (1<<7)) & IR)>>7
    funct3 = (((1<<15) - (1<<12)) & IR)>>12
    rs1 = (((1<<20) - (1<<15)) & IR)>>15
    rs2 = (((1<<25) - (1<<20)) & IR)>>20
    funct7 = (((1<<32) - (1<<25)) & IR)>>25

    if opcode == 0b0110011: # R format
        imm = 0
        alu.aluSrc = 0
        alu.aluOp = 2
        alu.muxY = 0
        branch = 0
    elif opcode == 0b0010011 or opcode == 0b0000011 or opcode == 0b1100111: # I format
        imm = (((1<<32) - (1<<20)) & IR) >> 20
        if (imm>>11)&1 == 1:            # check if sign bit is 1
            imm = -((imm ^ (1<<12-1)) + 1)
        alu.aluSrc = 1
        if opcode == 0b0010011:
            alu.aluOp = 2
            alu.muxY = 0
        else:
            alu.aluOp = 0
            if opcode == 0b0000011:
                alu.muxY = 1
                pmi.dataType = funct3
                pmi.mem_read = True
            else:
                branch = 1
                alu.muxY = -1
    elif opcode == 0b0100011: # S format
        imm = ((((1<<32) - (1<<25)) & IR) >> 20) + ((((1<<12)-(1<<7)) & IR)>>7)
        if (imm>>11)&1 == 1:            # check if sign bit is 1
            imm = -((imm^(1<<12-1)) + 1)
        alu.aluSrc = 1
        alu.aluOp = 0
        alu.muxY = -1
        pmi.mem_write = True
        pmi.dataType = funct3
        branch = 0
    elif opcode == 0b1100011: # SB format
        imm = (((1<<31) & IR) >> 19) + (((1<<7) & IR) << 4) + ((((1<<31) - (1<<25)) & IR)>>20) + ((((1<<12) - (1<<8))&IR)>>7)
        if (imm>>12)&1 == 1:            # check if sign bit is 1
            imm = -((imm^(1<<13-1)) + 1)
        alu.aluSrc = 0
        alu.aluOp = 1
        alu.muxY = -1
        branch = 1
    elif opcode == 0b0110111 or opcode == 0b0010111:    # U format
        imm = ((1<<32) - (1<<12)) & IR
        alu.aluSrc = 1         # to disable ALU
        alu.aluOp = 0
        alu.muxY = 0
        branch = 0
    elif opcode == 0b1101111:   # UJ format
        imm = (((1<<31) & IR)>>11) + (((1<<20) - (1<<12)) & IR) + (((1<<20) & IR)>>9) + ((((1<<31) - (1<<21)) & IR)>>20)
        if (imm>>20)&1 == 1:            # check if sign bit is 1
            imm = -((imm^(1<<21-1)) + 1)
        alu.aluSrc = -1
        alu.aluOp = 0
        alu.muxY = 2
        branch = 1
    reg.read_register_1 = "{0:b}".format(rs1)
    reg.read_register_2 = "{0:b}".format(rs2)
    reg.write_register = "{0:b}".format(rd)
    reg.read_register()
    return

def execute():
    global imm, funct3, funct7
    alu.execute(reg.read_data_1, reg.read_data_2, imm, funct3, funct7)
    return

def memory_access():
    global imm
    pmi.update(alu.rz, iag.PC, alu.rm, 0)
    iag.PCSrc = alu.zero & branch
    iag.update(imm)

    return

def register_update():
    alu.process_output(pmi.getMDR(), iag.PC)
    if alu.muxY in [0, 1, 2]: # if register is not be updated reg_write maybe set to some value like -1
        reg.reg_write = True
    reg.write_data = alu.ry
    reg.register_update()
    reg.reg_write = False
    return

def step():
    fetch()
    print(iag.PC, "{:b}".format(IR))
    decode()
    execute()
    memory_access()
    register_update()

def run(file):
    with open(file, 'r') as infile:
            text = True
            for line in infile:
                mloc, instr = [int(x, 16) for x in line.split()]
                if text:
                    pmi.memory.setWordAtAddress(mloc, instr)
                else:
                    pmi.memory.setByteAtAddress(mloc, instr)
                    
                if instr == TERMINATION_CODE:
                    text = False
        
    while (True):
        step()
        if IR == TERMINATION_CODE or IR == 0:
            break

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Need one argument for input file")
        exit()
    
    run(sys.argv[1])
