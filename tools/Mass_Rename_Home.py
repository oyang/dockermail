import os

class MassRenameHome:

    def __init__(self, working_dir):
        self.working_dir = working_dir

    def rename_single_home(self, old_name, new_name):
        os.rename(old_name, new_name)

    def rename_mass_home(self, old_new_home_mapping):
        for old_home, new_home in old_new_home_mapping.iteritems():
            try:
                self.rename_single_home(old_home, new_home)
            except (IOError, os.error) as e:
                print 'can not rename {} to {} with {}!'.format(old_home, new_home, e)

    def get_home_mapping(self):
        old_new_home_mapping = {}
        with open('email_address.txt', 'r') as email_address:
            for line in email_address:
                if line.find('|') >= 0:
                    old_new = line.split('|')
                    old_new_home = old_new[1].split('@')
                    old_new_home_mapping[old_new[0]] = old_new_home[0]

        return old_new_home_mapping

    def run(self):
        old_new_home_mapping = self.get_home_mapping()

        os.chdir(working_dir)
        self.rename_mass_home(old_new_home_mapping)



if __name__ == '__main__':
    working_dir = '/Volumes/My Passport/Enron_Email_Dataset/convert_maildir'
    massrename_util = MassRenameHome(working_dir)
    massrename_util.run()
