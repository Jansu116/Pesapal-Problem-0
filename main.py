# Mnemonics/OpCodes
operationCodes = {
    'HALT': 0x00,
    'NOP': 0x01,
    'LI': 0x02,
    'LW': 0x03,
    'SW': 0x04,
    'ADD': 0x05,
    'SUB': 0x06,
    'MUL': 0x07,
    'DIV': 0x08,
    'MOD': 0x09,
    'INC': 0x0A,
    'DEC': 0x0B,
    'J': 0x0C, 
    'JR': 0x0D,
    'BEQ': 0x0E,
    'BNE': 0x0F,
    'LOG': 0x10,
    'SA': 0x11,  # Store Address - Used to assign a memory location to a register e.g. "SA R2 46" (46 being a memory location), enabling SW and LW to be able use/manipulate memory.
    'RET': 0x12,   # Return  -  Exits from function, returns to location immediately after the CALL.
    'CALL': 0x13   # Call  -  Executes function, jumps to label e.g. "CALL fact", works with RET (not J or JR).
}

# Registers
registers = {
    'R1': None,
    'R2': None,
    'R3': None,
    'R4': None,
    'R5': None,
    'R6': None,
    'RS': None, # Unique register, Stores Running & Final Result (Not neccessary)
    'RR': None, # Unique register, Stores Running Loop Value (Not neccessary)
}

# Store relationship between register and memory location. e.g. {'RR': 98, 'RS': 99} 
registerAddresses = {}

def writeToRegister(register, data):
    if register not in registers:
        print('Incorrect register')
        return None
    registers[register] = data

def readFromRegister(register):
    if register not in registers:
        print('Incorrect register')
        return None
    return registers[register]

# Array to simulate memory storage. 
memorySize = 100
memory = [0] * memorySize

def writeToMemory(address, data):
    try:
        address = int(address)
    except ValueError:
        print(f"Invalid address: {address}")
        return None
    
    if address >= memorySize or address < 0:
        print('Out of memory range')
        return None
    memory[address] = data

def readFromMemory(address):
    try:
        address = int(address)
    except ValueError:
        print(f"Invalid address: {address}")
        return None
    
    if address >= memorySize or address < 0:
        print('Out of memory range')
        return None
    return memory[address]


def getValueIfInMemory(register):
    if ',' in register:
        register = register.split(',')[0]

    if register in registerAddresses:
        registerValue = memory[registerAddresses[register]]
    else:
        registerValue = readFromRegister(register)

    # Try Except block created to convert memory value to integer (unless it's a label)
    try:
        return int(registerValue)
    except ValueError:
        return registerValue  

# Unused function - Initally meant to store labels to manage RET from J and JR. (Before finding out about call stacks)    
def getNextAvailableMemoryAddress():
    for i in range(memorySize):
        if memory[i] == 0:
            return i

# Checks if register has a memory location.
def checkIfInMemory(register):
    if ',' in register:
        register = register.split(',')[0]

    if register in registerAddresses:
        return True
    return False

# Read instructions file.
def readFileOfInstructions(file):
    fileLines = file.split('\n')
    labels = {}
    instructions = []
    instructionsLabel = None
    
    for line in fileLines:
        line = line.strip()
    
        if line.startswith(';') or line == "":
            continue # Skip comments and blank lines
      
        if line.endswith(':'): # Labels
            instructionsLabel = line[:-1]
            labels[instructionsLabel] = len(instructions)
        else: # Instructions
            instruction = line.split()
            mnemonic = instruction[0]
            opcode = operationCodes[mnemonic]
            operands = instruction[1:]
            instructions.append([opcode, mnemonic, operands, instructionsLabel])

    instructionsLabel = None

    return labels, instructions
    

