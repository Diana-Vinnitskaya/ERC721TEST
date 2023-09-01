import pytest
from brownie import MyERC721, accounts
from web3 import Web3

@pytest.fixture
def my_erc721_contract():
    withdrawal_receiver = accounts[1]
    return MyERC721.deploy(withdrawal_receiver, {'from': accounts[0]})

def test_withdraw(my_erc721_contract):
    withdrawal_receiver = my_erc721_contract.getWithdrawalReceiver()
    owner = accounts[0]
    non_owner = accounts[2]

    initial_balance = my_erc721_contract._balance()

    # Non-owner trying to withdraw should fail
    with pytest.raises(Exception):
        my_erc721_contract.withdraw({'from': non_owner})

    # Owner withdrawing
    my_erc721_contract.withdraw({'from': owner})
    assert my_erc721_contract._balance() == 0
    