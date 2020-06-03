# ECON 28000 Final Paper
# Numerical computation for model solutions

# Yongju Kim, Jeong Whan Lee
# Last updated: June 1 2020

from itertools import combinations

def partial_pa(t, tl, tr):
    '''
    Computes partial derivative of p* (optimal price) w.r.t. alpha
    '''
    numerator = (1 / (t + tl) - 1 / (t + tr)) * t
    denominator = -2 * (1 / (t + tl) + 1 / (t + tr))
    return numerator / denominator


def compute_alpha(t, tl, tr, al, ar, pl, pr):
    '''
    Computes alpha* (optimal location)
    '''
    partial = partial_pa(t, tl, tr)
    gamma = (tl * al - pl) / (t + tl) - (tr * ar + pr) / (t + tr)
    
    term1 = partial + (1/(t+tr) - 1/(t+tl)) * t / (2 * (1/(t+tr) + 1/(t+tl)))
    term2 = (1/(t+tr) - 1/(t+tl)) * partial * t
    
    return gamma * term1 / term2, partial


def compute_price(t, tl, tr, al, ar, pl, pr):
    '''
    Computes p* (optimal price)
    '''
    alpha, partial = compute_alpha(t, tl, tr, al, ar, pl, pr)
    
    rest_numer = (tl * al - pl)/(t + tl) - (tr * ar + pr)/(t + tr)
    rest_denom = -2 * (1/(t+tr) + 1/(t+tl))
    rest = rest_numer / rest_denom
    
    price = partial * alpha + rest
    
    # addressing "left-right" size comparison ambiguity    
    if price < 0:
        price *= -1
        
    return price, alpha, partial


def compute_profit(t, tl, tr, al, ar, pl, pr):
    '''
    Computes profit at the optimal location and price
    '''
    p, alpha, partial = compute_price(t, tl, tr, al, ar, pl, pr)
    
    xr = (t*alpha + tr*ar + pr - p) / (t + tr)
    xl = (t*alpha + tl*al - pl + p) / (t + tl)
    size = xr - xl
    
    # addressing "left-right" size comparison ambiguity         
    if size < 0:
        size *= -1
        
    profit = size * p
    return profit, p, alpha


def tcost(reputation):
    '''
    Travel cost based on reputation score
    '''
    return (1/reputation)**0.5


t, al, ar = tcost(0.1), 0, 3.14159/3

# price and travel cost parameters from the data
info = {"Starbucks":(4.1, tcost(3.228049)), "Twosome Place":(4.1, tcost(0.792145)),
        "Ediya":(3.2, tcost(0.63633)), "Hollys":(4.1, tcost(0.334763)),
        "Angel-in-us":(4.8, tcost(0.228564)), "Coffee Bean":(4.8, tcost(0.474797))}

brandlist = list(info.keys())
pairs = list(combinations(brandlist, 2))

result = dict()
recommend = dict()


for pair in pairs:
    
    if info[pair[0]][1] < info[pair[1]][1]:
        L, R = pair[0], pair[1]
    
    else:
        L, R = pair[1], pair[0]
        
    profit, price, alpha = compute_profit(t, info[L][1], info[R][1],
                                          al, ar, info[L][0], info[R][0])
    
    result[pair] = (profit, price, alpha)


for pair in result:
    
    if result[pair][2] % (2 * 3.14159) <= 3.14159 / 3:
        recommend[pair] = result[pair]
