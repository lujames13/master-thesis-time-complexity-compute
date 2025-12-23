import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import math

def calculate_min_committee(N, f, target_prob):
    M = int(N * f)
    for C in range(1, N + 1):
        threshold = math.floor(C / 2)
        prob_failure = stats.hypergeom.sf(threshold, N, M, C)
        if prob_failure < target_prob:
            return C
    return N

# Parameters
N = 100
f = 0.3
# Range of security targets (epsilon) from 10^-1 to 10^-10
epsilons = np.logspace(-1, -10, 50)
log_epsilons = np.log10(epsilons)

# Calculate costs
cost_base = []
cost_ours = []

# Ours: 149 (approx) if p=0.01, or just O(7^2) = 49 if p -> 0
# The prompt says: E[Cost_ours] approx O(C_small^2) + p * O(N^2)
# Let's use the formula with p=0.01 for a realistic "small p" scenario, or just flat 49 if purely theoretical ideal.
# The user prompt suggests: "Line 2: Ours (almost flat...)"
# Let's model p decreasing as security demand increases? Or just constant small p?
# The prompt says: "Line 2: Ours (almost flat... slightly sloped representing p)"
# Let's assume p is constant small, e.g. 0.01, or maybe linked to epsilon? 
# Actually, the game theoretic bound says p -> 0. Let's use a very small constant p, e.g., 0.001
p = 0.001
C_small = 7

for eps in epsilons:
    # Baseline
    C_base = calculate_min_committee(N, f, eps)
    cost_base.append(C_base ** 2)
    
    # Ours
    # Cost = (1-p)*C_small^2 + p*(C_small^2 + N^2) 
    #      = C_small^2 + p*N^2
    current_cost_ours = (C_small ** 2) + p * (N ** 2)
    cost_ours.append(current_cost_ours)

plt.figure(figsize=(10, 6))
plt.plot(log_epsilons, cost_base, label='Baseline (BlockDFL)', linewidth=2.5, color='#e74c3c')
plt.plot(log_epsilons, cost_ours, label='Proposed Scheme (Audit-Augmented)', linewidth=2.5, color='#2ecc71')

plt.title('Communication Complexity vs Security Target', fontsize=14)
plt.xlabel(r'Security Level ($\log_{10}(\epsilon)$)', fontsize=12)
plt.ylabel('Communication Complexity (Messages)', fontsize=12)
plt.gca().invert_xaxis() # High security (small epsilon) to the right usually? 
# Wait, log(10^-9) is -9. log(10^-2) is -2. 
# Conventionally, "Higher Security" means lower probability of failure.
# So -9 is "Higher Security" than -2.
# If we plot from -2 to -9 (left to right), the x-axis decreases.
# Let's keep it standard: -2 on left, -9 on right. 
# This means x-axis is already inverted in value (decreasing).
# But wait, usually plots go from small to large. -9 is smaller than -2.
# If we want "Higher Security" on the right, we want -9 on the right.
# That is the natural 'decreasing' order if we think of magnitude, but mathematically -9 < -2.
# Let's just Label the X axis clearly.
# If I use plt.gca().invert_xaxis(), -2 will be on left, -9 on right? No, -2 (larger) is usually on right.
# Let's check: -10 is smaller than -1.
# By default, matplotlib sorts X. So -10 (left) to -1 (right). 
# But we want "Higher Security" on the Right. -10 is Higher Security.
# So we want -1 to -10 direction? Or just let it be -10 to -1?
# User prompt: "Line 1: BlockDFL (Exponential or Quadratic Rise)".
# As security increases (epsilon gets smaller, e.g. 10^-9), C_base increases.
# So if X is epsilon, as X decreases, Y increases.
# If X is log(epsilon), as X goes from -1 to -9, Y should increase.
# So if we plot -10 to -1, the graph will go DOWN (high sec to low sec).
# It looks better if it goes UP (Low Sec to High Sec).
# So let's plot "Security Level (1/epsilon)"? Or just invert X axis so -2 is left, -9 is right.
# Yes, let's invert X axis.
plt.gca().invert_xaxis()

plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.yscale('log') # Optional: Use log scale for Y if the difference is huge?
# User said "BlockDFL (Exponential rising)". 
# Let's stick to linear Y scale first to show the sheer scale difference, 
# or log if 75^2 (5625) vs 49 is too extreme. 5625 vs 150 is visible on linear.
# Let's try linear first.

plt.tight_layout()
plt.savefig('analysis/complexity_comparison.png')
print("Graph generated at analysis/complexity_comparison.png")
