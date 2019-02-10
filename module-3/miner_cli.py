from pitcoin_modules.blockchain import Blockchain


blockchain = Blockchain()


def consensus():
    pass


def mine():
    while True:
        result = blockchain.mine_and_submit_block()
        if result:
            print("new block was mined and broadcast to the network. block hash is: ", result)
        else:
            print("block was mined by other node, continuing on the new chain.")


if __name__ == "__main__":
    # get_known_nodes()
    # consensus()
    mine()

