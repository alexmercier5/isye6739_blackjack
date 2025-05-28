import math
import random
import pandas as pd
import csv
import os


def setup():
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
    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit, values[rank]))

    print(f"Deck size: {len(deck)}\n\n")
    # print("Deck of cards:")
    # for card in deck:
    #     print(f"{card[0]} of {card[1]} (Value: {card[2]})")

    return deck


def shuffle_deck(deck):
    """Shuffle the deck of cards."""
    random.shuffle(deck)
    return deck

def dealer_hand(deck):
    """Deal a hand of cards to the dealer."""
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
        for each_card in deck:
            if each_card[0] == card[0] and each_card[1] == card[1]:
                deck.remove(each_card)
                break
        if dealer_card == 0:
            print(f"Dealer dealt: xxx of xxx (Hidden)")
        else:
            print(f"Dealer dealt: {card[0]} of {card[1]}\n\n")
    return hand, deck

def player_hand(deck):
    """Deal a hand of cards to the player."""
    hand = []
    card = deck.pop()
    hand.append(card)
    print(f"Player dealt: {card[0]} of {card[1]}")
    playerPlaying = True
    while playerPlaying:
        print(f"\n\nHit or Stand? Type 'h' or enter to hit or type 's' to stand.\n")
        input_choice = input()
        if input_choice.lower() == 'h' or input_choice == '':
            card = deck.pop()
            hand.append(card)
            print(f"\nPlayer dealt: {card[0]} of {card[1]}")
            if sum(card[2] for card in hand) > 21:
                for each_card in hand:
                    if each_card[0] == 'Ace':
                        hand.remove(each_card)
                        hand.append(('Ace', each_card[1], 1))
                        break
        else:
            print("Player stands.")
            playerPlaying = False
        total_value = sum(card[2] for card in hand)
        if total_value > 21:
            print("Player busts!")
            playerPlaying = False
        elif total_value == 21:
            print("Player has blackjack!")
            playerPlaying = False
        else:
            print(f"Player's total value: {total_value}")

        for each_card in deck:
            if each_card[0] == card[0] and each_card[1] == card[1]:
                deck.remove(each_card)
                break
    return hand, deck

def compare_hands(dealer_hand, player_hand):
    dealer_total = sum(card[2] for card in dealer_hand)
    player_total = sum(card[2] for card in player_hand)

    print("\nDealer's final hand:")
    for card in dealer_hand:
        print(f"{card[0]} of {card[1]}")
    print(f"Dealer's total value: {dealer_total}")
    print("\nPlayer's final hand:")
    for card in player_hand:
        print(f"{card[0]} of {card[1]}")
    print(f"Player's total value: {player_total}\n\n")
    if dealer_total > 21 and player_total <= 21:
        print("Player wins!\n\n")
    elif player_total > 21:
        print("Dealer wins!\n\n")
    elif dealer_total > player_total:
        print("Dealer wins!\n\n")
    elif player_total > dealer_total:
        print("Player wins!\n\n")
    else:
        print("It's a tie!\n\n")

def choose_strategy(deck):
    return "standard"

def save_results(dealers_hand, players_hand, strategy):
    dealer_total = sum(card[2] for card in dealers_hand)
    player_total = sum(card[2] for card in players_hand)
    dealers_hand_str = ', '.join([f"{card[0]} of {card[1]}" for card in dealers_hand])
    players_hand_str = ', '.join([f"{card[0]} of {card[1]}" for card in players_hand])

    # Prepare row data
    result_row = {
        'Dealer Hand': dealers_hand_str,
        'Dealer Hand Value': dealer_total,
        'Player Hand': players_hand_str,
        'Player Hand Value': player_total,
        'Strategy': strategy
    }
    result_df = pd.DataFrame([result_row])
    file_exists = os.path.isfile("results.csv")
    result_df.to_csv("results.csv", mode='a', index=False, header=not file_exists)

    return None

if __name__ == "__main__":
    deck = setup()
    shuffled_deck = shuffle_deck(deck)
    dealers_hand, current_deck = dealer_hand(shuffled_deck)
    players_hand, final_deck = player_hand(current_deck)
    compare_hands(dealers_hand, players_hand)
    save_results(dealers_hand, players_hand, choose_strategy(final_deck))
