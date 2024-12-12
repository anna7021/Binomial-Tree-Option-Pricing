import numpy as np
import logging

logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
    handlers=[
        logging.FileHandler("option_pricing.log"),  # Log file name
        logging.StreamHandler()  # Continue to output logs to the console
    ]
)

class OptionPricing:
    def __init__(self, S0, K, r, T, sigma, N, option_type="European", option_style="put"):
        """
        Initialize parameters for the option pricing model.
        :param S0: Initial stock price
        :param K: Strike price
        :param r: Risk-free rate
        :param T: Time to maturity
        :param sigma: Volatility
        :param N: Number of steps in the binomial tree
        :param option_type: "European" or "American"
        :param option_style: "call" or "put"
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.T = T
        self.sigma = sigma
        self.N = N
        self.option_type = option_type
        self.option_style = option_style.lower()
        self.dt = T / N
        self.u = np.exp(sigma * np.sqrt(self.dt))  # Up factor
        self.d = np.exp(-sigma * np.sqrt(self.dt))  # Down factor
        self.p = (np.exp(r * self.dt) - self.d) / (self.u - self.d)  # Risk-neutral probability
        self.discount = np.exp(-r * self.dt)  # Discount factor

    def stock_price_tree(self):
        """
        Generate the stock price tree.
        :return: A 2D list representing the stock prices at each node.
        """
        tree = [[self.S0]]
        for i in range(1, self.N+1): # time steps
            branch = [self.S0 * self.u ** j * self.d ** (i - j) for j in range(i + 1)] # j represents the senarios
            tree.append(branch)
        # for i, level in enumerate(tree):
        #     logging.info(f"Step {i}: {['{:.4f}'.format(x) for x in level]}")
        return tree

    def payoff_function(self, S):
        if self.option_style == "call":
            return max(S - self.K, 0)
        elif self.option_style == "put":
            return max(self.K - S, 0)
        else:
            raise ValueError("Option style must be 'call' or 'put'")

    def option_tree(self):
        """
        Generate the option price tree.
        :return: The option value at the root node.
        """
        stock_tree = self.stock_price_tree()
        option_tree = [[self.payoff_function(price) for price in stock_tree[-1]]]
        # logging.info("Payoff at Maturity Calculated.")
        # logging.info(f"Step {self.N}: {['{:.4f}'.format(x) for x in option_tree[0]]}")

        # backward update the option tree
        for i in range(self.N - 1, -1, -1): # time steps
            branch = []
            for j in range(i + 1):
                continuation_value = self.discount * (
                    self.p * option_tree[0][j + 1] + (1 - self.p) * option_tree[0][j]
                )
                if self.option_type == "American":
                    intrinsic_value = self.payoff_function(stock_tree[i][j])
                    branch.append(max(continuation_value, intrinsic_value))
                else:
                    branch.append(continuation_value)
            option_tree.insert(0, branch)
            # logging.info(f"Step {i}: {['{:.4f}'.format(x) for x in branch]}")
        return option_tree



S0 = 100  # Initial stock price
K = 105  # Strike price
r = 0.05  # Risk-free rate
T = 0.5  # Time to maturity
sigma = 0.445  # Volatility
N = 100  # Number of steps

# European Put Option
european_put = OptionPricing(S0, K, r, T, sigma, N, option_type="European", option_style="put")
european_put_tree = european_put.option_tree()
logging.info(f"Final European Put Option Value at t=0: {european_put_tree[0][0]:.4f}")

# American Put Option
american_put = OptionPricing(S0, K, r, T, sigma, N, option_type="American", option_style="put")
american_put_tree = american_put.option_tree()
logging.info(f"Final American Put Option Value at t=0: {american_put_tree[0][0]:.4f}")































