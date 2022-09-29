import socket
import sys, time
import subprocess
import json

results = []

def test(input_, expected_out):
    data_socket = socket.socket()

    host = 'localhost'
    port = int(sys.argv[1])
    subprocess.run(f"coverage run ~/server.py {port} &", shell=True)
  
    time.sleep(0.1)
    data_socket.connect((host,port))

    real_out = []
    for cmd in input_:
        data_socket.sendall(cmd.encode('utf-8'))
        mess_recv = str(data_socket.recv(1024),encoding='utf-8')
        real_out.append(mess_recv)
    data_socket.close()

    if real_out == expected_out:
        return True
    else:
        return False

def tester():
    test_list = ["login_test.in", "login_test.out", "channels_test.in", "channels_test.out", 
    "say_test.in", "say_test.out", "error_test.in", "error_test.out"]
    
    i = 0
    while i < len(test_list):
        input_f = []
        with open(test_list[i], "r") as in_read:
            input_ = in_read.readlines()

        for element in input_:
            element = element.strip()
            input_f.append(element)

        with open(test_list[i+1], "r") as in_read:
            output_ = in_read.readlines()
      
        test_name = test_list[i].split('.in')[0]
      
        if test(input_f, output_):
            results.append({test_name:"Passed"})
        else:
            results.append({test_name:"Failed"})
        i+=2

    final_output = json.dumps(results, indent=4)
    with open("test_results.json", "w") as f:
        f.write(final_output)
    subprocess.run(f"coverage report", shell=True)

if __name__ == "__main__":
    tester()
