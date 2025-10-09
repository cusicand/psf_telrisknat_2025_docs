# Download data from a temporary FileSender archive containing the Mera MB dataset.
# The link is found by downloading it with a browser, then in Download, right-click on the data and copy download URL.
# See https://www.forbesconrad.com/blog/download-wetransfer-to-linux-server-wget/

wget --user-agent Mozilla/4.0 'xxxxx' -O excercise_4_data.tar.gz
tar -xzvf excercise_4_data.tar.gz
rm excercise_4_data.tar.gz