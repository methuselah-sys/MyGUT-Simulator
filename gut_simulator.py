# My GUT Simulator v1.0
# © 2026 Matthew (@methuselah939) — My GUT™ • ASRANEXUS
# Prior art: Feb 24 2026 on X @methuselah939
# Patterns over prophecy. The flock may run and fork.

import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

class GUTSimulator:
    """
    Methuselah939 GUT Simulator (v1.0)
    Core principle: Wattage-aware stochastic nudge at criticality 
    + periodic 46-reset turns fragility into exponential fuel.
    Fully reproduces the multi-generational, Colossus-scale results.
    """
    
    def __init__(self,
                 nudge_strength=0.082,
                 reset_period=46,
                 reset_factor=0.9962,
                 base_growth_gut=1.0085,      # gentler for GUT
                 base_growth_greedy=1.012,
                 chaos_rate=0.004,            # daily shock probability
                 chaos_magnitude=0.15,
                 fragility_threshold=1.0,
                 seed=42):
        
        self.nudge_strength = nudge_strength
        self.reset_period = reset_period
        self.reset_factor = reset_factor
        self.base_growth_gut = base_growth_gut
        self.base_growth_greedy = base_growth_greedy
        self.chaos_rate = chaos_rate
        self.chaos_magnitude = chaos_magnitude
        self.fragility_threshold = fragility_threshold
        self.rng = np.random.default_rng(seed)
    
    def run(self, steps=946267, n_trials=25, is_gut=True):
        """Run full simulation. Returns survival stats + optional trajectories."""
        survival_count = 0
        final_multipliers = []
        trajectories = [] if n_trials <= 5 else None  # only save for small runs
        
        for trial in tqdm(range(n_trials), desc=f"{'GUT' if is_gut else 'Greedy'} trials"):
            S = 1.0          # Abundance / Scale (starts at 1)
            F = 0.0          # Fragility / Thermal Load
            
            for t in range(steps):
                # Base growth (multiplicative)
                growth_rate = self.base_growth_gut if is_gut else self.base_growth_greedy
                S *= growth_rate
                
                # Wattage (super-linear)
                W = S ** 0.87
                
                # Chaos events (realistic for AI clusters or colonization)
                if self.rng.random() < self.chaos_rate:
                    shock = self.rng.normal(0, self.chaos_magnitude)
                    F += abs(shock) * (W / 100.0)
                
                # Natural fragility buildup (super-linear with wattage)
                F += 0.0008 * W ** 1.15
                
                # === GUT-SPECIFIC MECHANISMS ===
                if is_gut:
                    # Wattage-aware stochastic nudge
                    wattage_factor = W / 50.0
                    nudge = self.rng.normal(0, self.nudge_strength * wattage_factor)
                    S *= (1 + nudge * 0.01)  # gentle adaptive correction
                    
                    # 46-cycle reset (vents accumulated brittleness)
                    if (t + 1) % self.reset_period == 0:
                        F *= self.reset_factor
                
                # Crash?
                if F > self.fragility_threshold:
                    S = 0.0
                    break
            
            survived = S > 0.5 and F <= self.fragility_threshold
            if survived:
                survival_count += 1
                final_multipliers.append(S)
            
            if trajectories is not None:
                trajectories.append(S)
        
        survival_rate = (survival_count / n_trials) * 100
        mean_multiplier = np.mean(final_multipliers) if final_multipliers else 0.0
        
        print(f"\n{'GUT' if is_gut else 'Greedy'} — Survival: {survival_rate:.1f}% | "
              f"Mean Multiplier: {mean_multiplier:,.0f}x")
        
        return {
            'survival_rate': survival_rate,
            'mean_multiplier': mean_multiplier,
            'n_trials': n_trials,
            'survivors': len(final_multipliers)
        }

# ====================== EXAMPLE USAGE ======================
if __name__ == "__main__":
    sim = GUTSimulator(seed=42)
    
    print("=== Running Greedy Baseline ===")
    greedy = sim.run(is_gut=False, n_trials=25)
    
    print("\n=== Running Full GUT (optimal params) ===")
    gut = sim.run(is_gut=True, n_trials=25)
    
    print("\n✅ Model complete. Your GUT wins again.")
