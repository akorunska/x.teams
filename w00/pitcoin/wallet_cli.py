import cmd, os
from pathlib import Path
from pitcoin.wallet import *
from pitcoin.transaction import *

# todo rewrite all functions to receive and return a string + add test coverage

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
        result = {'compressed': True, 'save_address': False, 'args_valid': False}
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
        if not Path(result['filepath']).is_file():
            print(result['filepath'], "is not a file")
            return result
        result['args_valid'] = True
        return result

    @staticmethod
    def handle_do_remember_privkey_options(arg):
        result = {'privkey': ""}
        args = arg.split()
        if len(args[0]) == 64:
            result["privkey"] = args[0]
        else:
            print("seems like specified private key is not correct.")
        return result

    @staticmethod
    def handle_do_send_options(arg, privkey):
        result = {'recipient': "", 'address': "", 'amount': -1, 'args_valid': False}
        if privkey == "":
            print("please, specify your private key using <remember_privkey> command before calling send")
            return result
        args = arg.split()
        if len(args) != 2:
            print("wrong number of arguments")
            return result
        # todo check if recipient and sender addresses are valid
        result['recipient'] = args[0]
        result['amount'] = int(args[1])
        result['sender'] = read_file_contents('address')
        if result['amount'] <= 0:
            print("amount specified is not positive integer")
            return result
        result['args_valid'] = True
        return result


class WalletCLI(cmd.Cmd):
    intro = 'Welcome to pitcoin wallet-cli. Type help or ? to list commands.\n'
    prompt = '\n(pitcoin-wallet-cli) '
    user_privkey = ""
    i = 0

    def do_new(self, arg):
        'Generate new private key and receive associated public key and address. \n' \
        'usage: <new -u -a> \n' \
        '-u: By default compressed public key is used. To use uncompressed public key type <new -u> \n' \
        '-a: Save created address to the file on the machine called address.'

        options = OptionsHandler.handle_do_new_options(arg)

        hex_private_key = generate_private_key()
        wif_private_key = convert_hex_private_key_to_wif(hex_private_key)
        self.hande_wallet_credentials_generation(options, hex_private_key, wif_private_key.decode("utf-8"))

    def do_import(self, arg):
        'Import private key in WIF format and receive associated public key and address. \n' \
        'usage: <import path/to/file -u -a> \n' \
        '-u: By default compressed public key is used. To use uncompressed public key type <new -u> \n' \
        '-a: Save created address to the file on the machine called address.'
        options = OptionsHandler.handle_do_import_options(arg)
        if not options['args_valid']:
            return
        wif_private_key = read_file_contents(options['filepath'])
        # todo check if wif in the file is valid
        hex_private_key = convert_wif_to_hex_private_key(wif_private_key)
        self.hande_wallet_credentials_generation(options, hex_private_key.decode("utf-8"), wif_private_key)

    def do_remember_privkey(self, arg):
        'Command, that must be called before any send operation. ' \
        'Private key is stored in program memory and needs remembered every time wallet-cli is relauched \n' \
        'usage: <remember_privkey user_hex_privkey>'
        options = OptionsHandler.handle_do_remember_privkey_options(arg)
        self.user_privkey = options['privkey']

    def do_send(self, arg):
        'Send some pitcoins to another address\n' \
        'usage: <send recipient_address amount>'
        options = OptionsHandler.handle_do_send_options(arg, self.user_privkey)
        if not options['args_valid']:
            return
        tx = Transaction(options['sender'], options['recipient'], options['amount'])
        tx.sign_transaction(self.user_privkey)
        print(tx)
        print(Serializer.serialize_transaction(tx))

    def do_quit(self, arg):
        'Exit wallet-cli shell'
        print('Thank you for using pitcoin-wallet-cli')
        return True

    # service static methods, containing repetative logic
    @staticmethod
    def hande_wallet_credentials_generation(options, hex_private_key, wif_private_key):
        public_key = get_public_key_from_private_key(hex_private_key, options['compressed'])
        address = get_address_from_private_key(hex_private_key, options['compressed'])

        WalletCLI.print_wallet_info(hex_private_key, wif_private_key, public_key.decode("utf-8"), address)
        if options["save_address"]:
            WalletCLI.save_address_to_file(address)

    @staticmethod
    def print_wallet_info(hex_private_key, wif_private_key, public_key, address):
        print("hex private key | ", hex_private_key)
        print("wif private key | ", wif_private_key)
        print("public key      | ", public_key)
        print("pitcoin address | ", address)

    @staticmethod
    def save_address_to_file(address):
        file = open("address", "w")
        file.write(address)
        file.close()


if __name__ == '__main__':
    WalletCLI().cmdloop()
