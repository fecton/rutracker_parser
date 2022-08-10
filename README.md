# Native Linux Games Parser from RuTracker
This parser parse all native linux games and make a quick search by your query. You do not to register at RuTracker or anything, just run it

## How to Run

1. Clone the repository
2. Enter the directory
3. Create a virtual enviroment
4. Activate it
5. Install necessary modules 
7. Run the python file 'main.py'
```
git clone https://github.com/fecton/rutracker_parser
cd rutracker_parser
python3 -m venv venv/
source venv/bin/activate
pip3 install -r requirements.txt
./main.py -d "your_game" --help
```

## Functionality

### Help message
![image](https://user-images.githubusercontent.com/76391547/183996644-0c028624-c8bb-4152-8da0-4eb87701ba22.png)

### Searching by game's name (phrase)
![image](https://user-images.githubusercontent.com/76391547/183997202-33864f26-0350-43e9-9a99-cbb3b173ce69.png)

### Searching by each word
![image](https://user-images.githubusercontent.com/76391547/183997923-1a5b4392-c5f0-41fe-a424-396bd78ae39f.png)

### Show detailt during searching
![image](https://user-images.githubusercontent.com/76391547/183998227-37451954-fe65-44e0-96e5-e1a90d3315a6.png)

### Finish after a first march
It stops after 4 matches because it uses 4 threads
![image](https://user-images.githubusercontent.com/76391547/183999230-639b3ce7-c110-42b6-b963-ece152a80d2c.png)

### Ingore cached pages
If you want to update your caches pages, use this parameter (it will be slower)
![image](https://user-images.githubusercontent.com/76391547/184000679-2e2b0fc7-d886-48a8-81a5-a613175242cd.png)

