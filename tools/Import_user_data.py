from passlib.hash import sha256_crypt

class ImportEmailData:

    def __init__(self):
        pass

    def run(self):
        users = open('users.txt', 'w+')
        with open('email_address.txt', 'r') as email_address:
            for line in email_address:
                email = line.split('|')[1]
                userid = email.split('@')[0]
                users.write('{}|{}|{}\n'.format(userid, 'enron.com', sha256_crypt.encrypt('12345', rounds=5000)))

        users.close()


if __name__ == '__main__':
    importemaildata_util = ImportEmailData()
    importemaildata_util.run()
