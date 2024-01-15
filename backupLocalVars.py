import subprocess
import time
from os.path import getmtime as lastEditTime
import gzip
from pickle import load

while True:

    subprocess.run("cp -r Variables/ Variables_backupLocal_new", shell=True)


    filesNew = [f for f in subprocess.run("find Variables_backupLocal_new -type f", shell=True, stdout=subprocess.PIPE).stdout.decode().split("\n") if len(f) != 0]
    filesOld = [f for f in subprocess.run("find Variables_backupLocal -type f", shell=True, stdout=subprocess.PIPE).stdout.decode().split("\n") if len(f) != 0]


    for newPath in filesNew:
        if ".DS_Store" in newPath:
            continue
        
        oldPath = newPath.replace("_new", "")
        originalPath = oldPath.replace("_backupLocal", "")
        
        print(f"Checking {originalPath}", end='')
        
        if oldPath not in filesOld:
            print(" --> new File! Backing up!", flush=True)
            subprocess.run(f"mv {newPath} {oldPath}", shell=True)

        else:
            originalTime = lastEditTime(originalPath)
            backupTime = lastEditTime(oldPath)
            #print(" --> got edit times for current file and last backup", end='')
            if originalTime >= backupTime:
                try:
                    load(gzip.open(newPath, "rb"))
                    print(f" --> Backed up!", flush=True)
                    subprocess.run(f"mv {newPath} {oldPath}", shell=True)
                except:
                    print(" --> New file is corrupted, DID NOT BACKUP!", flush=True)
            else:
                print(" --> Backup is already updated!", flush=True)

    subprocess.run("rm -r Variables_backupLocal_new", shell=True)
    
    print("\n\n\n")

    
    time.sleep(900)

