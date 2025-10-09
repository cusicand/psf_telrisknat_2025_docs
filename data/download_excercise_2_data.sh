# Download data from a temporary FileSender archive containing the Mera MB dataset.
# The link is found by downloading it with a browser, then in Download, right-click on the data and copy download URL.
# See https://www.forbesconrad.com/blog/download-wetransfer-to-linux-server-wget/

wget --user-agent Mozilla/4.0 'https://filesender.renater.fr/download.php?token=70d6a62a-922c-4ccd-bdf2-ae0ca8f47d49&files_ids=60456149' -O excercise_2_data.tar.gz
tar -xzvf excercise_2_data.tar.gz
rm excercise_2_data.tar.gz