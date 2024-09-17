from main import main

instructionFile = """
    fact:
        JR R3
        HALT

    test:
        LI R4 123
        LOG R4
        HALT

    ; test out jump register.
    main:
        SA R3 0
        LI R1 test
        SW R3 R1
        J fact
"""
print("Jump Register Test")
print("------------------------------------------------------------")
main(instructionFile)
print("\n\n\n\n")

    
instructionFile = """
main:
    LI R1 1
    CALL func1
    LOG R1
    HALT

func1:
    INC R1
    CALL func2
    INC R1
    RET

func2:
    INC R1
    CALL func3
    INC R1
    RET

func3:
    INC R1
    RET
"""
print("Nested Function Calls Test")
print("------------------------------------------------------------")
main(instructionFile)
print("\n\n\n\n")

# instructionFile = """
# main:
#     LI R1 10
#     LI R2 0
#     DIV R3 R1 R2
#     LOG R3
#     LOG R4
#     LI R5 5
#     ADD R6 R5 R4
#     LOG R6
#     HALT
# """
# print("Edge Cases Test")
# print("------------------------------------------------------------")
# main(instructionFile)
# print("------------------------------------------------------------")