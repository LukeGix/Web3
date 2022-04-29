from qiling import *
from qiling.arch.evm.exceptions import Revert
from binascii import unhexlify as unhex

from eth_abi import decode_single

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

def memdump(src, length=16, start=0):
    mem_bytes = src.read(start, length)
    mem = ''.join(['%02X' % b for b in mem_bytes])
    return mem

def storagedump(src, address, index=0, slots=1):
    result = []
    for s in range(index, index+slots):
        val = src.get_storage(address=address, slot=s)
        result.append("{:>x}".format(val))
    return result

if __name__ == '__main__':
    contract = open('Vault.evm','r').read()
    contract += "0000000000000000000000"
    
    ql = Qiling(code=contract, archtype="evm")
    ql.debugger = True
    
    user1 = ql.arch.evm.create_account(balance=100*10**18)
    contract_addr = ql.arch.evm.create_account()

    def hook_sload(ql, argv):
        d = argv.disasm[argv.code.pc]
        index = int(stackdump(argv._stack.values)[-1])
        print(hex(d.pc), d.mnemonic, index, storagedump(argv.state, argv.msg.storage_address, index=index)[0])

    def hook_sstore(ql, argv):
        d = argv.disasm[argv.code.pc]
        index = int(stackdump(argv._stack.values)[-1])
        value = stackdump(argv._stack.values)[-2]
        print(hex(d.pc), d.mnemonic, index, value)

    def hook_eq(ql, argv):
        d = argv.disasm[argv.code.pc]
        print(hex(d.pc), d.mnemonic, ' == '.join(stackdump(argv._stack.values[-2:])))

    ql.hook_insn(hook_sload, 'SLOAD')
    ql.hook_insn(hook_sstore, 'SSTORE')
    ql.hook_insn(hook_eq, 'EQ')
    try:
        msg0 = ql.arch.evm.create_message(user1, b'', code=ql.code, contract_address=contract_addr)
        ql.run(code=msg0)

        call_data = '0xcf309012'
        msg1 = ql.arch.evm.create_message(user1, contract_addr, data=call_data)
        data = ql.run(code=msg1)
        print('\nLocked: {}\n'.format(decode_single('(bool)', data.output)[0]))

        call_data = '0xec9b5b3a' + ql.arch.evm.abi.convert(['bytes32'], [unhex('00')])
        msg1 = ql.arch.evm.create_message(user1, contract_addr, data=call_data)
        ql.run(code=msg1)

        call_data = '0xcf309012'
        msg1 = ql.arch.evm.create_message(user1, contract_addr, data=call_data)
        data = ql.run(code=msg1)
        print('\nLocked: {}\n'.format(decode_single('(bool)', data.output)[0]))

        call_data = '0xec9b5b3a' + ql.arch.evm.abi.convert(['bytes32'], [unhex('412076657279207374726f6e67207365637265742070617373776f7264203a29')])
        msg1 = ql.arch.evm.create_message(user1, contract_addr, data=call_data)
        ql.run(code=msg1)

        call_data = '0xcf309012'
        msg1 = ql.arch.evm.create_message(user1, contract_addr, data=call_data)
        data = ql.run(code=msg1)
        print('\nLocked: {}\n'.format(decode_single('(bool)', data.output)[0]))
    except Revert as e:
        print(f'Execution got reverted: {e}')
