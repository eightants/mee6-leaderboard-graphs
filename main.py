# main.py
# A program and scrapes the mee6 leaderboard site api and generates graphs

import matplotlib.pyplot as plt
from ServerInfo import ServerInfo

# --------
# config.ini file reader
# --------
with open('config.ini', 'r') as configfile: 
    configs = configfile.readlines()
    # checks that config file has 6 lines
    if not len(configs) == 6: 
        print("Invalid config file: incorrect number of lines!")
    else: 
        try: 
            # completes json link with server id
            url = 'https://mee6.xyz/api/plugins/levels/leaderboard/' + str(configs[0]) + '?limit=999&page=0'
            # checks for 'na' and sets default
            if not configs[1] == "na":
                top = int(configs[1])
            else: 
                top = 100
            # converts str to int before being used in functions
            statuslevels = list(configs[2].strip(" ").split(","))
            for i in range(len(statuslevels)): 
                statuslevels[i] = int(statuslevels[i])
            # setting statusnames
            statusnames = list(configs[3].strip("\n").strip(" ").split(","))
            yvar = configs[4]
            # output csv?
            printcsv = configs[5]
            csv = False
            if printcsv == 'y': 
                csv = True
        except: 
            print("An error ocurred, please recheck config.ini")

# sets server variable
server = ServerInfo(url, top)
# csv
if csv: 
    server.csv()
# plots figure
plt.figure()
plt.suptitle(server.servername)
plt.subplot(221)
server.statuspie(statuslevels, statusnames)
plt.subplot(222)
server.rankbar(yvar)
plt.subplot(223)
server.lvldistribution()
plt.subplot(224)
server.randomstats()
plt.subplots_adjust(hspace=0.3)
plt.show()



