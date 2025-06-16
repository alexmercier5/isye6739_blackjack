import math
import random
import pandas as pd
import csv
import os


def setup(bankroll=100, deck=None):
    if deck is None:
        print("Setting up the game with a new deck of cards...\n")
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        values = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'Jack': 10,
            'Queen': 10,
            'King': 10,
            'Ace': 11
        }

        deck = []
        for i in range(6):  # 6 decks
            for suit in suits:
                for rank in ranks:
                    deck.append((rank, suit, values[rank]))

        print(f"Deck size: {len(deck)}\n\n")
        # print("Deck of cards:")
        # for card in deck:
        #     print(f"{card[0]} of {card[1]} (Value: {card[2]})")
    else:
        print("Using the existing deck of cards...\n")
        print(f"Deck size: {len(deck)}\n\n")

    return deck, bankroll


def shuffle_deck(deck):
    """Shuffle the deck of cards."""
    random.shuffle(deck)
    return deck

def dealer_hand(hand, deck, ifBusted=False):
    """Deal a hand of cards to the dealer."""
    if hand is None:
        hand = []
        card = deck.pop()
        hand.append(card)
        if sum(card[2] for card in hand) > 21:
            for each_card in hand:
                if each_card[0] == 'Ace':
                    hand.remove(each_card)
                    hand.append(('Ace', each_card[1], 1))
                    break
        # for i, each_card in enumerate(deck):
        #     if each_card[0] == card[0] and each_card[1] == card[1]:
        #         del deck[i]
        #         break
        print(f"Dealer dealt: xxx of xxx (Hidden)")
    else:
        if len(hand) == 1:
            card = deck.pop()
            hand.append(card)
            print(f"Dealer dealt: {card[0]} of {card[1]}")
            # for i, each_card in enumerate(deck):
            #     if each_card[0] == card[0] and each_card[1] == card[1]:
            #         del deck[i]
            #         break
        else:
            if ifBusted:
                pass
            else:
                for card in hand:
                    print(f"Dealer's hand: {card[0]} of {card[1]}")
                while sum(dcard[2] for dcard in hand) <= 16:
                    card = deck.pop()
                    hand.append(card)
                    print(f"Dealer hits and is dealt: {card[0]} of {card[1]}")
                    if sum(card[2] for card in hand) > 21:
                        for each_card in hand:
                            if each_card[0] == 'Ace':
                                hand.remove(each_card)
                                hand.append(('Ace', each_card[1], 1))
                                break
                    # for i, each_card in enumerate(deck):
                    #     if each_card[0] == card[0] and each_card[1] == card[1]:
                    #         del deck[i]
                    #         break
            print("Dealer stands.")
    return hand, deck

