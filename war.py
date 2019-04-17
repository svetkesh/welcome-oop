from model import init_game

"""
Variant of the card game aka 'War'.
https://en.wikipedia.org/wiki/War_(card_game)

Run cycles is limited.

Output example:

$ python Python_Level_Two/playground/war.py

Card game starts for:  ['Player PlayerA with 26 cards',
                         'Player PlayerB with 26 cards']
Dealing hands:  C10 S5
game_cycle: 0 ['Player PlayerA with 27 cards', 'Player PlayerB with 25 cards']
...
game_cycle: 62 ['Player PlayerA with 51 cards', 'Player PlayerB with 1 cards']
Dealing hands:  C9 S9
WAR state at: 63 Cards in stack:  2
End game! Winner is: Player PlayerA with 46 cards after 63 runs!

"""
def war():
    table, players = init_game()

    CYCLES_LIMIT = 101

    print("Card game starts for: ", list(str(p) for p in players))

    for game_cycle in range(CYCLES_LIMIT):
        try:
            hand_a, hand_b = [p.draw_cards() for p in players]

            print("Dealing hands: ", hand_a[0], hand_b[0])

            table.cards = hand_a, hand_b  # passing all cards to stack

            if hand_a == hand_b:
                print("WAR state at:", game_cycle, "Cards in stack: ",\
                        len(table.cards))
                table.cards = [p.draw_cards(4) for p in players]

            else:
                if hand_a > hand_b:
                    winner = players[0]
                else:
                    winner = players[1]
                winner.cards = table.draw_cards(len(table.cards))

            print("game_cycle:", game_cycle, list(str(p) for p in players))

        except ValueError:
            """
            Winner should be found again because the previous
            winner actually could loose the game:
            ...
            Dealing hands:  H6 HQ
            game_cycle: 69 ['Player PlayerA with 50 cards',
                             'Player PlayerB with 2 cards']
            Dealing hands:  C6 H6
            End game! Winner is: Player PlayerB with 0 cards
            """
            winner = players[0] if len(players[0].cards) > len(players[1].cards)\
                                else players[1]
            print(f"End game! Winner is: {winner} after {game_cycle} runs!")
            break

        except Exception as e:
            print(f"Game aborted with {e, type(e)}")
            break


if __name__ =="__main__":
    war()
