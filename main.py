import math
import random
import pandas as pd
import csv
import os


#TODO: ADD BETTING SYSTEMS
'''
Even Money Wins:
If you beat the dealer's hand (having a higher value without exceeding 21), you win your original bet back plus the amount you won. 
Doubling Down:
If you choose to double down (place an additional bet after your first two cards) and win, the payout is still even money, but you're doubling your potential winnings. 
Blackjack Payout:
Traditionally, a Blackjack (Ace and a face card as your initial two cards) pays 3:2. This means if you bet $100, you win $150 (plus the $100 back). 
Blackjack Payout Variation:
Some casinos offer 6:5 payouts for Blackjack, meaning you win $12 for a $10 bet. 
Insurance:
If the dealer's face-up card is an Ace, you can bet on whether they have Blackjack. This bet pays 2:1 if the dealer does have Blackjack but loses otherwise, according to the Venetian Las Vegas. 
Push:
If you and the dealer have the same hand value, it's a push (tie), and your bet is returned to you. 
'''

def setup(bankroll=100):
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

    return deck, bankroll


def shuffle_deck(deck):
    """Shuffle the deck of cards."""
    random.shuffle(deck)
    return deck

def dealer_hand(hand, deck):
    """Deal a hand of cards to the dealer."""
    if hand is None:
        hand = []
        for dealer_card in range(2):
            card = deck.pop()
            hand.append(card)
            if sum(card[2] for card in hand) > 21:
                for each_card in hand:
                    if each_card[0] == 'Ace':
                        hand.remove(each_card)
                        hand.append(('Ace', each_card[1], 1))
                        break
            for i, each_card in enumerate(deck):
                if each_card[0] == card[0] and each_card[1] == card[1]:
                    del deck[i]
                    break
            if dealer_card == 0:
                print(f"Dealer dealt: xxx of xxx (Hidden)")
            else:
                print(f"Dealer dealt: {card[0]} of {card[1]}\n\n")
    else:
        print("\n\n")
        for card in hand:
            print(f"Dealer's hand: {card[0]} of {card[1]}")
        while sum(card[2] for card in hand) <= 16:
            card = deck.pop()
            hand.append(card)
            print(f"Dealer hits and is dealt: {card[0]} of {card[1]}")
            if sum(card[2] for card in hand) > 21:
                for each_card in hand:
                    if each_card[0] == 'Ace':
                        hand.remove(each_card)
                        hand.append(('Ace', each_card[1], 1))
                        break
        else:
            print("Dealer stands.")
    return hand, deck

