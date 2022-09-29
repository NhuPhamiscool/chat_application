#!/bin/bash

# formatting the output file in json
echo -e "[\n\t" > result.json
python3 ~/server/server.py 1223 & # run the server in the background
sleep 0.1
# the file of bunch of inputs
# mess_login=~/server/testing_folder/test_case_1/login_test.in 

# python3 ~/server/testing_folder/client_test.py 1223 $mess_login > login_output.txt
# dif=`diff login_output.txt ~/server/testing_folder/test_case_1/login_test.out`
# echo $dif

# if [ "$dif" != "" ]; then
#     echo -e '{ "login_test" : "failed" }' >> result.json
# else
#     echo -e '{ "login_test" : "passed" }' >> result.json
# fi

# pid=`ps aux | grep client_test.py | tr -s ' ' | cut -d ' ' -f2`
# kill -2 $pid
# ------------------------------------------------------------------------------

mess_channel=~/server/testing_folder/test_case_2/channels_test.in 

python3 ~/server/testing_folder/client_test.py 1223 $mess_login > login_output.txt
dif=`diff login_output.txt ~/server/testing_folder/test_case_1/login_test.out`
echo $dif

if [ "$dif" != "" ]; then
    echo -e '{ "login_test" : "failed" }' >> result.json
else
    echo -e '{ "login_test" : "passed" }' >> result.json
fi
# python3 ~/server/server.py 1223 & # run the server in the background
# mess_channel=~/server/testing_folder/test_case_2/channels_test.in
# python3 ~/server/testing_folder/client_test.py 1223 $mess_channel > channel_output.txt
# # dif=`python3 ~/server/testing_folder/client_test.py < ~/server/testing_folder/test_case_1/testing_1.in | diff - ~/server/testing_folder/test_case_1/testing_1.out`
# dif_channel=`diff channel_output.txt ~/server/testing_folder/test_case_2/channels_test.out`
# echo $dif_channel

# if [ "$dif_channel" != "" ]; then
#     echo '{ "channels_test" : "failed" }' >> result.json
# else
#     echo '{ "channels_test" : "passed" }' >> result.json
# fi
# kill -2
# mess_1="REGISTER NHU JI"
# python3 ~/server/testing_folder/client_test.py 1224 $mess_1 > register.in
# dif_1=`diff register.in ~/server/testing_folder/test_case_1/register_pass.out`
# echo $dif_1

# if [ "-z $dif_1" ]; then
#     echo '{ "register_test" : "failed" }' >> result.json
# else
#     echo '{ "register_test" : "passed" }' >> result.json
# fi

# --------------------------------------------------------------------------------

# mess_2="CREATE SU"
# python3 ~/server/testing_folder/client_test.py 1224 $mess_2 > create.in
# dif_2=`diff create.in ~/server/testing_folder/test_case_1/create_fail.out`
# echo $dif_2

# if [ "-z $dif_2" ]; then
#     echo '{ "create_test" : "failed" }' >> result.json
# else
#     echo '{ "create_test" : "passed" }' >> result.json
# fi


# python3 server.py 1223 &
# echo server_test.txt > python3 client.py | reult.txt 



# diff empty.csv ~/cald/test_daemon/add_event.out