# OpCode Handling   
def handleOpCode(opcode, operands, call_stack):
    try: # Handles in-line comments (Doesn't work on labels)
        comment_index = operands.index(';')
        operands = operands[:comment_index]
    except ValueError:
        pass

    if opcode == operationCodes['J']: # Move to label location.
        label = operands[0]
        return "JUMP", label
    if opcode == operationCodes['JR']: # Move to label stored in register or memory location pointed to by register.
        register = operands[0]
        if checkIfInMemory(register):
            registerVal = getValueIfInMemory(register)
        else:
            registerVal = readFromRegister(register)
        return "JUMP_REG", registerVal
    elif opcode == operationCodes['BEQ']: # Move to label location if register values (memory or not) are equal.
        registerA, registerB, memoryLocation = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        if registerAVal == registerBVal:
            return "BEQ_Branch", memoryLocation 
    elif opcode == operationCodes['BNE']: # Move to label location if register values (memory or not) are not equal.
        registerA, registerB, memoryLocation = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        if registerAVal != registerBVal:
            return "BNE_Branch", memoryLocation 
    elif opcode == operationCodes['LOG']: # Display value of register (memory or not). 
        print(f"LOG: {getValueIfInMemory(operands[0])}")
    elif opcode == operationCodes['NOP']: # Do nothing
        pass  
    elif opcode == operationCodes['LI']: # Add value to register
        register, value = operands
        writeToRegister(register, value)
        print(f"Added {value} to {register}")
    elif opcode == operationCodes['SA']: # Assign a memory location to a register
        register, address = operands
        registerAddresses[register] = int(address)  # Create a mapping between the register and the memory address
        print(f"Assigned memory location {address} to {register}")
    elif opcode == operationCodes['LW']: # Load a value from a memory location into a register
        registerTo, registerFrom = operands
        address = registerAddresses.get(registerFrom)  # Get the memory address from the register
        if address is not None:
            value = readFromMemory(address)
            writeToRegister(registerTo, value)
            print(f"Loaded value {value} from memory location {address} into {registerTo}")
        else:
            print(f"No memory location assigned to {registerFrom}")
    elif opcode == operationCodes['SW']: # Store a value from a register into a memory location
        address_reg, registerFrom = operands
        address = registerAddresses.get(address_reg) # Get the memory address from the register
        if address is not None:
            value = readFromRegister(registerFrom)
            writeToMemory(address, value)
            print(f"Stored value {value} from {registerFrom} into memory location {address}")
        else:
            print(f"No memory location assigned to {address_reg}")
    elif opcode == operationCodes['ADD']: # Add two registers
        registerResult, registerA, registerB = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        writeToRegister(registerResult, registerAVal + registerBVal)
        print(f"{registerResult} = {registerAVal} + {registerBVal}")
    elif opcode == operationCodes['SUB']: # Subtract two registers
        registerResult, registerA, registerB = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        writeToRegister(registerResult, registerAVal - registerBVal)
        print(f"{registerResult} = {registerAVal} - {registerBVal}")
    elif opcode == operationCodes['MUL']: # Multiply two registers    
        registerResult, registerA, registerB = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        writeToRegister(registerResult, registerAVal * registerBVal)
        print(f"{registerResult} = {registerAVal} * {registerBVal}")
    elif opcode == operationCodes['DIV']: # Divide two registers
        registerResult, registerA, registerB = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        writeToRegister(registerResult, registerAVal / registerBVal)
        print(f"{registerResult} = {registerAVal} / {registerBVal}")
    elif opcode == operationCodes['MOD']: # Modulous of two registers
        registerResult, registerA, registerB = operands
        registerAVal = getValueIfInMemory(registerA)
        registerBVal = getValueIfInMemory(registerB)
        writeToRegister(registerResult, registerAVal % registerBVal)
        print(f"{registerResult} = {registerAVal} % {registerBVal}")
    elif opcode == operationCodes['INC']: # Increment value in register (By +1)
        register = operands[0]
        registerVal = getValueIfInMemory(register)
        registerVal += 1
        writeToRegister(register, registerVal)
        print(f"{register} increased by 1 to {registerVal}")
    elif opcode == operationCodes['DEC']: # Decrement value in register (By -1)
        register = operands[0]
        registerVal = getValueIfInMemory(register)
        registerVal -= 1
        writeToRegister(register, registerVal)
    elif opcode == operationCodes['HALT']: # Stop execution
        return False
    elif opcode == operationCodes['CALL']: # Call a function (Functions like a jump but with a return address)
        return "CALL", operands[0]
    elif opcode == operationCodes['RET']: # Jump back to where the function was called
        if call_stack:
            return_address = call_stack.pop()  # Retrieve the last return address
            return "RETURN", return_address  
        else:
            return False
    return None 


def main(instructionFile):
    labels, instructions = readFileOfInstructions(instructionFile)
    if 'main' in labels: # Entry always at main:
        program_counter = labels['main']
        call_stack = [] # LIFO (Last In First Out) Function Call Stack - Keeps track of program_counter for RET (return)

        while program_counter < len(instructions):
            instruction = instructions[program_counter]
            print(f"\nExecuting: {instruction}")
            program_counter += 1
            result = handleOpCode(instruction[0], instruction[2], call_stack) # Didn't use opcodes and instead used mnemonics.
            if result is None:
                pass
            elif result is False:
                print("Stop Machine")
                break
            elif result[0] == "JUMP":
                print(f"Jump to '{result[1]}' section.")
                program_counter = labels.get(result[1], program_counter)
            elif result[0] == "JUMP_REG":
                print(f"Jump to register '{result[1]}'.")
                program_counter = labels.get(result[1], program_counter)
            elif result[0] == "BEQ_Branch":
                print(f"Branch to '{result[1]}' section, values ARE equal")
                program_counter = labels.get(result[1], program_counter)
            elif result[0] == "BNE_Branch":
                print(f"Branch to '{result[1]}' section, values NOT equal")
                program_counter = labels.get(result[1], program_counter)
            elif result[0] == "CALL":
                call_stack.append(program_counter) # Save return point before jumpings
                print(f"Run function '{result[1]}'.")
                program_counter = labels.get(result[1], program_counter)
            elif result[0] == "RETURN":
                print("Return from function")
                program_counter = result[1]
    else:
        print("No 'main' label found in the instructions.")


if __name__ == '__main__':
    instructionFile = """
    fact:
        ; if n == 0 return 1
        LI R1 0
        BNE R1, RR, ne
        RET

        ; recurse with n - 1
        ne:
        LW R1 RR
        LW R4 RS
        MUL R4 R4 R1
        LI R2 1
        SUB R1 R1 R2
        SW RR R1
        SW RS R4
        J fact ; Test2

    ; compute 5!
    main:
        LI R3 5
        SA RR 98 
        SW RR R3
        LI R4 1
        SA RS 99
        SW RS R4
        CALL fact
        LOG RS
    """
    main(instructionFile) # Factorial Instruction