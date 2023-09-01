import pytest
from brownie import MyERC721, accounts

@pytest.fixture
def my_erc721_contract():
    withdrawal_receiver = accounts[1]
    return MyERC721.deploy(withdrawal_receiver, {'from': accounts[0]})

def test_total_tokens_of(my_erc721_contract):
    account = accounts[0]
    mint_limit = my_erc721_contract.mint_limit()

    # Mint tokens
    my_erc721_contract.mint(mint_limit, {'from': account, 'value': mint_limit * my_erc721_contract.price_per_token()})

    assert my_erc721_contract.totalTokensOf(account) == mint_limit

    # Mint more tokens and check the total
    additional_tokens = mint_limit - 1
    my_erc721_contract.mint(additional_tokens, {'from': account, 'value': additional_tokens * my_erc721_contract.price_per_token()})

    assert my_erc721_contract.totalTokensOf(account) == mint_limit * 2 - 1