def player_hand(deck, bankroll):
    """Deal a hand of cards to the player."""
    balance=bankroll
    print(f"Player's current balance: ${balance}\n")
    print(f"Enter your bet amount (or type 'exit' to quit): ")
    bet = input()
    if bet.lower() == 'exit':
        print("Exiting the game.")
        exit()
    try:
        bet = int(bet)
        if bet > balance:
            print(f"Insufficient balance. Your current balance is ${balance}.")
            return player_hand(deck, balance)
    except ValueError:
        print("Invalid bet amount. Please enter a valid number.")
        return player_hand(deck, balance)
    
    #TODO: 
    '''
    Make sure that a card is removed from the deck after being delt on line 126, 
    also need to deal in the order: player, dealer, player, dealer where 4 cards are delt before hit/stand is asked
    '''
    hand = []
    split_hand = []
    split_card_num = 0
    num_of_hands = 1
    card = deck.pop()
    hand.append(card)
    print(f"Player dealt: {card[0]} of {card[1]}")
    #dealer_hand(None, deck)
    mainPlaying = True
    splitPlaying = False
    playerPlaying = True
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
            print(f"\n\n{current_hand} --- Total: {total_value} \nHit or Stand? Type 'h' or enter to hit or type 's' to stand.\n")
            input_choice = input()
            if input_choice.lower() == 'h' or input_choice == '':
                card = deck.pop()
                card=card
                if indiv_hand == 0:
                    hand.append(card)
                elif indiv_hand == 1:
                    split_hand.append(card)
                print(f"\nPlayer dealt: {card[0]} of {card[1]}")
                split_card_num += 1
                if card[0] == hand[0][0] and split_card_num == 1:
                    print("\n\nPlayer has a pair! Type 'split' to split, else game continues\n\n")
                    split_choice = input()
                    if split_choice.lower() == 'split':
                        splitPlaying = True
                        num_of_hands += 1
                        split_hand.append(card)
                        hand.remove(card)
                if sum(card[2] for card in hand) > 21:
                    for each_card in hand:
                        if each_card[0] == 'Ace':
                            hand.remove(each_card)
                            hand.append(('Ace', each_card[1], 1))
                            break
            else:
                if indiv_hand == 0:
                    mainPlaying = False
                elif indiv_hand == 1:
                    splitPlaying = False
                print(f"{current_hand}: Player stands.")
            if indiv_hand == 0:
                total_value = sum(card[2] for card in hand)
                if total_value > 21:
                    print(f"{current_hand}: Player busts!")
                    mainPlaying = False
                elif total_value == 21:
                    print(f"{current_hand}: Player has blackjack!")
                    mainPlaying = False
                else:
                    print(f"{current_hand} --- Total: {total_value}")

                for i, each_card in enumerate(deck):
                    if each_card[0] == card[0] and each_card[1] == card[1]:
                        del deck[i]
                        break

            if indiv_hand == 1:
                total_value = sum(card[2] for card in split_hand)
                if total_value > 21:
                    print("{current_hand}: Player busts!")
                    splitPlaying = False
                elif total_value == 21:
                    print("{current_hand}: Player has blackjack!")
                    splitPlaying = False
                else:
                    print(f"{current_hand}: Player's total value: {total_value}")

                for i, each_card in enumerate(deck):
                    if each_card[0] == card[0] and each_card[1] == card[1]:
                        del deck[i]
                        break
        if not mainPlaying and not splitPlaying:
            playerPlaying = False
    if len(split_hand) == 0:
        split_hand = None
    return hand, split_hand, deck

def compare_hands(dealer_hand, player_hand, split_hand):
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
    elif player_total > 21:
        print("Dealer wins!\n")
    elif dealer_total > player_total:
        print("Dealer wins!\n")
    elif player_total > dealer_total:
        print("Player wins!\n")
    else:
        print("It's a tie!\n")

    if split_hand:
        split_total = sum(card[2] for card in split_hand)
        print("\nPlayer's split final hand:")
        for card in split_hand:
            print(f"{card[0]} of {card[1]}")
        print(f"Player's split hand total value: {split_total}")
        if dealer_total > 21 and split_total <= 21:
            print("Player's split hand wins!\n\n")
        elif split_total > 21:
            print("Dealer beats split hand!\n\n")
        elif dealer_total > split_total:
            print("Dealer beats split hand!\n\n")
        elif split_total > dealer_total:
            print("Player's split hand wins!\n\n")
        else:
            print("Split hand ties dealer!\n\n")

def choose_strategy(deck):
    return "standard"

def save_results(dealers_hand, players_hand, split_hand, strategy):
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
        'Strategy': strategy
    }
    result_df = pd.DataFrame([result_row])
    file_exists = os.path.isfile("results.csv")
    result_df.to_csv("results.csv", mode='a', index=False, header=not file_exists)

    return None

if __name__ == "__main__":
    deck, balance = setup(bankroll=100)
    shuffled_deck = shuffle_deck(deck)
    players_hand, split_hand, current_deck = player_hand(shuffled_deck, balance)
    dealers_hand, current_deck = dealer_hand(None, current_deck)
    dealers_hand, final_deck = dealer_hand(dealers_hand, current_deck)
    compare_hands(dealers_hand, players_hand, split_hand)
    save_results(dealers_hand, players_hand, split_hand, choose_strategy(final_deck))
