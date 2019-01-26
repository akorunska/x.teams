import cmd
from pitcoin.blockchain import Blockchain


class MinerCLI(cmd.Cmd):
    intro = 'Welcome to pitcoin miner-cli. Type help or ? to list commands.\n'
    prompt = '\n(pitcoin-miner-cli) '
    blockchain = Blockchain()
    i = 0

    def do_mine(self, arg):
        'Initiate mining process. \n'
        data = self.blockchain.mine_and_submit_block()
        print(data.__dict__)

    def do_add_node(self, arg):
        'Add new node address to the list of nodes\n' \
        'usage: add_node http://127.0.0.1:3001'
        print(self.blockchain.add_node(arg.strip()))

    def do_consensus(self, arg):
        'Check other node`s chains.'\
        ' If some of them in longer than current chain, replace current chain with the longest'
        self.blockchain.resolve_conflicts()

    def do_quit(self, arg):
        'Exit wallet-cli shell'
        print('Thank you for using pitcoin-wallet-cli')
        return True


if __name__ == '__main__':
    MinerCLI().cmdloop()

