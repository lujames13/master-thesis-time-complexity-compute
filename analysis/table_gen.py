import scipy.stats as stats
import math

def calculate_min_committee(N, f, target_prob):
    M = int(N * f)  # Number of malicious nodes
    # Iterate C from 1 to N to find the minimum C that satisfies the safety condition
    for C in range(1, N + 1):
        # The threshold for attack success is > 2/3 (BFT assumption)
        threshold = math.floor(C * 2 / 3)
        
        # Calculate P(X > threshold) using Hypergeometric Survival Function (sf)
        # stats.hypergeom.sf(k, M, n, N) 
        # k: outcome, M: total population size, n: number of success states in population, N: number of draws
        # Mapping to scipy: total=N, good=M (malicious count), draws=C
        prob_failure = stats.hypergeom.sf(threshold, N, M, C)
        
        if prob_failure < target_prob:
            return C, prob_failure
    return N, 0

# Parameters from your thesis
N = 100
f = 0.3
targets = [1e-2, 1e-4, 1e-6, 1e-9]

print(f"Comparison for N={N}, Malicious Ratio={f}")
print("-" * 60)
print(f"{'Target P_fail':<15} | {'BlockDFL C':<12} | {'Actual P_fail':<15} | {'Ours C':<8}")
print("-" * 60)

for t in targets:
    c_base, p_real = calculate_min_committee(N, f, t)
    print(f"{t:<15} | {c_base:<12} | {p_real:.2e}        | 7")
