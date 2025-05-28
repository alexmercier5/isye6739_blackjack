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
Activate your virtual environment:
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

TODO: Develop a method to implement specific strategies, also allow for running DoE's based on the strategies so user does not have to play each game. 