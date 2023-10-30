import subprocess
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

sshKey = os.getenv("VCS_SSH_KEY")
iType = os.getenv("VCS_ITYPE")
pType = os.getenv("VCS_PTYPE")
img = os.getenv("VCS_IMG")
secg = os.getenv("VCS_SECG")
net = os.getenv("VCS_NET")
keyPath = os.getenv("VCS_KEY_PATH")

def ListVCS(waitTime):
    print("wait for "+str(waitTime)+" secs")
    time.sleep(waitTime)
    print("list vcs")
    cmd = "twccli ls vcs -json"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
    if output == "":
        print("no vcs found")
    else:
        output = json.loads(output)
        print(f"find {len(output)} vcs")
        #print(output)


def CreateVCS():
    print("create vcs")
    cmd = f"twccli mk vcs -key {sshKey} -itype {iType} -ptype {pType} -secg {secg} -net {net} -fip -wait -json"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
    output = json.loads(output)
    #print(output)
    return output["id"]

def RunCommand(vcsID, cmd):
    print("run command "+cmd)
    info = f"twccli ls vcs -s {vcsID} -json".split(" ")
    result = subprocess.run(info, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').strip()
    print(output)
    ip = json.loads(output)[0]["public_ip"]
    print(ip)
    sshCmd = f"ssh -t -o StrictHostKeyChecking=no ubuntu@{ip} -i {keyPath}"
    sshCmd = sshCmd.split(" ")+["/bin/bash "+cmd]
    print(sshCmd)
    result = subprocess.run(sshCmd, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)

def DeleteVCS(vcsID):
    print(f"delete vcs {vcsID}")
    cmd = f"twccli rm vcs -f -s {vcsID}"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)

if __name__ == "__main__":
    ListVCS(0)
    vcsID = CreateVCS()
    ListVCS(30)
    RunCommand(vcsID, "./out.sh")
    DeleteVCS(vcsID)
    ListVCS(60)
