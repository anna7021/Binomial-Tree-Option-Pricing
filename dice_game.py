'''
    question: You are a risk-neutral investor and you have a fair six-sided dice (numbered
1-6) and you are asked to participate in the following gamble. You are allowed
to throw the dice a maximum of three times, after each throw you have two
choices:
    A: To throw the dice again
    B: To stop and receive $10 per point showing on the dice.
    Obviously, if you throw the dice for the third time you must choose B.
    a) What is your optimal strategy, i.e what scores would lead you to stop on
the first and second rolls?
    b) What is the fair price (assume that you are risk neutral) to pay to
enter into this particular gamble?
    c) What would be the impact on your answers to parts a) and b) if the
number of throws was increased to 5?
'''
import numpy as np
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("dice_game.log"),
        logging.StreamHandler()
    ]
)

def dice_game(max_throws=3, sides=6):
    """
    Calculate the optimal strategy and fair price for the dice gamble.

    :param max_throws: Maximum number of throws allowed.
    :param sides: Number of sides on the dice.
    :return: (strategy, fair_price)
    """
    expected_values = np.zeros((max_throws + 1, sides + 1)) #  # Rows: throws, Columns: dice scores

    # if reaches the last step, you have to stop
    for score in range(1, sides + 1):
        expected_values[-1][score] =10 *  score

    # compute the expected value backwards
    for throws in range(max_throws - 1, 0, -1):
        for score in range(1, sides + 1):
            stop_value = 10 * score
            continuation_value = np.mean(expected_values[throws + 1][1:])
            expected_values[throws][score] = max(stop_value, continuation_value)

    # Determine the optimal strategy
    strategy = [["" for _ in range(sides + 1)] for _ in range(max_throws + 1)]
    for throws in range(1, max_throws):
        for score in range(1, sides + 1):
            stop_value = 10 * score
            continuation_value = np.mean(expected_values[throws + 1][1:])
            strategy[throws][score] = "Stop" if stop_value > continuation_value else "Continue"

    # For the last throw, always "Stop"
    for score in range(1, sides + 1):
        strategy[max_throws][score] = "Stop"

    fair_price = np.mean(expected_values[1][1:])
    return strategy, fair_price


max_throws = 3
strategy, fair_price = dice_game(max_throws=max_throws)

logging.info(f"Optimal Strategy and Fair Price for {max_throws} throws:\n")
print(f"Optimal Strategy for {max_throws} throws:")
for throws in range(1, max_throws + 1):
    logging.info(f"Throw {throws}: {strategy[throws][1:]}")
    print(f"  Throw {throws}: {strategy[throws][1:]}")  # Exclude the 0th score for clarity
logging.info(f"Fair price to pay for {max_throws} throws: ${fair_price:.2f}")
print(f"\nFair price to pay for {max_throws} throws: ${fair_price:.2f}")

max_throws = 5
strategy, fair_price = dice_game(max_throws=max_throws)

logging.info(f"Optimal Strategy and Fair Price for {max_throws} throws:\n")
print(f"Optimal Strategy for {max_throws} throws:")
for throws in range(1, max_throws + 1):
    logging.info(f"Throw {throws}: {strategy[throws][1:]}")
    print(f"  Throw {throws}: {strategy[throws][1:]}")  # Exclude the 0th score for clarity
logging.info(f"Fair price to pay for {max_throws} throws: ${fair_price:.2f}")
print(f"\nFair price to pay for {max_throws} throws: ${fair_price:.2f}")




