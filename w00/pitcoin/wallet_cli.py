import cmd, sys
from pitcoin.wallet import *


def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


class WalletCLI(cmd.Cmd):
    intro = 'Welcome to pitcoin wallet-cli. Type help or ? to list commands.\n'
    prompt = '(pitcoin-wallet-cli) '

    def do_new(self, arg):
        'Generate new private key and receive associated public key and address. \n' \
        'By default compressed public key is used. \n'\
        'To use uncompressed key type <new --uncompressed-pubkey>.'

        hex_private_key = generate_private_key()
        wif_private_key = convert_hex_private_key_to_wif(hex_private_key)
        compressed = True
        if arg != "":
            if arg == "--uncompressed-pubkey":
                print("using uncompressed public key for address creation")
                compressed = False
            else:
                print("Unknown option:", arg)
        public_key = get_public_key_from_private_key(hex_private_key, compressed)
        address = get_address_from_private_key(hex_private_key, compressed)

        print("hex private key | ", hex_private_key)
        print("wif private key | ", wif_private_key.decode("utf-8"))
        print("public key      | ", public_key.decode("utf-8"))
        print("pitcoin address | ", address)


    def do_quit(self, arg):
        'Exit wallet-cli shell'
        print('Thank you for using pitcoin-wallet-cli')
        return True


if __name__ == '__main__':
    WalletCLI().cmdloop()

