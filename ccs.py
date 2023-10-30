import subprocess
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

iType = os.getenv("CCS_ITYPE")
gpuNum = os.getenv("CCS_GPU_NUM")

def ListCCS(waitTime):
    print("wait for "+str(waitTime)+" secs")
    time.sleep(waitTime)
    print("list ccs")
    cmd = "twccli ls ccs -json"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)
    if output == "":
        print("no ccs found")
    else:
        output = json.loads(output)
        print(f"find {len(output)} ccs")
        print(output)


def CreateCCS():
    print("create ccs")
    cmd = f"twccli mk ccs -itype {iType} -gpu {gpuNum} -wait -json"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    output = json.loads(output)
    print(output)
    return output["id"]

def RunCommand(ccsID, cmd):
    print("run command "+cmd)
    sshInfo = f"twccli ls ccs -gssh -s {ccsID}".split(" ")
    result = subprocess.run(sshInfo, stdout=subprocess.PIPE)
    sshInfo = result.stdout.decode('utf-8').strip()
    print(sshInfo)
    sshCmd = f"ssh -t -o StrictHostKeyChecking=no {sshInfo}"
    sshCmd = sshCmd.split(" ")+["/bin/bash "+cmd]
    print(sshCmd)
    result = subprocess.run(sshCmd, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)

def DeleteCCS(ccsID):
    print(f"delete ccs {id}")
    cmd = f"twccli rm ccs -f -s {ccsID}"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)

if __name__ == "__main__":
    ListCCS(0)
    ccsID = CreateCCS()
    ListCCS(30)
    RunCommand(ccsID, "./out.sh")
    DeleteCCS(ccsID)
    ListCCS(60)
