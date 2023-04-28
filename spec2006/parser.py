#!/usr/bin/python3
import os
import sys

if len(sys.argv) != 2:
    sys.exit()

path = sys.argv[1]
path = os.chdir(path)

rootDir = os.getcwd()
benchList = os.listdir(os.getcwd())
benchList.remove('bench-script')
benchList.sort()

for benchDir in benchList:
    os.chdir(benchDir + '/result')

    resRawFiles = os.listdir(os.getcwd())

    result = [benchDir]
    totalTime = 0
    vmRSS = 0
    isSignal = False

    for raw in resRawFiles:
        f = open(raw)

        for line in f.readlines():
            if isSignal:
                break

            if "signal" in line:
                isSignal = True
                break
            if "Maximum resident set size" in line:
                words = line.split(':')
                vmRSS += int(words[-1])
            if "Elapsed (wall clock) time" in line:
                words = line.split(' ')
                time = words[-1].split(':')
                if len(time) == 3:
                    h, mm, ss = time
                    totalTime += float(h.replace('\n', '')) * 360 + float(mm.replace('\n', '')) * 60 + float(ss.replace('\n', ''))
                else:
                    mm, ss = time
                    totalTime += float(mm.replace('\n', '')) * 60 + float(ss.replace('\n', ''))

        f.close()

    print("{}\t{}\t{}".format(benchDir, totalTime, vmRSS));


    os.chdir(rootDir)

