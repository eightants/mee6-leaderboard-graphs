# Mee6 Leaderboard Graphs
Here you go! Spent a couple days working on this little project. I always thought that the Mee6 leaderboard site has great data for some demographic charts, especially its use in popular servers. This should work with all Discord servers that use the Mee6 bot. Let me know if there are any bugs. 

## What it does
This program creates graphs to visualize up to the top 1000 members of your Discord server. The graphs include a pie chart showing a breakdown of level ranges of members, a leaderboard the top members and their levels/experience represented in a bar graph, a histogram showing the frequency distribution of levels in the sample, and a few more general analytics statements. 

## How to use

### Getting started
To use this program, you will need a couple things: 
- Python 3
- Make sure that the server you want to graph has the Mee6 bot
- Your Mee6 Server ID (more on this below)

Getting your Mee6 Server ID: 
1. Go on the server you want to use and type `!levels` in the chat
2. Visit the link that Mee6 replies with, it should look like this: https://mee6.xyz/leaderboard/123456789123456789 or https://mee6.xyz/levels/123456789123456789
3. The server ID is the numbers at the end of the url, in this case "123456789123456789"

### Configurations
The config.ini file you will need to edit to run the program with the server and settings you want. Here's how to use it. To use the default settings (if available) in each line, write `na`

Each line of config.ini explained: 
1. Mee6 Server ID: the number from the Mee6 leaderboard url (see above). REQUIRED FIELD
2. Number of members (3 - 1000): How many server top members the program should take into account, sample size. Default is `100`
3. Level cutoffs for pie chart: You decide the level ranges for the pie chart slices, separate with commas. Default is `10,20,30,40,50`
4. Names for each level range: For the pie chart legend. Useful if your server has roles when members reach certain levels and you want to show them (eg "Bronze, Silver, Gold"). Write `na` to auto generate descriptions for the legend
5. Dependent var for leaderboard: Plot the leaderboard bar graph with level or xp on the y-axis. `lvl` for levels, `exp` for xp. Default is `lvl`

Example of a valid config.ini file: 
```
123456789123456789
500
5,10,20,30,50
na
exp
```

### Running the program
After filling in the config file, save all your changes. Run main.py with Python 3 to use the program
