Work on this project was done by Alex Mercier and Katie Bush. 

Within this project there are a few important files. First, the main.py file is the simulation. It is broken into functions which are designed to construct player and dealer moves. Additionally, there are functions utilized to compare the hands of the player/dealer as well as save the results of the game. These results are saved to separate files and can be named within the save_results() function. The three .csv's 'total_results_stratX_50cases_10000runs.csv' where X=1, 2, 3 are the total simulation results for each strategy respectively. There are 50 cases of 10,000 games that were ran until bankroll was $0 for each strategy. Additionally, the bets were standardized at $10 with an initial bankroll of $10,000. The 9 individual .csv's consist of the 3 cases for each strategy utilized in the construction of the report.

The use of AI (ChatGPT) for certain syntax and specific debugging was used to help improve the code performance. All ideas and construction of the code itself were that of the above authors. Additionally links to websites used in creation of documented blackjack strategies are included within the code where applicable. 

Set up the project using the following steps.

Copy this link:
```
https://github.com/alexmercier5/isye6739_blackjack.git 
```
Navigate to where you want your project in desired terminal, example:
```
cd Documents/School/Project
```
Clone the repository:
```
git clone https://github.com/alexmercier5/isye6739_blackjack.git
```
Make a virtual environment:
```
py -m venv .env
```
Activate your virtual environment depending on OS

Windows:
```
.env/scripts/activate
```
Mac OS: 
```
source .env/bin/activate
```
Install the necessary packages:
```
pip install -r requirements.txt
```
Run the script:
```
py -m main
```
Evaluate outputs by navigating to results.csv. 
