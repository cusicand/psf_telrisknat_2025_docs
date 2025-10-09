# Download data from a temporary FileSender archive containing the Mera MB dataset.
# The link is found by downloading it with a browser, then in Download, right-click on the data and copy download URL.
# See https://www.forbesconrad.com/blog/download-wetransfer-to-linux-server-wget/

wget --user-agent Mozilla/4.0 'https://filesender.renater.fr/download.php?token=d3e04c75-60f0-4abf-8f3b-aa23f58b680e&files_ids=60460478' -O excercise_3_data.tar.gz
tar -xzvf excercise_3_data.tar.gz
rm excercise_3_data.tar.gz