def player_hand(deck, bankroll, strategy):
    """Deal a hand of cards to the player."""
    balance=bankroll
    print(f"Player's current balance: ${balance}\n")
    if strategy in ['strat1', 'strat2', 'strat3']:
        print(f"Using strategy: {strategy}\n")
        bet = 10
        #bet = math.fabs(bankroll // 10)
    else:
        print(f"Enter your bet amount: ")
        bet = input()
    bet2 = 0
    try:
        bet = int(bet)
        if bet > balance:
            print(f"Insufficient balance. Your current balance is ${balance}.")
            return
    except ValueError:
        print("Invalid bet amount. Please enter a valid number.")
        return
    balance -= bet
    print(f"Player's bet: ${bet}\n")
    hand = []
    split_hand = []
    num_of_hands = 1
    if len(hand) == 0:
        card = deck.pop()
        hand.append(card)
        print(f"Player dealt: {card[0]} of {card[1]}")
        # for i, each_card in enumerate(deck):
        #             if each_card[0] == card[0] and each_card[1] == card[1]:
        #                 del deck[i]
        #                 break
        dealer_hand_1card, deck = dealer_hand(None, deck)
    if len(hand) == 1:
        card = deck.pop()
        hand.append(card)
        print(f"Player dealt: {card[0]} of {card[1]}")
        # for i, each_card in enumerate(deck):
        #     if each_card[0] == card[0] and each_card[1] == card[1]:
        #         del deck[i]
        #         break
        dealer_hand_2card, deck = dealer_hand(dealer_hand_1card, deck)
    mainPlaying = True
    splitPlaying = False
    playerPlaying = True
    turn = 0
    busted = False
    while playerPlaying:
        for indiv_hand in range(num_of_hands):
            if indiv_hand == 0:
                current_hand = "Main Hand"
                if not mainPlaying:
                    continue
                total_value = sum(card[2] for card in hand)
            elif indiv_hand == 1:
                current_hand = "Split Hand"
                if not splitPlaying:
                    continue
                total_value = sum(card[2] for card in split_hand)
            if strategy not in ['strat1', 'strat2', 'strat3']:
                print(f"\n\n{current_hand} --- Total: {total_value} \nHit or Stand? Type 'h' or enter to hit or type 's' to stand.\n")
                if turn == 0:
                    print(f"Type 'double' or 'd' to double down.\n")
                if card[2] == hand[0][2] and turn == 0:
                    print("\n\nPlayer has a pair! Type 'split' to split, else game continues\n")
                input_choice = input()
            elif strategy == "strat1":
                #Strats: https://www.888casino.com/blog/blackjack-strategy/best-blackjack-strategies
                #Strategy for always double down on a hard 11
                isAce = any(card[0] == 'Ace' for card in hand)
                isAceDealer = any(card[0] == 'Ace' for card in dealer_hand_2card)

                if turn == 0:
                    if total_value == 11 and not isAce:
                        input_choice = 'double'
                        if balance >= bet:
                            balance -= bet
                            bet *= 2
                            card = deck.pop()
                            hand.append(card)
                            print(f"Player doubled down and is dealt: {card[0]} of {card[1]}")
                            playerPlaying = False
                            return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted
                    elif total_value == 17 and isAce and isAceDealer:
                        input_choice = 'h'
                        card = deck.pop()
                        hand.append(card)
                        print(f"Player hits and is dealt: {card[0]} of {card[1]}")
                        if sum(card[2] for card in hand) > 21:
                            for each_card in hand:
                                if each_card[0] == 'Ace':
                                    hand.remove(each_card)
                                    hand.append(('Ace', each_card[1], 1))
                                    break
                        return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

                if total_value > 21:
                    busted = True
                    print("Player busts!")
                else:
                    for card in hand:
                        print(f"Player's hand: {card[0]} of {card[1]}")
                    while sum(dcard[2] for dcard in hand) <= 16:
                        card = deck.pop()
                        hand.append(card)
                        print(f"Player hits and is dealt: {card[0]} of {card[1]}")
                        if sum(card[2] for card in hand) > 21:
                            for each_card in hand:
                                if each_card[0] == 'Ace':
                                    hand.remove(each_card)
                                    hand.append(('Ace', each_card[1], 1))
                                    break

                return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

            elif strategy == "strat2":
                #strategy for always split a pair of 8s and aces
                isAce = any(card[0] == 'Ace' for card in hand)

                if turn == 0:
                    if total_value == 16 and not isAce:
                        input_choice = 'split'
                        balance -= bet
                        bet2 = bet
                        print(f"Player splits the hand. New bet is ${bet} and ${bet2}.")
                        splitPlaying = True
                        num_of_hands += 1
                        split_hand.append(card)
                        hand.remove(card)
                        return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted
                    elif total_value == 18 and isAce:
                        input_choice = 'split'
                        balance -= bet
                        bet2 = bet
                        print(f"Player splits the hand. New bet is ${bet} and ${bet2}.")
                        splitPlaying = True
                        num_of_hands += 1
                        split_hand.append(card)
                        hand.remove(card)
                        return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

                if total_value > 21:
                    print("Player busts!")
                    busted = True
                else:
                    for card in hand:
                        print(f"Player's hand: {card[0]} of {card[1]}")
                    while sum(dcard[2] for dcard in hand) <= 16:
                        card = deck.pop()
                        hand.append(card)
                        print(f"Player hits and is dealt: {card[0]} of {card[1]}")
                        if sum(card[2] for card in hand) > 21:
                            for each_card in hand:
                                if each_card[0] == 'Ace':
                                    hand.remove(each_card)
                                    hand.append(('Ace', each_card[1], 1))
                                    break

                return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

            elif strategy == "strat3":
                # Strategy for never splitting a pair of 5s or tens
                isAce = any(card[0] == 'Ace' for card in hand)

                if turn == 0:
                    if total_value == 10 and not isAce:
                        input_choice = 'h'
                        card = deck.pop()
                        hand.append(card)
                        print(f"Player hits and is dealt: {card[0]} of {card[1]}")
                        if sum(card[2] for card in hand) > 21:
                            for each_card in hand:
                                if each_card[0] == 'Ace':
                                    hand.remove(each_card)
                                    hand.append(('Ace', each_card[1], 1))
                                    break
                        return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

                    elif total_value == 20 and not isAce:
                        input_choice = 's'
                        # No action needed (player stands)
                        return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

                # Now handle the "big else" for all other cases
                if total_value > 21:
                    busted = True
                    print("Player busts!")
                else:
                    for card in hand:
                        print(f"Player's hand: {card[0]} of {card[1]}")
                    while sum(card[2] for card in hand) <= 16:
                        card = deck.pop()
                        hand.append(card)
                        print(f"Player hits and is dealt: {card[0]} of {card[1]}")
                        if sum(card[2] for card in hand) > 21:
                            for each_card in hand:
                                if each_card[0] == 'Ace':
                                    hand.remove(each_card)
                                    hand.append(('Ace', each_card[1], 1))
                                    break

                return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

            if input_choice.lower() == 'h' or input_choice == '':
                print(f"Player hits.\n")
                card = deck.pop()
                if indiv_hand == 0:
                    hand.append(card)
                elif indiv_hand == 1:
                    split_hand.append(card)
                print(f"\nPlayer dealt: {card[0]} of {card[1]}")
            elif input_choice.lower() == 'split':
                balance -= bet
                bet2 = bet
                print(f"Player splits the hand. New bet is ${bet} and ${bet2}.")
                splitPlaying = True
                num_of_hands += 1
                split_hand.append(card)
                hand.remove(card)
            elif input_choice.lower() == 'double' or input_choice.lower() == 'd':
                if balance >= bet:
                    balance -= bet
                    bet *= 2
                    card = deck.pop()
                    hand.append(card)
                    print(f"Player doubled down and is dealt: {card[0]} of {card[1]}")
                    playerPlaying = False
                else:
                    print("Insufficient balance to double down.")
            else:
                if indiv_hand == 0:
                    mainPlaying = False
                elif indiv_hand == 1:
                    splitPlaying = False
                print(f"{current_hand}: Player stands.")
            if indiv_hand == 0:
                total_value = sum(maincard[2] for maincard in hand)
                if total_value > 21:
                    for each_card in hand:
                            if each_card[0] == 'Ace' and each_card[2] == 11:
                                hand.remove(each_card)
                                hand.append(('Ace', each_card[1], 1))
                                total_value = sum(card[2] for card in hand)
                                if total_value <= 21:
                                    break
                    else:
                        print(f"{current_hand}: Player busts!")
                        busted = True
                        mainPlaying = False
                elif total_value == 21:
                    print(f"{current_hand}: Player has blackjack!")
                    mainPlaying = False
                else:
                    print(f"{current_hand} --- Total: {total_value}")

                # for i, each_card in enumerate(deck):
                #     if each_card[0] == card[0] and each_card[1] == card[1]:
                #         del deck[i]
                #         break

            if indiv_hand == 1:
                total_value = sum(splitcard[2] for splitcard in split_hand)
                if total_value > 21:
                    for each_card in hand:
                            if each_card[0] == 'Ace' and each_card[2] == 11:
                                hand.remove(each_card)
                                hand.append(('Ace', each_card[1], 1))
                                total_value = sum(card[2] for card in split_hand)
                                if total_value <= 21:
                                    break
                    else:
                        print("{current_hand}: Player busts!")
                        splitPlaying = False
                elif total_value == 21:
                    print("{current_hand}: Player has blackjack!")
                    splitPlaying = False
                else:
                    print(f"{current_hand}: Player's total value: {total_value}")

                # for i, each_card in enumerate(deck):
                #     if each_card[0] == card[0] and each_card[1] == card[1]:
                #         del deck[i]
                #         break
        if not mainPlaying and not splitPlaying:
            playerPlaying = False
        turn += 1
    if len(split_hand) == 0:
        split_hand = None
    return hand, split_hand, deck, dealer_hand_2card, bet, bet2, balance, busted

