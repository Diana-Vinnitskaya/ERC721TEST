from brownie import MyERC721, network, config, accounts


def deploy_contract():
    account = accounts[0]
    contract = MyERC721.deploy(account, {"from" : account})
    print("contract has been deployed successfully to :", contract.address)

    return contract

def main():
    deploy_contract()