import subprocess
import multiprocessing
import socket
import os
import time 
from multiprocessing import Process, Queue
from file_helper import check_directory



def hostname_scan(target_hosts, output_directory, quiet):
    check_directory(output_directory)
    output_file = output_directory + "/hostnames.txt"
    f = open(output_file, 'w')
    print("[+] Writing hostsnames to: %s" % output_file)
    
    hostnames = 0
    SWEEP = ''

    if(os.path.isfile(target_hosts)):
        SWEEP = "nbtscan -q -f %s" % (target_hosts)
    else:
        SWEEP = "nbtscan -q %s" % (target_hosts)

    results = subprocess.check_output(SWEEP, shell=True)
    lines = results.split("\n")
    
    for line in lines:
        line = line.strip()
        line = line.rstrip()
        while "  " in line: 
            line = line.replace("  ", " ");

        if ("<server>" in line) or ("<unknown>" in line):
            ip_address = line.split(" ")[0]
            host = line.split(" ")[1]
        
            if (hostnames > 0):
                f.write('\n')

            print("   [>] Discovered hostname: %s (%s)" % (host, ip_address))
            f.write("%s - %s" % (host, ip_address))
            hostnames += 1

    print("[*] Found %s hostnames." % (hostnames))
    print("[*] Created hostname list %s" % (output_file))
    f.close()