def compare_hands(dealer_hand, player_hand, split_hand, bet, bet2, balance):
    profit = 0
    dealer_total = sum(card[2] for card in dealer_hand)
    player_total = sum(card[2] for card in player_hand)

    print("\nDealer's final hand:")
    for card in dealer_hand:
        print(f"{card[0]} of {card[1]}")
    print(f"Dealer's total value: {dealer_total}")
    print("\nPlayer's final hand:")
    for card in player_hand:
        print(f"{card[0]} of {card[1]}")
    print(f"Player's total value: {player_total}\n")
    if dealer_total > 21 and player_total <= 21:
        print("Player wins!\n")
        profit = bet * 2
        balance += profit
    elif player_total > 21 and dealer_total > 21:
        print("It's a tie!\n")
        profit = 0
        balance += bet
    elif player_total > 21:
        print("Dealer wins!\n")
        profit = -bet
        balance += profit
    elif dealer_total > player_total:
        print("Dealer wins!\n")
        profit = -bet
        balance += profit
    elif player_total > dealer_total:
        print("Player wins!\n")
        profit = bet * 2
        balance += profit
    else:
        print("It's a tie!\n")
        profit = 0
        balance += bet
    print(f"Player's balance after this round: ${balance}\n")

    if split_hand:
        split_total = sum(card[2] for card in split_hand)
        print("\nPlayer's split final hand:")
        for card in split_hand:
            print(f"{card[0]} of {card[1]}")
        print(f"Player's split hand total value: {split_total}")
        if dealer_total > 21 and split_total <= 21:
            print("Player's split hand wins!\n\n")
            profit += bet2 * 2
            balance += bet2 * 2
        elif split_total > 21 and dealer_total > 21:
            print("It's a tie!\n")
            profit = 0
            balance += bet
        elif split_total > 21:
            print("Dealer beats split hand!\n\n")
            profit -= bet2
            balance -= bet2
        elif dealer_total > split_total:
            print("Dealer beats split hand!\n\n")
            profit -= bet2
            balance -= bet2
        elif split_total > dealer_total:
            print("Player's split hand wins!\n\n")
            profit += bet2 * 2
            balance += bet2 * 2
        else:
            print("Split hand ties dealer!\n\n")
            profit += bet2
            balance += bet2
    revenue = profit - (bet + bet2)
    return profit, balance, revenue

