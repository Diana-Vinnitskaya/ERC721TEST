import pytest
from brownie import MyERC721, accounts

@pytest.fixture
def my_erc721_contract():
    withdrawal_receiver = accounts[1]
    return MyERC721.deploy(withdrawal_receiver, {'from': accounts[0]})

def test_mint(my_erc721_contract):
    account = accounts[0]
    mint_limit = my_erc721_contract.mint_limit()
    price_per_token = my_erc721_contract.price_per_token()
    limit_for_address =  my_erc721_contract.limit_for_address()

    # Mint exceeding limit should fail
    with pytest.raises(Exception):
        my_erc721_contract.mint(4, {'from': account, 'value': price_per_token * 4})


    # Mint within limit
    my_erc721_contract.mint(mint_limit, {'from': account, 'value': mint_limit * price_per_token})
    assert my_erc721_contract.balanceOf(account) == mint_limit

    my_erc721_contract.mint(mint_limit, {'from': account, 'value': mint_limit * price_per_token})
    assert my_erc721_contract.balanceOf(account) ==  limit_for_address

    # Exceeding limit per account should fail
    with pytest.raises(Exception):
        my_erc721_contract.mint(2, {'from': account, 'value': price_per_token * 2})

    # Mint with incorrect ether amount should fail
    with pytest.raises(Exception):
        my_erc721_contract.mint(1, {'from': account, 'value': price_per_token + 1})