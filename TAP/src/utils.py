def get_quadrant_explanation(x_axis, y_axis):
    """
    Return tactical explanations for quadrants based on index combinations.
    """
    explanations = {
        ('IOB', 'IDI'): {
            'HH': "Dominant Pressing: Controls the ball and wins it back high with extreme intensity.",
            'HL': "Patient Build-up: Dominates possession but adopts a cautious, low-intensity defensive structure.",
            'LH': "Direct Counter-Press: Direct attacking style combined with aggressive, high-pressure defending.",
            'LL': "Deep Block: Direct transitions with a conservative, low-block defensive approach."
        },
        ('IGC', 'IOB'): {
            'HH': "Efficiency & Control: High game control translating into high-volume offensive actions.",
            'HL': "sterile possession: Controls the game tempo but struggles to generate meaningful offensive threat.",
            'LH': "Chaos Efficiency: Low control but highly efficient and vertical in offensive output.",
            'LL': "Struggling Transitions: Limited control and low offensive threat; reactive playing style."
        },
        ('IDI', 'IDO'): {
            'HH': "Defensive Fortress: Aggressive pressing synchronized with elite structural organization.",
            'HL': "Disjointed Press: High intensity pressing that lacks backup organization, potentially leaving gaps.",
            'LH': "Organized Passive: Very well-structured defense but low intensity in winning the ball back.",
            'LL': "Defensive Vulnerability: Lacks both pressing intensity and structural cohesion."
        },
        ('IGC', 'ITS'): {
            'HH': "Modern Hybrid: Controls the tempo but can explode into high-speed transitions at will.",
            'HL': "Slow & Controlled: Prefers a slow, methodical build-up with very little transition speed.",
            'LH': "Transition Specialists: Sacrifices ball control to maximize speed in vertical transitions.",
            'LL': "Statical Play: Low control and slow transitions; lacks tactical dynamism."
        },
        ('IOB', 'ITS'): {
            'HH': "Transition Juggernaut: High offensive volume driven by rapid, vertical transitions.",
            'HL': "Methodical Attack: High offensive volume through sustained, slow-tempo positional play.",
            'LH': "Counter-Attack Directness: Low overall offensive volume but extremely fast when attacking.",
            'LL': "Low Threat: Limited offensive output and slow to progress the ball."
        }
    }
    
    # Check both orientations
    key = (x_axis, y_axis)
    if key in explanations:
        return explanations[key]
    key_rev = (y_axis, x_axis)
    if key_rev in explanations:
        # Swap H/L for the reversed key if needed, or just return reversed logic
        # For simplicity, I'll provide a generic one if not explicitly defined
        return explanations.get(key, explanations.get(key_rev, {
            'HH': "High in both indices indicating a dominant tactical profile in these areas.",
            'HL': f"High {x_axis} but low {y_axis}; specialized tactical focus.",
            'LH': f"Low {x_axis} but high {y_axis}; specialized tactical focus.",
            'LL': "Low in both indices indicating developmental areas for these tactical phases."
        }))
    
    return {
        'HH': "High Performance Cluster",
        'HL': f"Specialized {x_axis}",
        'LH': f"Specialized {y_axis}",
        'LL': "Efficiency Gap"
    }
