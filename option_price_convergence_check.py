import logging

from binomial_tree_option_pricing import OptionPricing
logging.basicConfig(level=logging.INFO)
logging.info("Explore the convergence of a binomial tree for american options")
logging.info("To achieve $0.01 precision, we must ensure that increasing N further does not change the option price by more than $0.005 between consecutive iterations. This way, when rounded, the price remains stable at $0.01 precision.")

def find_converged_option_price(S0, K, r, T, sigma, option_type, option_style, precision=0.01, max_steps=20):
    """
    Iteratively increase N to find the converged option price within the specified precision.
    """
    N = 2 # starting with 2 steps
    previous_price = None
    converged = False

    for step in range(1, max_steps+1):
        option_pricing = OptionPricing(S0, K, r, T, sigma, N, option_type, option_style)
        option_tree = option_pricing.option_tree()
        current_price = option_tree[0][0]

        if previous_price is not None:
            price_difference = abs(current_price - previous_price)
            if price_difference < precision/2:
                converged = True
                logging.info(f"Convergence achieved at N={N} with option price: {current_price:.4f}")
                break
        previous_price = current_price
        N += 1
    if not converged:
        logging.warning(f"Did not converge within {max_steps} iterations. Last N={N}, Option Price={current_price:.4f}")
    return current_price, N if converged else None

# Parameters
S0 = 100  # Initial stock price
K = 105  # Strike price
r = 0.05  # Risk-free rate
T = 0.5  # Time to maturity
sigma = 0.445  # Volatility
option_type_am = "American"
option_style = "put"
max_step = 500

# Find converged American Put Option Price
logging.info("Starting convergence search for American Put Option...")
am_price, am_N = find_converged_option_price(S0, K, r, T, sigma, option_type_am, option_style, precision=0.01, max_steps=max_step)
if am_N:
    logging.info(f"American Put Option converged to {am_price:.2f} with N={am_N}")
else:
    logging.info(f"American Put Option price: {am_price:.2f} (did not fully converge)")