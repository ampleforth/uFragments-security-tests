import os
from manticore.ethereum import  ManticoreEVM

import helpers as h

NODE_MODULES_LIBS = ['openzeppelin-zos', 'zos-lib', 'openzeppelin-solidity']

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uFragments')
UFRAGMENTS_PATH = os.path.join(BASE_PATH, 'contracts')
MARKET_ORACLE_PATH = os.path.join(BASE_PATH, '..', 'market-oracle', 'contracts')

def init_workspace(test_name, cpus=1):
    workspace = test_name
    assert not os.path.isdir(workspace), "Workspace folder already exists"
    m = ManticoreEVM(procs=cpus, workspace_url=workspace)
    m.verbosity(3)
    return m

def _load_contract(m, path, contract, **kwargs):
    with open(os.path.join(path, f'{contract}.sol')) as f:
        return m.solidity_create_contract(
            f,
            contract_name=contract,
            solc_remaps=[f'{m}={os.path.join(BASE_PATH, "node_modules", m)}' for m in NODE_MODULES_LIBS],
            **kwargs,
        )

manticore = init_workspace('gons_invariant')

deployer = manticore.create_account(balance=int(1e25))
print('[*] Created deployer account')

market_oracle = _load_contract(manticore, MARKET_ORACLE_PATH, 'MarketOracle', owner=deployer)
print('[*] Created MarketOracle')

# Add a market source:
market_source_sol = '''
pragma solidity ^0.4.24;
contract MarketSource {
    uint256 _volume1;
    uint256 _volume2;
    uint256 _exchangeRate1;
    uint256 _exchangeRate2;
    bool _firstCall;

    constructor(uint256 v1, uint256 e1, uint256 v2, uint256 e2) public {
        _volume1 = v1;
        _volume2 = v2;
        _exchangeRate1 = e1;
        _exchangeRate2 = e2;
        _firstCall = true;
    }

    function getReport()
        public
        view
        returns (bool, uint256, uint256)
    {
        if (_firstCall) {
            _firstCall = false;
            return (true, _exchangeRate1, _volume1);
        } else {
            return (true, _exchangeRate2, _volume2);
        }
    }
}
'''
market_source_account = manticore.create_account(balance=10)
volume1 = manticore.make_symbolic_value(name='v1')
volume2 = manticore.make_symbolic_value(name='v2')
exchange_rate1 = manticore.make_symbolic_value(name='e1')
exchange_rate2 = manticore.make_symbolic_value(name='e2')
market_source = manticore.solidity_create_contract(market_source_sol, owner=market_source_account, args=[volume1, exchange_rate1, volume2, exchange_rate2])
print('[*] Created MarketSource')

market_oracle.addSource(market_source)
print('[*] Added MarketSource to the Oracle')

ufragments = _load_contract(manticore, UFRAGMENTS_PATH, 'UFragments', owner=deployer, gas=99999999)
#ufragments.initialize(deployer, signature='(address)', gas=99999999)
print('[*] Created and initialized UFragments')

#ufragments_policy = _load_contract(manticore, UFRAGMENTS_PATH, 'UFragmentsPolicy', owner=deployer, gas=999999999999)
#ufragments_policy.initialize(deployer, ufragments, signature='(address,address)', gas=99999999)
#print('[*] Created and initialized UFragmentsPolicy')

#ufragments.rebase()
#print('[*] Rebased')

# Now see if there is a transaction that can cause the invariant to be broken:
user_account = manticore.create_account(balance=1000)
symbolic_data1 = manticore.make_symbolic_buffer(64)
manticore.transaction(caller=user_account,
                      address=ufragments,
                      value=100,
                      data=symbolic_data1,
                      gas=9999999999
)
# symbolic_data2 = manticore.make_symbolic_buffer(64)
# manticore.transaction(caller=user_account,
#                       address=ufragments,
#                       value=100,
#                       data=symbolic_data2,
#                       gas=9999999999
# )
print('[*] Generated symbolic transaction')

DECIMALS = 9
MAX_UINT256 = 2**256-1
INITIAL_FRAGMENTS_SUPPLY = 50 * 10**6 * 10**DECIMALS
# TOTAL_GONS is a multiple of INITIAL_FRAGMENTS_SUPPLY so that _gonsPerFragment is an integer.
# Use the highest value that fits in a uint256 for max granularity.
TOTAL_GONS = MAX_UINT256 - (MAX_UINT256 % INITIAL_FRAGMENTS_SUPPLY)

for state in manticore.all_states:
    gons_per_fragment = state.platform.get_storage_data(ufragments.address, 2)
    total_supply = state.platform.get_storage_data(ufragments.address, 3)
    manticore.generate_testcase(
        state,
        '_gonsPerFragment != TOTAL_GONS.div(_totalSupply)',
        only_if=gons_per_fragment != TOTAL_GONS / total_supply
    )

h.finalize(m)
print(f"[+] Look for results in {manticore.workspace}")
