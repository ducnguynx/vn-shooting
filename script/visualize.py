import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib import cm

def calculate_delta_xc(DH, DE, delta, AD, r, xc_max, yc_max, k):
    """
    Calculates Delta xc based on the provided formula.
    Handles division by zero if DH == DE by returning NaN.
    Filters results based on geometric constraints and position limits.
    """
    # Pre-calculate square roots to keep formula clean
    sqrt_AD_DH = np.sqrt(AD**2 + DH**2)
    sqrt_AD_DE = np.sqrt(AD**2 + DE**2)
    
    # Denominator term (DH - DE)
    denom_diff = DH - DE
    
    # Avoid division by zero: where DH equals DE, set result to Nan
    # We use a mask to safely handle the division
    with np.errstate(divide='ignore', invalid='ignore'):
        # Calculate the theoretical position xc based on DH and DE
        # xc = r * (AH + AE) / (DH - DE)
        xc = r * (sqrt_AD_DH + sqrt_AD_DE) / denom_diff

        # Calculate the theoretical position yc based on DH and DE
        # yc = (r/AD) * (DE*AH + DH*AE) / (DH - DE)
        yc = r / AD * (DE * sqrt_AD_DH + DH * sqrt_AD_DE) / denom_diff

        # Term 1 inside the modulus
        term1_inner = (DH / sqrt_AD_DH) - ((sqrt_AD_DH + sqrt_AD_DE) / denom_diff)
        
        # Term 2 inside the modulus
        term2_inner = (DE / sqrt_AD_DE) + ((sqrt_AD_DH + sqrt_AD_DE) / denom_diff)
        
        # Combine terms
        # Delta xc = delta * (r / (DH - DE)) * (|Term1| + |Term2|)
        Z = delta * (r / denom_diff) * (np.abs(term1_inner) + np.abs(term2_inner))
    
    # GEOMETRIC CONSTRAINT 1:
    # Based on the diagram, DH > DE and the difference must be at least the radius r.
    # Mask out invalid regions where DH - DE < r.
    Z[denom_diff < r] = np.nan
    
    # GEOMETRIC CONSTRAINT 2:
    # The calculated center positions xc and yc must be within reasonable bounds.
    Z[(xc < 0) | (xc > xc_max)] = np.nan
    Z[(yc < 0) | (yc > yc_max)] = np.nan

    # GEOMETRIC CONSTRAINT 3:
    # Condition: yc < (k/AD) * xc. Mask out values where yc >= (k/AD) * xc
    Z[yc >= (k / AD) * xc] = np.nan

    return Z

# ==========================================
# 1. INPUTS (Modify these values)
# ==========================================
# Constants
delta_val = 1   # Input for delta
AD_val = 650      # Input for AD
r_val = 5.6       # Input for r (assumed constant)
xc_max_val = 400  # Max allowed distance for xc
yc_max_val = 150  # Max allowed distance for yc
k_val = 150        # Input for k (controls slope constraint yc < k/AD * xc)

# Ranges for Variables (Start, Stop, Number of points)
# Warning: If ranges overlap, code handles the singularity where DH = DE
DH_range = np.linspace(0, 200, 200)  # Range for DH
DE_range = np.linspace(0, 200, 200)   # Range for DE

# ==========================================
# 2. CALCULATION
# ==========================================
# Create a grid of DH and DE values
DH_grid, DE_grid = np.meshgrid(DH_range, DE_range)

# Calculate Z values (Delta xc)
Z = calculate_delta_xc(DH_grid, DE_grid, delta_val, AD_val, r_val, xc_max_val, yc_max_val, k_val)

# ==========================================
# 3. FIND MAX & MIN
# ==========================================
# We use nanmax/nanmin to ignore any division-by-zero singularities
max_val = np.nanmax(Z)
min_val = np.nanmin(Z)

# Find the location (indices) of max and min
# Note: There might be multiple points with the same max/min; this finds the first one.
max_idx = np.where(Z == max_val)
min_idx = np.where(Z == min_val)

# Extract the DH and DE values at those indices
max_DH = DH_grid[max_idx][0]
max_DE = DE_grid[max_idx][0]
min_DH = DH_grid[min_idx][0]
min_DE = DE_grid[min_idx][0]

print("-" * 30)
print(f"Global Maximum: {max_val:.4f}")
print(f"At DH = {max_DH:.2f}, DE = {max_DE:.2f}")
print("-" * 30)
print(f"Global Minimum: {min_val:.4f}")
print(f"At DH = {min_DH:.2f}, DE = {min_DE:.2f}")
print("-" * 30)

# ==========================================
# 4. PLOTTING
# ==========================================
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(DH_grid, DE_grid, Z, cmap=cm.viridis,
                       linewidth=0, antialiased=False, alpha=0.8)

# Highlight Max and Min points
ax.scatter(max_DH, max_DE, max_val, color='red', s=100, label='Max', edgecolors='black')
ax.scatter(min_DH, min_DE, min_val, color='blue', s=100, label='Min', edgecolors='white')

# Labels and Title
ax.set_xlabel('DH')
ax.set_ylabel('DE')
ax.set_zlabel('Delta xc')
ax.set_title(f'Surface Plot of Delta xc\n(AD={AD_val}, r={r_val}, k={k_val})')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)
ax.legend()

plt.show()