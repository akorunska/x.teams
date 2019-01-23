import cmd, os
from pathlib import Path
from pitcoin.wallet import *


def print_wallet_info(hex_private_key, wif_private_key, public_key, address):
    print("hex private key | ", hex_private_key)
    print("wif private key | ", wif_private_key)
    print("public key      | ", public_key)
    print("pitcoin address | ", address)


def save_address_to_file(address):
    file = open("address", "w")
    file.write(address)
    file.close()


class OptionsHandler:
    @staticmethod
    def handle_do_new_options(arg):
        result = {'compressed': True, 'save_address': False}
        args = arg.split()
        for arg in args:
            if arg == "-u":
                print("using uncompressed public key for address creation")
                result['compressed'] = False
            elif arg == "-a":
                print("created address is going to be saved in file named 'address'")
                result["save_address"] = True
            else:
                print("unknown option:", arg)
        return result

    @staticmethod
    def handle_do_import_options(arg):
        result = {'compressed': True, 'save_address': False}
        args = arg.split()
        result['filepath'] = args[0]
        for i in range(1, len(args)):
            if args[i] == "-u":
                print("using uncompressed public key for address creation")
                result['compressed'] = False
            elif args[i] == "-a":
                print("created address is going to be saved in file named 'address'")
                result["save_address"] = True
            else:
                print("unknown option:", args[i])
        return result


class WalletCLI(cmd.Cmd):
    intro = 'Welcome to pitcoin wallet-cli. Type help or ? to list commands.\n'
    prompt = '\n(pitcoin-wallet-cli) '

    def do_new(self, arg):
        'Generate new private key and receive associated public key and address. \n' \
        'usage: <new -u -a> \n' \
        '-u: By default compressed public key is used. To use uncompressed public key type <new -u> \n' \
        '-a: Save created address to the file on the machine called address.'

        options = OptionsHandler.handle_do_new_options(arg)

        hex_private_key = generate_private_key()
        wif_private_key = convert_hex_private_key_to_wif(hex_private_key)
        public_key = get_public_key_from_private_key(hex_private_key, options['compressed'])
        address = get_address_from_private_key(hex_private_key, options['compressed'])

        print_wallet_info(hex_private_key, wif_private_key.decode("utf-8"), public_key.decode("utf-8"), address)
        if options["save_address"]:
            save_address_to_file(address)

    def do_import(self, arg):
        'Import private key in WIF format and receive associated public key and address. \n' \
        'usage: <import path/to/file -u -a> \n' \
        '-u: By default compressed public key is used. To use uncompressed public key type <new -u> \n' \
        '-a: Save created address to the file on the machine called address.'

        options = OptionsHandler.handle_do_import_options(arg)
        if Path(options['filepath']).is_file() != True:
            print(options['filepath'], "is not a file")
            return

        wif_private_key = read_file_contents(options['filepath'])
        # todo check if wif in the file is valid
        hex_private_key = convert_wif_to_hex_private_key(wif_private_key)
        public_key = get_public_key_from_private_key(hex_private_key, options['compressed'])
        address = get_address_from_private_key(hex_private_key, options['compressed'])

        print_wallet_info(hex_private_key.decode("utf-8"), wif_private_key, public_key.decode("utf-8"), address)
        if options["save_address"]:
            save_address_to_file(address)

    def do_quit(self, arg):
        'Exit wallet-cli shell'
        print('Thank you for using pitcoin-wallet-cli')
        return True


if __name__ == '__main__':
    WalletCLI().cmdloop()
