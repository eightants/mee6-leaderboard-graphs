# ServerInfo.py
# Attempt 1 using the json link to get the API
# Object contains info of up to top 1000 members in server
# Contains methods for csv and data visualization

import requests
import csv
import matplotlib.pyplot as plt
import numpy as np

class ServerInfo:

    def __init__(self, URL, top=100): 
        res = requests.get(URL)
        # res.json() is now the entire webpage API as a dictionary
        print("Communicating with the Mee6 servers...")
        self.servername = res.json()["guild"]["name"]
        print("server name: " + str(self.servername))
        # catches errors associated with inputs for top n members
        maxtop = False
        if top < 3: 
            top = 3
            print("top: cannot be less than 3, changed to 3")
        elif top > 1000: 
            top = 1000
            print("top: cannot be greater than 1000, changed to 1000")
        # special case to handle if top == 1000
        if top == 1000: 
            maxtop = True
            top = 999
        # the members information is contained in a list of 100(default) dictionaries, one dictionary per member
        username, discordtag, exp, level, messages = [], [], [], [], []
        print("number of members in server:", len(res.json()["players"]))
        # makes sure the server has enough members to graph the top 100/1000 of, else, cap it at an amount
        if top > len(res.json()["players"]):
            top = len(res.json()["players"])
            print("top: cannot be greater than number of members in server, changed to", len(res.json()["players"]))
        for user in res.json()['players'][0:top]:
            username.append(user['username'])
            discordtag.append("#" + str(user['discriminator']))
            exp.append(user['xp'])
            level.append(user['level'])
            messages.append(user['message_count'])
        # Somehow the json link only contains the top 999 entries
        # To make graph titles nicer to read, this makes it 1000 by duplicating the last element
        if maxtop: 
            self.username, self.discordtag, self.exp, self.level, self.messages = username + [username[-1]], discordtag + [discordtag[-1]], exp + [exp[-1]], level + [level[-1]], messages + [messages[-1]]
            top = 1000
        else: 
            self.username, self.discordtag, self.exp, self.level, self.messages = username, discordtag, exp, level, messages
        self.top = top
        print("number of members to graph: " + str(top))
        print("----------")
    
    def csv(self): 
        '''
        Writes csv of top n members 
        '''
        with open("mee6-leaderboard.csv", "w", newline="", encoding = "utf-8") as outfile: 
            fileWriter = csv.writer(outfile)
            header = ["username", "discord tag", "exp", "level", "messages sent"]
            fileWriter.writerow(header)
            for i in range(len(self.username)): 
                fileWriter.writerow([self.username[i], self.discordtag[i], self.exp[i], self.level[i], self.messages[i]])
            print("mee6-leaderboard.csv created")

    def statuspie(self, statuslevels=[10, 20, 30, 40, 50], statusnames=""): 
        """
        Pie chart showing the percentage of members in each level range
        ---
        statuslevels: list of int specifying the cutoffs for each range. eg [10, 20, 30, 40, 50]
        statusnames: list of str specifying custom name for each range, leave blank to autogenerate
        """
        # checks if user wanted defaults
        if statuslevels == "na": 
            statuslevels = [10, 20, 30, 40, 50]
        # checks if input level cutoffs start at 0, if not add 0 to start of list
        if not int(statuslevels[0]) == 0: 
            statuslevels = [0] + statuslevels
        if statusnames: 
            if statuslevels[0] == 0 and (len(statusnames) + 1) == len(statuslevels): 
                statusnames = ["below " + statusnames[0]] + statusnames
            else: 
                statusnames = ""
        # creates array to tally number of members in each rank status
        tally = np.zeros(len(statuslevels), dtype=int)
        # tallies up number of members in each level category
        #print(self.level)
        for i in range(len(self.level)): 
            userlevel = self.level[i]
            for n in reversed(range(len(statuslevels))):
                if userlevel >= statuslevels[n]:
                    tally[n] += 1
                    break
        # generates default category names if not specified
        if statusnames and not statusnames == "na": 
            labels = statusnames
        else: 
            labels = []
            for i in range(1, len(statuslevels)):
                labels.append("lvl" + str(statuslevels[i - 1]) + " to lvl" + str(statuslevels[i]))
            labels.append("above lvl" + str(statuslevels[-1]))
        # prints inputs to terminal
        print("level cutoffs: " + str(statuslevels))
        print("level range names: " + str(labels))
        # generates pie chart
        self.tally = tally
        self.statusnames = labels
        sizes = self.tally
        plt.pie(sizes)
        plt.legend(labels, loc=1)
        plt.title("Breakdown of Top " + str(self.top) + " Members")
        plt.axis("equal")
    
    def rankbar(self, yvar="lvl"): 
        """
        yvar: str, determines the dependent variable. 'lvl' for levels, 'exp' for experience points
        """
        # leaderboard visualized
        if yvar == "exp": 
            bars = self.exp[0:self.top]
            yvarname = "Experience"
            print("yvar: exp")
        else: 
            bars = self.level[0:self.top]
            yvarname = "Level"
            print("yvar: lvl")
        labels = list(range(1, self.top + 1))
        plt.bar(labels, bars)
        plt.title("Leaderboard")
        plt.xlabel('Rank')
        plt.ylabel(yvarname)
        plt.grid()

    def lvldistribution(self): 
        """
        Plots frequency of each level in a histogram
        """
        levels = self.level[0:self.top]
        # determines number of bars needed, one for each level
        bins = levels[0] - levels[-1]
        plt.hist(levels, bins=bins, align="right")
        plt.title("Level Distribution of Top " + str(self.top) + " Members")
        plt.ylabel("Frequency")
        plt.xlabel("Level")
        plt.grid()
    
    def randomstats(self): 
        """
        analysis statements about the data collected
        """
        textlist = []
        # statements about pie chart data
        piestats = []
        for n in range(len(self.tally)): 
            percent = (self.tally[n] / self.top) * 100
            piestats.append(str(round(percent, 2)) + "% are " + str(self.statusnames[n]))
        # statement about first place
        leader = str(self.username[0]) + " is first place at level " + str(self.level[0]) + " and " + str(self.exp[0]) + " XP"
        # central tendencies of data
        levels = self.level[0:self.top]
        mode = "The modal level is " + str(max(set(levels), key=(levels).count))
        median = "The median level is " + str(self.level[(self.top + 1) // 2])
        sumlevels = sum(levels)
        avglevel = sumlevels / self.top
        aboveavg = 0
        for level in levels: 
            if level > avglevel: 
                aboveavg += 1
        mean = "The mean level is " + str(avglevel)
        percentabove = str(round(aboveavg * 100 / self.top, 2)) + "% of the top " + str(self.top) + " is above the mean level"
        # gathers all text into a list
        textlist = piestats + [leader, mode, median, mean, percentabove]
        # formats the text with line breaks and plots it
        textdata = ""
        for text in textlist: 
            textdata += text + "\n"
        plt.text(0, 0, textdata)
        plt.title("For the Top " + str(self.top) + " Members")
        plt.axis("off")






