import cmd
from pitcoin_modules.blockchain import Blockchain


class MinerCLI(cmd.Cmd):
    intro = 'Welcome to pitcoin_modules miner-cli. Type help or ? to list commands.\n'
    prompt = '\n(pitcoin-miner-cli) '
    blockchain = Blockchain()
    i = 0

    def do_mine(self, arg):
        'Initiate mining process. \n'
        data = self.blockchain.mine_and_submit_block()
        print("block was mined and broadcasted to other nodes")
        print("hash of the new block: ", data)

    def do_add_node(self, arg):
        'Add new node address to the list of nodes\n' \
        'usage: add_node http://127.0.0.1:3001'
        url = arg.strip()
        self.blockchain.add_node(url)

    def do_consensus(self, arg):
        'Check other node`s chains.'\
        ' If some of them in longer than current chain, replace current chain with the longest'
        res = self.blockchain.resolve_conflicts()
        if res == "":
            print("No conflicts found")
        else:
            print("Loaded new chain from ", res['source'], " with length ", res['len'])

    def do_quit(self, arg):
        'Exit wallet-cli shell'
        print('Thank you for using pitcoin_-wallet-cli')
        return True


if __name__ == '__main__':
    MinerCLI().cmdloop()

