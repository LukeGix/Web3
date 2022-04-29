from qiling import *
from qiling.arch.evm.vm.utils import *
from qiling.arch.evm.vm.instruction import *
from qiling.arch.evm.vm.disassembler import *
from binascii import unhexlify as unhex


def stackdump(src, length=16, start=0):
    result = []
    for i in range(start, len(src)):
        v_type = src[i][0]
        value = src[i][1]
        if v_type is bytes:
            val = int(value.hex() or '0', 16)
        elif v_type is int:
            val = value
        else:
            val = int(value[2:], 16)
        result.append("{:>x}".format(val))
    return result
#Leggo il contract

contract_target = open('Vault.evm', 'r').read()
contract_target += "0000000000000000000000"


ql = Qiling(code=contract_target, archtype="evm") #Emulating with qiling the ethereum virtual machine
#ql.debugger = True
user = ql.arch.evm.create_account(balance=100*10**18) #Creo un user con un balance di 100*10**18 wei
bt = bytecode_to_bytes(contract_target)

ret = EVMDisasm().disasm(bt,0)
print("\t--- CODE DUMP ---")
for j,i in ret.items():
	print("\t",i.pc,i.byte,i.mnemonic, i.imm_op)

print("\t--- END ---")

print("\n\n")
contract_addr = ql.arch.evm.create_account() #Così creo un'istanza del contratto --> SIMULA ANCHE IL COSTRUTTORE

print(f"DEBUG contract_address: {contract_addr.hex()}")

#Devo creare un hook all'opcode EQ; è come con LD_PRELOAD che sovrascrivo una strcmp per farmi stampare gli operandi che sta confrontando


def hook_eq(ql, argv):
	result = ""
	print("EQ hook executed!")
	val = (stackdump(argv._stack.values)[-2:])
	print(f"{hex(argv.code.pc)}: {' = '.join(val)} ")
	s = (stackdump(argv._stack.values)[-1:])[0]
	try:
		for i in range(0, len(s), 2):
			result += (bytes.fromhex(s[i:i+2]).decode("utf-8"))
		print(f"Password: {result}")
	except Exception:
		pass




function_signature = '0xec9b5b3a' #signature for unlock(bytes32)
calldata = function_signature + ql.arch.evm.abi.convert(['bytes32'], [unhex('41')])
#Set the hook
ql.hook_insn(hook_eq, 'EQ')

msg0 = ql.arch.evm.create_message(user, b'', code=ql.code, contract_address=contract_addr) #Transaction to deploy the contract
ql.run(code=msg0)

msg1 = ql.arch.evm.create_message(user, contract_addr, data=calldata)

ql.run(code=msg1)
