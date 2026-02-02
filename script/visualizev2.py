import numpy as np
import matplotlib
# matplotlib.use('TkAgg') # Uncomment if running locally
import matplotlib.pyplot as plt
from matplotlib import cm

def calculate_delta_xc(DH, DE, delta, AD, r, xc_max, yc_max, k):
    """
    Calculates Delta xc and filters based on strict geometric constraints
    ensuring the WHOLE circle is inside the triangle.
    """
    # Pre-calculate square roots
    sqrt_AD_DH = np.sqrt(AD**2 + DH**2)
    sqrt_AD_DE = np.sqrt(AD**2 + DE**2)
    
    # Denominator term (DH - DE)
    denom_diff = DH - DE
    
    with np.errstate(divide='ignore', invalid='ignore'):
        # --- 1. Calculate Coordinates ---
        xc = r * (sqrt_AD_DH + sqrt_AD_DE) / denom_diff
        yc = r / AD * (DE * sqrt_AD_DH + DH * sqrt_AD_DE) / denom_diff

        # --- 2. Calculate Uncertainty (Delta xc) ---
        term1_inner = (DH / sqrt_AD_DH) - ((sqrt_AD_DH + sqrt_AD_DE) / denom_diff)
        term2_inner = (DE / sqrt_AD_DE) + ((sqrt_AD_DH + sqrt_AD_DE) / denom_diff)
        
        Z = delta * (r / denom_diff) * (np.abs(term1_inner) + np.abs(term2_inner))
    
    # --- 3. Apply Constraints ---
    
    # Constraint A: Shadow must be physically valid (> 2r is the strict physical limit)
    # If the shadow is smaller than the diameter, the circle implies a position beyond the screen.
    Z[denom_diff <= 2 * r] = np.nan 
    
    # Constraint B: Bounds checks
    Z[(xc < 0) | (xc > xc_max)] = np.nan
    Z[yc > yc_max] = np.nan # Simplified; yc < r check is below
    
    # Constraint C: Top Edge (AD) Clearance
    # The circle's top edge must not cross y=0. Center must be >= r.
    Z[yc < r] = np.nan

    # Constraint D: Hypotenuse (AC) Clearance ("Whole Circle" check)
    # Distance from center (xc, yc) to line (passing through 0,0 and AD,k) must be >= r
    # Line Eq: k*x - AD*y = 0.
    # We need the point to be "above" the line (smaller y), so k*xc - AD*yc must be positive.
    dist_to_hypotenuse = (k * xc - AD * yc) / np.sqrt(k**2 + AD**2)
    
    # Filter where distance is less than radius (circle crosses line)
    # or where center is on the wrong side of the line (negative distance)
    Z[dist_to_hypotenuse < r] = np.nan

    return Z

# ==========================================
# INPUTS (Unchanged)
# ==========================================
delta_val = 0.01   
AD_val = 650      
r_val = 5.6       
xc_max_val = 400  
yc_max_val = 200  
k_val = 200        

DH_range = np.linspace(0, 250, 250) # Increased slightly to catch more edge cases
DE_range = np.linspace(0, 250, 250)

# ==========================================
# CALCULATION & PLOTTING (Unchanged)
# ==========================================
DH_grid, DE_grid = np.meshgrid(DH_range, DE_range)

Z = calculate_delta_xc(DH_grid, DE_grid, delta_val, AD_val, r_val, xc_max_val, yc_max_val, k_val)

# ==========================================
# 3. FIND MAX & MIN & COORDINATES
# ==========================================
max_val = np.nanmax(Z)
min_val = np.nanmin(Z)

if np.isnan(max_val):
    print("No valid geometric solutions found in this range.")
else:
    # Find indices of max and min
    max_idx = np.where(Z == max_val)
    min_idx = np.where(Z == min_val)

    # Extract DH and DE for Max/Min
    max_DH = DH_grid[max_idx][0]
    max_DE = DE_grid[max_idx][0]
    min_DH = DH_grid[min_idx][0]
    min_DE = DE_grid[min_idx][0]

    # --- Helper function to calculate xc, yc for a single point ---
    def get_coords(DH, DE, AD, r):
        sqrt_AD_DH = np.sqrt(AD**2 + DH**2)
        sqrt_AD_DE = np.sqrt(AD**2 + DE**2)
        denom = DH - DE
        xc = r * (sqrt_AD_DH + sqrt_AD_DE) / denom
        yc = (r / AD) * (DE * sqrt_AD_DH + DH * sqrt_AD_DE) / denom
        return xc, yc

    # Calculate coordinates for the Max and Min uncertainty points
    xc_max_err, yc_max_err = get_coords(max_DH, max_DE, AD_val, r_val)
    xc_min_err, yc_min_err = get_coords(min_DH, min_DE, AD_val, r_val)

    print("-" * 40)
    print(f"Global MAXIMUM Uncertainty: {max_val:.4f} mm")
    print(f"  -> Shadow: DH = {max_DH:.2f}, DE = {max_DE:.2f}")
    print(f"  -> Position: x_c = {xc_max_err:.2f}, y_c = {yc_max_err:.2f}")
    print("-" * 40)
    print(f"Global MINIMUM Uncertainty: {min_val:.4f} mm")
    print(f"  -> Shadow: DH = {min_DH:.2f}, DE = {min_DE:.2f}")
    print(f"  -> Position: x_c = {xc_min_err:.2f}, y_c = {yc_min_err:.2f}")
    print("-" * 40)

    # ==========================================
    # 4. PLOTTING
    # ==========================================
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(DH_grid, DE_grid, Z, cmap=cm.viridis,
                           linewidth=0, antialiased=False, alpha=0.8)

    # Highlight Max and Min points
    ax.scatter(max_DH, max_DE, max_val, color='red', s=100, label='Max Uncertainty', edgecolors='black')
    ax.scatter(min_DH, min_DE, min_val, color='blue', s=100, label='Min Uncertainty', edgecolors='white')

    # Labels and Title
    ax.set_xlabel('DH (Shadow Bottom)')
    ax.set_ylabel('DE (Shadow Top)')
    ax.set_zlabel('Uncertainty Delta xc (mm)')
    ax.set_title(f'Uncertainty Landscape\n(AD={AD_val}, r={r_val}, k={k_val})')

    # Add a color bar
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.legend()

    plt.show()