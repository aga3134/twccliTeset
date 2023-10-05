import subprocess
import time
import json

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
    cmd = "twccli mk ccs -itype PyTorch -gpu 1 -wait -json"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    output = json.loads(output)
    print(output)
    return output["id"]

def DeleteCCS(id):
    print(f"delete ccs {id}")
    cmd = f"twccli rm ccs -f -s {id}"
    result = subprocess.run(cmd.split(" "), stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    print(output)

if __name__ == "__main__":
    ListCCS(0)
    ccsID = CreateCCS()
    ListCCS(30)
    DeleteCCS(ccsID)
    ListCCS(60)
