import os, json, sys
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def install():
    filename = ''
    while(not filename.endswith('.json')):
        Tk().withdraw() 
        filename = askopenfilename() 

    repos = json.load(open(filename))

    for dnf_repo in repos['dnf']:
        print("Installing " + dnf_repo)
        os.system("sudo dnf install -y " + dnf_repo)
        print(dnf_repo + " installed!\n")

    for snap_repo in repos['snap']:
        print("Installing " + snap_repo)
        os.system("sudo snap install " + snap_repo)
        print(snap_repo + " installed!\n")

def backup():
    filename = input('Type the name of the file to save the backup to: ')
    while(filename in os.listdir()):
        old_filename = filename
        filename = input('File already exists. Type the name of the file to save the backup to (or type enter to overwrite): ')
        if(filename == ''):
            filename = old_filename
            break

    os.system(f'dnf repolist --all > {filename}-dnf.txt')
    os.system(f'snap list > {filename}-snap.txt')

    def clean_line(line):
        pos = line.find(' ')
        return line[:pos]

    with open(filename + '-dnf.txt', 'r') as f:
        dnf_repos = f.readlines()[1:]
        dnf_repos = [clean_line(line) for line in dnf_repos]

    with open(filename + '-snap.txt', 'r') as f:
        snap_repos = f.readlines()[1:]
        snap_repos = [clean_line(line) for line in snap_repos]

    repos = {
        'dnf': dnf_repos,
        'snap': snap_repos
    }
    
    os.remove(filename + '-dnf.txt')
    os.remove(filename + '-snap.txt')

    with open(filename + '.json', 'w') as f:
        json.dump(repos, f)
    
    print(f'{len(repos["dnf"])} dnf repos backed up to {filename}.json')
    print(f'{len(repos["snap"])} snap repos backed up to {filename}.json')

options = {
    'install': install,
    'backup': backup
}

arg = sys.argv[1]
options[arg]()