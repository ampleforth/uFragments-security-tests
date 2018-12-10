from manticore.core.smtlib import Operators

import helpers as h

m = h.init_workspace('add_and_remove_source')

owner_account = m.create_account(balance=int(1e25))
print('[*] Created owner account')

market_oracle = h.create_market_oracle(m, owner_account)

tx_offset = len(m.human_transactions())
print("Beginning symbolic transactions at Tx No. ", tx_offset)

# Add a source and remove it
market_oracle.addSource(m.make_symbolic_value())
market_oracle.removeSource(m.make_symbolic_value())

# Get size
market_oracle.whitelistSize()

if m.count_running_states() == 0:
    print("[+] WARNING expected at least one running_state! see %s" % m.workspace)

for state in m.running_states:
    sym_tx = state.platform.human_transactions[tx_offset:]

    addSource_input = h.get_calldata_uint_arg(sym_tx[0].data, arg_ix=0, bits=160)
    removeSource_input = h.get_calldata_uint_arg(sym_tx[1].data, arg_ix=0, bits=160)

    whitelistSize = h.get_return_data(state.platform.human_transactions[-1])

    # if we added the same source as we removed, whitelist size shall be 0
    m.generate_testcase(
        state,
        'The addSource and removeSource made whitelistSize be in an unexpected state',
        only_if=Operators.ITE(
            addSource_input == removeSource_input,
            whitelistSize != 0,  # if sources addresses were same, the whitelist size shall not be 0
            whitelistSize != 1  # if the addresses differs, the whitelist size shall be 1
        )
    )

h.finalize(m)
