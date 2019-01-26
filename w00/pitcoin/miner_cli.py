import cmd
from pitcoin.blockchain import Blockchain


class MinerCLI(cmd.Cmd):
    intro = 'Welcome to pitcoin miner-cli. Type help or ? to list commands.\n'
    prompt = '\n(pitcoin-miner-cli) '
    blockchain = Blockchain()
    i = 0

    def do_mine(self, arg):
        'Initiate mining process. \n'
        self.blockchain.mine_and_submit_block()

    def do_add_node(self, arg):
        self.blockchain.add_node(arg.strip())

    def do_quit(self, arg):
        'Exit wallet-cli shell'
        print('Thank you for using pitcoin-wallet-cli')
        return True


if __name__ == '__main__':
    MinerCLI().cmdloop()

