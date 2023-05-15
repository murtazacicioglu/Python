from input_module import take_input
from process_module import process
from output_module import output
import welcome
import os
import assistant_details as ad
from database import listen_is_on
from listen_module import listen
from AIBot import response
from automatic import check_last_modify

my_file = "setup.py"

if os.path.isfile(my_file):
    import setup

os.system('cls')

def installation():
    f = open("setup.py", "a")
    print("-----------Hoşgeldinn Assistant------------")
    output("Size nasıl seslenmemi istersiniz")
    status = take_input()
    statement1 = 'status = "' + status + '"' + '\n'
    f.write(statement1)
    output("Müzik yolunu belirlemek ister misiniz?")
    ans = take_input()
    if ans.lower() == 'yes':
        output("Müzik yolunu giriniz.")
        path = take_input()
        statement2 = 'music_path = "' + path + '"' + '\n'
        f.write(statement2)
    else:
        statement2 = 'music_path = "' + '"' + '\n'
        f.write(statement2)
    f.close()

if os.path.isfile(my_file): 
    status = setup.status
    check_last_modify()
    welcome.greet(status) 
    while True:
        if listen_is_on():
            i = listen()
        else:
            i = take_input()
        o = process(i) 
        output(o)
else:
    installation() 
    import setup
    status = setup.status
    welcome.greet(status)

    while True:
        if listen_is_on():
            i = listen()
        else:
            i = take_input()
        o = process(i)
        output(o)