def choose_strategy(deck):

    return "standard"

def save_results(dealers_hand, players_hand, split_hand, strategy, profit, balance, revenue, runs):
    dealer_total = sum(card[2] for card in dealers_hand)
    player_total = sum(card[2] for card in players_hand)
    if split_hand:
        split_total = sum(card[2] for card in split_hand)
        split_hand = ', '.join([f"{card[0]} of {card[1]}" for card in split_hand])
        
    else:
        split_total = None
    dealers_hand_str = ', '.join([f"{card[0]} of {card[1]}" for card in dealers_hand])
    players_hand_str = ', '.join([f"{card[0]} of {card[1]}" for card in players_hand])

    result_row = {
        'Dealer Hand': dealers_hand_str,
        'Dealer Hand Value': dealer_total,
        'Player Hand': players_hand_str,
        'Player Hand Value': player_total,
        'Split Hand': split_hand,
        'Split Hand Value': split_total,
        'Profit': profit,
        'Balance': balance,
        'Revenue': revenue,
        'Strategy': strategy
    }
    result_df = pd.DataFrame([result_row])
    file_exists = os.path.isfile(f"results_{strategy}.csv")
    result_df.to_csv(f"total_results_{strategy}_{runs}runs.csv", mode='a', index=False, header=not file_exists)

    return None

if __name__ == "__main__":
    strategy = input("Choose a strategy (strat1, strat2, strat3) or enter to play yourself: ").strip().lower()
    if strategy in ['strat1', 'strat2', 'strat3']:
        runs = int(input("Enter the number of runs for the strategy: "))
        run = 0
    else: 
        runs = 1
    balance = int(input("Enter your starting bankroll: "))
    deck = None
    if strategy not in ['strat1', 'strat2', 'strat3']:
        while True:
            deck, balance = setup(bankroll=balance, deck=deck)
            shuffled_deck = shuffle_deck(deck)
            players_hand, split_hand, current_deck, dealer_hands, bet, bet2, balance, ifBusted = player_hand(shuffled_deck, balance, None)
            dealers_hand, final_deck = dealer_hand(dealer_hands, current_deck, ifBusted)
            profit, balance, revenue = compare_hands(dealers_hand, players_hand, split_hand, bet, bet2, balance)
            save_results(dealers_hand, players_hand, split_hand, 'user', profit, balance, revenue, runs)
            if balance <= 0:
                print("You have run out of money! Game over.")
                break

    else:
        balance_init = balance
        deck = None
        for i in range(50):
            print(f"SIMULATION: \n\n\n\n\n{i}\n\n\n\n")
            run = 0
            balance = balance_init
            while run < runs:
                try:
                    strategy = strategy
                    run += 1
                    deck, balance = setup(bankroll=balance, deck=deck)
                    shuffled_deck = shuffle_deck(deck)
                    #strat = choose_strategy(strategy)
                    players_hand, split_hand, current_deck, dealer_hands, bet, bet2, balance, ifBusted = player_hand(shuffled_deck, balance, strategy)
                    dealers_hand, final_deck = dealer_hand(dealer_hands, current_deck, ifBusted)
                    profit, balance, revenue = compare_hands(dealers_hand, players_hand, split_hand, bet, bet2, balance)
                    save_results(dealers_hand, players_hand, split_hand, strategy, profit, balance, revenue, runs)
                    if balance <= 0:
                        print("You have run out of money! Game over.")
                        break
                    if len(deck) < 52:
                        print("Deck is running low, reshuffling...")
                        deck = None
                except Exception as e:
                    print(f"Error during simulation {i}, run {run}: {e}")
                    break  # exit current 'while run < runs', go to next i
