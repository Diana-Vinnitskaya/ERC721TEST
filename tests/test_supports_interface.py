import pytest
from brownie import MyERC721, accounts

@pytest.fixture
def my_erc721_contract():
    withdrawal_receiver = accounts[1]
    return MyERC721.deploy(withdrawal_receiver, {'from': accounts[0]})

def test_supports_interface(my_erc721_contract):
    supported_interfaces = [
        "0x80ac58cd",  # ERC721
        "0x780e9d63",  # ERC721Enumerable
        "0x5b5e139f",  # ERC721Burnable
    ]

    for interface_id in supported_interfaces:
        assert my_erc721_contract.supportsInterface(interface_id)

    unsupported_interface = "0x5f46473f" 
    assert not my_erc721_contract.supportsInterface(unsupported_interface)