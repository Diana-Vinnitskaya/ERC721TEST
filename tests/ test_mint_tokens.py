import pytest
from brownie import MyERC721, WithdrawalReceiver, accounts

@pytest.fixture
def my_erc721_contract():
    withdrawal_receiver = accounts[1]
    return MyERC721.deploy(withdrawal_receiver, {'from': accounts[0]})

def test_mint(my_erc721_contract):
    account = accounts[0]
    mint_limit = my_erc721_contract.mint_limit()
    price_per_token = my_erc721_contract.price_per_token()

    # Mint within limit
    my_erc721_contract.mint(mint_limit, {'from': account, 'value': mint_limit * price_per_token})
    assert my_erc721_contract.balanceOf(account) == mint_limit

    # Mint exceeding limit should fail
    with pytest.raises(Exception):
        my_erc721_contract.mint(1, {'from': account, 'value': price_per_token})

    # Mint exceeding max supply should fail
    with pytest.raises(Exception):
        my_erc721_contract.mint(1, {'from': account, 'value': price_per_token * mint_limit})

    # Mint with incorrect ether amount should fail
    with pytest.raises(Exception):
        my_erc721_contract.mint(1, {'from': account, 'value': price_per_token + 1})
