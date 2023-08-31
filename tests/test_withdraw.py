import pytest
from brownie import MyERC721, WithdrawalReceiver, accounts

@pytest.fixture
def my_erc721_contract():
    withdrawal_receiver = accounts[1]
    return MyERC721.deploy(withdrawal_receiver, {'from': accounts[0]})

def test_withdraw(my_erc721_contract):
    withdrawal_receiver = my_erc721_contract.withdrawalReceiver()
    owner = accounts[0]
    non_owner = accounts[2]

    initial_balance = my_erc721_contract.balance()
    amount_to_withdraw = 1000  # adjust this based on your scenario

    # Non-owner trying to withdraw should fail
    with pytest.raises(Exception):
        my_erc721_contract.withdraw({'from': non_owner})

    # Owner withdrawing
    my_erc721_contract.withdraw({'from': owner})
    assert my_erc721_contract.balance() == 0
    assert withdrawal_receiver.balance() == initial_balance

    # Trying to withdraw again should fail (no balance left)
    with pytest.raises(Exception):
        my_erc721_contract.withdraw({'from': owner})

    # Withdraw with a specific amount
    my_erc721_contract.withdraw(amount_to_withdraw, {'from': owner})
    assert withdrawal_receiver.balance() == initial_balance + amount_to_withdraw
