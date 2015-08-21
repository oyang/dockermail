#!/bin/bash

SRC_DIR='/Volumes/My Passport/Enron_Email_Dataset_AWS_Mbox'
DEST_DIR='/Volumes/My Passport/Enron_Email_Dataset_AWS_Maildir'


function convert_mbox_to_maildir() {
    ls "$SRC_DIR" | while read sub_dir ; do 
        local home_dir=$(find "$SRC_DIR/$sub_dir" ! -path . -type d -maxdepth 1 -mindepth 1 -exec echo {} \; )
        local user_name=$(ls    "$SRC_DIR/$sub_dir")
        local dest_user_dir="$DEST_DIR/$user_name"
        echo "home_dir: $home_dir"
        echo "dest_user_dir: $dest_user_dir"
        ./mb2md-3.20.pl -R -s "$home_dir" -d "$dest_user_dir"
        echo

    done

}

function finding_email_address() {
    cd "$DEST_DIR"
    ls | while read user_dir ; do
        #cat "$user_dir/*000100.mbox:2,S" | grep -e 'To:'
        ls "$user_dir/.Inbox/cur/"*000000.mbox:2,S
        cat `ls "$user_dir/.Inbox/cur/"*000000.mbox:2,S` | grep -i -E '\(^To: \|^CC: \).*enron.com>$'
    done
}


function main() {
    convert_mbox_to_maildir
}


main $*
