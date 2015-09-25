import os
import shutil
import time

class MaildirConverter:

    def __init__(self, from_dir, to_dir):
        self.from_dir = os.path.abspath(from_dir)
        self.to_dir = os.path.abspath(to_dir)

    def get_message_name(self, count):
        """This function will return a new Maildir format name
        """
        unix_time = time.time()
        cur_pid = os.getpid()
        message_name = "{:f}.{}.{:07}". format(unix_time, cur_pid, count)

        return message_name

    def create_folder_tree(self, target_path):
        """This function will create cur, tmp, new folder for each subfolder.
        """
        cur_dir = os.path.join(target_path, "cur")
        new_dir = os.path.join(target_path, "new")
        tmp_dir = os.path.join(target_path, "tmp")

        for sub_dir in [cur_dir, new_dir, tmp_dir]:
            if not os.path.isfile(sub_dir):
                os.makedirs(sub_dir)

    def convert_message(self, old_sub_folder_abspath, new_sub_folder_abspath, message, count = 0):
        """Copy and rename original message into new folder under currect directory
        """
        old_message_full_path = os.path.join(old_sub_folder_abspath, message)

        new_message_name = self.get_message_name(count)
        new_message_full_path = os.path.join(new_sub_folder_abspath, 'new', new_message_name)

        try:
            shutil.copy(old_message_full_path, new_message_full_path)
        except (IOError, os.error) as e:
            print 'Can not convert message: {} with error: {}'.format(old_message_full_path, e)

    def get_home_mapping(self):
        old_new_home_mapping = {}
        email_address_source_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'email_address.txt')
        with open(email_address_source_path, 'r') as email_address:
            for line in email_address:
                if line.find('|') >= 0:
                    old_new = line.split('|')
                    old_new_home = old_new[1].split('@')
                    old_new_home_mapping[old_new[0]] = old_new_home[0]

        return old_new_home_mapping

    def run(self):
        if not os.path.isdir(self.from_dir):
            print 'Not a valid from dir: {}'.format(self.from_dir)
            return

        if not os.path.isdir(self.to_dir):
            os.makedirs(self.to_dir)

        old_new_home_mapping = self.get_home_mapping()

        print 'started'
        for user_home in os.listdir(self.from_dir):
            if not os.path.isdir(os.path.join(self.from_dir, user_home)):
                print '{} is not a dir!'.format(user_home)
                continue

            if not user_home in old_new_home_mapping.keys():
                print 'Can not find email address mapping for user home:{}!'.format(user_home)
                continue

            old_user_home_abspath = os.path.join(self.from_dir, user_home)
            new_user_home_abspath = os.path.join(self.to_dir, old_new_home_mapping[user_home])
            os.makedirs(new_user_home_abspath)
            os.chdir(old_user_home_abspath)

            for root, folders, messages in os.walk('.'):
                old_sub_folder_abspath = os.path.join(old_user_home_abspath, root)
                new_sub_folder_abspath = os.path.join(new_user_home_abspath, root)

                if root != '.':
                    self.create_folder_tree(new_sub_folder_abspath)

                for index, message in enumerate(messages):
                    self.convert_message(old_sub_folder_abspath, new_sub_folder_abspath, message, index)

        print 'ended'


if __name__ == '__main__':
    from_dir = '/Volumes/My Passport/Enron_Email_Dataset/orig_maildir'
    to_dir   = '/Volumes/My Passport/Enron_Email_Dataset/convert_maildir_03'

    maildir_converter = MaildirConverter(from_dir, to_dir)
    maildir_converter.run()
