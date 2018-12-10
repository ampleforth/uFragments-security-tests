import os

from functools import partial
from manticore.core.smtlib import Operators
from manticore.ethereum import ABI, ManticoreEVM
from manticore.platforms.evm import Transaction
from os.path import isdir

# Configure paths here!
NODE_MODULES_LIBS = ['openzeppelin-zos', 'zos-lib', 'openzeppelin-solidity']

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uFragments')
UFRAGMENTS_PATH = os.path.join(BASE_PATH, 'contracts')
MARKET_ORACLE_PATH = os.path.join(BASE_PATH, '..', 'market-oracle', 'contracts')

def init_workspace(test_name, cpus=1):
    workspace = test_name
    assert not isdir(workspace), "Workspace folder already exists"
    m = ManticoreEVM(procs=cpus, workspace_url=workspace)
    m.verbosity(3)
    return m


def finalize(m):
    m.finalize()
    print("[+] Look for results in %s" % m.workspace)


def create_all_contracts(m):
    owner_account = m.create_account(balance=int(1e25))
    print('[*] Created owner account')

    market_source = create_market_source(m, owner_account, symbol='GDAX', value=600)
    market_oracle = create_market_oracle(m, owner_account)

    ufragments = create_ufragments(m, owner_account)
    ufragments_policy = create_ufragments_policy(m, owner_account, ufragments)

    return owner_account, market_source, market_oracle, ufragments, ufragments_policy


def create_market_source(m, owner_account, symbol: str, value: int):
    """
    Example args: symbol='GDAX', value=600
    """
    ms = _load_contract(m, MARKET_ORACLE_PATH, 'MarketSource', owner=owner_account, args=[symbol, value])
    print('[*] Created MarketSource')
    return ms


def create_market_oracle(m, owner_account):
    mo = _load_contract(m, MARKET_ORACLE_PATH, 'MarketOracle', owner=owner_account)
    print('[*] Created MarketOracle')
    return mo


def create_ufragments(m, owner_account):
    ufragments = _load_contract(m, UFRAGMENTS_PATH, 'UFragments', owner=owner_account)
    ufragments.initialize(owner_account, signature='(address)')
    print('[*] Created and initialized UFragments')
    return ufragments


def create_ufragments_policy(m, owner_account, ufragments_account):
    ufragments_policy = _load_contract(m, UFRAGMENTS_PATH, 'UFragmentsPolicy', owner=owner_account)
    ufragments_policy.initialize(owner_account, ufragments_account, signature='(address,address)')
    print('[*] Created and initialized UFragmentsPolicy')
    return ufragments_policy


def _load_contract(m, path, contract, **kwargs):
    with open(os.path.join(path, f'{contract}.sol')) as f:
        return m.solidity_create_contract(
            f,
            contract_name=contract,
            solc_remaps=[f'{m}={os.path.join(BASE_PATH, "node_modules", m)}' for m in NODE_MODULES_LIBS],
            **kwargs,
        )


def get_return_data(tx):
    assert isinstance(tx, Transaction)
    r = tx.return_data
    if isinstance(r, str):
        r = list(map(ord, r))
    return Operators.CONCAT(256, *r)


def get_calldata_uint_arg(input_symbol, arg_ix=0, bits=256):
    offset = (4 + (arg_ix * 32))
    return ABI._deserialize_uint(input_symbol, bits // 8, offset=offset)
