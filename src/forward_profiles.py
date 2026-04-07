
# Profile definitions for Football Scouting App

# ==========================================
# CENTER FORWARD (CF) PROFILES
# ==========================================
CF_PROFILES = {
    "Target Man": {
        "metrics": {
            "high": ["Aerial duels per 90", "Aerial duels won, %", "Goals per 90", "Touches in box per 90", "xG per 90", "Shot assists per 90"],
            "medium": ["Shots per 90", "Goal conversion, %", "Offensive duels won, %", "Accurate passes, %"],
            "low": ["Progressive runs per 90", "Dribbles per 90", "Successful dribbles, %", "Accelerations per 90"]
        },
        "weights": {
            "Aerial duels per 90": 0.15, "Aerial duels won, %": 0.15, "Goals per 90": 0.15, 
            "Touches in box per 90": 0.10, "xG per 90": 0.10, "Shot assists per 90": 0.05,
            "Shots per 90": 0.05, "Goal conversion, %": 0.05, "Offensive duels won, %": 0.05, "Accurate passes, %": 0.05,
            "Progressive runs per 90": 0.025, "Dribbles per 90": 0.025, "Successful dribbles, %": 0.025, "Accelerations per 90": 0.025
        },
        "description": "Physical aerial presence who acts as a focal point, winning headers and bringing teammates into play.",
        "color": "#6A1B9A"
    },
    "Poacher": {
        "metrics": {
            "high": ["Goals per 90", "Non-penalty goals per 90", "xG per 90", "Touches in box per 90", "Shots on target, %", "Goal conversion, %"],
            "medium": ["Shots per 90", "Goals/xG", "Offensive duels per 90"],
            "low": ["Accurate passes, %", "Progressive passes per 90", "Dribbles per 90", "Smart passes per 90"]
        },
        "weights": {
            "Goals per 90": 0.20, "Non-penalty goals per 90": 0.15, "xG per 90": 0.15, 
            "Touches in box per 90": 0.10, "Shots on target, %": 0.10, "Goal conversion, %": 0.10,
            "Shots per 90": 0.05, "Goals/xG": 0.05, "Offensive duels per 90": 0.05,
            "Accurate passes, %": 0.01, "Progressive passes per 90": 0.01, "Dribbles per 90": 0.01, "Smart passes per 90": 0.02
        },
        "description": "Clinical finisher who specializes in converting chances inside the penalty area.",
        "color": "#E53935"
    },
    "Second Striker": {
        "metrics": {
            "high": ["Assists per 90", "xA per 90", "Smart passes per 90", "Progressive passes per 90", "Offensive duels per 90"],
            "medium": ["Goals per 90", "xG per 90", "Dribbles per 90", "Successful dribbles, %", "Accurate passes, %", "Shot assists per 90"],
            "low": ["Aerial duels per 90", "Aerial duels won, %", "Touches in box per 90"]
        },
        "weights": {
            "Assists per 90": 0.15, "xA per 90": 0.15, "Smart passes per 90": 0.10, "Progressive passes per 90": 0.10, "Offensive duels per 90": 0.10,
            "Goals per 90": 0.05, "xG per 90": 0.05, "Dribbles per 90": 0.05, "Successful dribbles, %": 0.05, "Accurate passes, %": 0.05, "Shot assists per 90": 0.05,
            "Aerial duels per 90": 0.03, "Aerial duels won, %": 0.03, "Touches in box per 90": 0.04
        },
        "description": "Drops deep to link play, creates chances for teammates while contributing defensively.",
        "color": "#00897B"
    },
    "Complete Forward": {
        "metrics": {
            "high": ["Goals per 90", "xG per 90", "Assists per 90", "xA per 90", "Shot assists per 90", "Aerial duels won, %"],
            "medium": ["Accurate passes, %", "Smart passes per 90", "Progressive passes per 90", "Dribbles per 90", "Successful dribbles, %", "Offensive duels won, %"],
            "low": ["Progressive runs per 90", "Accelerations per 90"]
        },
        "weights": {
            "Goals per 90": 0.35, "xG per 90": 0.15, "Assists per 90": 0.10, "xA per 90": 0.10, "Shot assists per 90": 0.10, "Aerial duels won, %": 0.10,
            "Accurate passes, %": 0.04, "Smart passes per 90": 0.04, "Progressive passes per 90": 0.04, "Dribbles per 90": 0.04, "Successful dribbles, %": 0.04, "Offensive duels won, %": 0.04,
            "Progressive runs per 90": 0.03, "Accelerations per 90": 0.03
        },
        "description": "Elite all-around striker who excels in scoring, creating, and physical duels.",
        "color": "#F9A825"
    },
    "Aggressive Presser": {
        "metrics": {
            "high": ["Defensive duels won, %", "Accelerations per 90", "Progressive runs per 90"],
            "medium": ["Offensive duels per 90", "Dribbles per 90"],
            "low": ["Aerial duels won, %", "Touches in box per 90"]
        },
        "weights": {
            "Defensive duels won, %": 0.25, "Accelerations per 90": 0.20, "Progressive runs per 90": 0.20,
            "Offensive duels per 90": 0.10, "Dribbles per 90": 0.10,
            "Aerial duels won, %": 0.07, "Touches in box per 90": 0.08
        },
        "description": "Energetic forward who leads the press and covers significant ground defensively.",
        "color": "#43A047"
    },
    "Passive Presser": {
        "metrics": {
            "high": ["Accurate passes, %", "Smart passes per 90"],
            "medium": ["Defensive duels won, %", "Aerial duels won, %", "Goals per 90"],
            "low": ["Progressive runs per 90", "Accelerations per 90", "Dribbles per 90"]
        },
        "weights": {
            "Accurate passes, %": 0.25, "Smart passes per 90": 0.25,
            "Defensive duels won, %": 0.10, "Aerial duels won, %": 0.10, "Goals per 90": 0.10,
            "Progressive runs per 90": 0.06, "Accelerations per 90": 0.07, "Dribbles per 90": 0.07
        },
        "description": "Maintains tactical discipline, conserves energy for key moments, and provides reliable passing.",
        "color": "#5E35B1"
    }
}

# ==========================================
# WINGER PROFILES
# ==========================================
WINGER_PROFILES = {
    "Playmaking Winger": {
        "metrics": {
            "high": ["xA per 90", "Smart passes per 90", "Progressive passes per 90", "Passes to penalty area per 90", "Accurate passes to penalty area, %"],
            "medium": ["Assists per 90", "Shot assists per 90", "Deep completions per 90", "Successful dribbles, %", "Touches in box per 90"],
            "low": ["Progressive runs per 90", "Accelerations per 90", "Offensive duels per 90"]
        },
        "weights": {
            "xA per 90": 0.15, "Smart passes per 90": 0.15, "Progressive passes per 90": 0.10, "Passes to penalty area per 90": 0.10, "Accurate passes to penalty area, %": 0.10,
            "Assists per 90": 0.05, "Shot assists per 90": 0.05, "Deep completions per 90": 0.05, "Successful dribbles, %": 0.05, "Touches in box per 90": 0.05,
            "Progressive runs per 90": 0.05, "Accelerations per 90": 0.05, "Offensive duels per 90": 0.05
        },
        "description": "Cuts inside to create chances, acts as an auxiliary playmaker.",
        "color": "#1976D2"
    },
    "Direct Winger": {
        "metrics": {
            "high": ["Dribbles per 90", "Successful dribbles, %", "Progressive runs per 90", "Accelerations per 90", "Offensive duels per 90"],
            "medium": ["Offensive duels won, %", "Touches in box per 90", "Deep completions per 90", "Passes to penalty area per 90"],
            "low": ["Smart passes per 90", "Progressive passes per 90", "xA per 90"]
        },
        "weights": {
            "Dribbles per 90": 0.15, "Successful dribbles, %": 0.15, "Progressive runs per 90": 0.15, "Accelerations per 90": 0.15, "Offensive duels per 90": 0.10,
            "Offensive duels won, %": 0.05, "Touches in box per 90": 0.05, "Deep completions per 90": 0.05, "Passes to penalty area per 90": 0.05,
            "Smart passes per 90": 0.03, "Progressive passes per 90": 0.03, "xA per 90": 0.04
        },
        "description": "Stays wide, beats fullbacks with pace, delivers crosses.",
        "color": "#FF6B35"
    },
    "Hybrid Winger": {
        "metrics": {
            "high": ["Goals per 90", "Non-penalty goals per 90", "xG per 90", "Shots per 90", "Touches in box per 90"],
            "medium": ["Goal conversion, %", "Shots on target, %", "Progressive runs per 90", "Accelerations per 90"],
            "low": ["Smart passes per 90", "xA per 90", "Deep completions per 90"]
        },
        "weights": {
            "Goals per 90": 0.15, "Non-penalty goals per 90": 0.15, "xG per 90": 0.15, "Shots per 90": 0.10, "Touches in box per 90": 0.10,
            "Goal conversion, %": 0.05, "Shots on target, %": 0.05, "Progressive runs per 90": 0.05, "Accelerations per 90": 0.05,
            "Smart passes per 90": 0.05, "xA per 90": 0.05, "Deep completions per 90": 0.05
        },
        "description": "Primarily focused on scoring goals, drifts inside frequently.",
        "color": "#FF9800"
    },
    "Aggressive Presser": {
        "metrics": {
            "high": ["Defensive duels per 90", "Defensive duels won, %", "Accelerations per 90", "Progressive runs per 90", "Offensive duels per 90"],
            "medium": ["Goals per 90", "Shots per 90", "Touches in box per 90", "Successful dribbles, %"],
            "low": ["Smart passes per 90", "xA per 90", "Passes to penalty area per 90"]
        },
        "weights": {
            "Defensive duels per 90": 0.15, "Defensive duels won, %": 0.15, "Accelerations per 90": 0.15, "Progressive runs per 90": 0.10, "Offensive duels per 90": 0.10,
            "Goals per 90": 0.05, "Shots per 90": 0.05, "Touches in box per 90": 0.05, "Successful dribbles, %": 0.05,
            "Smart passes per 90": 0.05, "xA per 90": 0.05, "Passes to penalty area per 90": 0.05
        },
        "description": "Actively engages in pressing traps high up the pitch.",
        "color": "#D32F2F"
    },
    "Passive Presser": {
        "metrics": {
            "high": ["Goals per 90", "xG per 90", "xA per 90", "Smart passes per 90", "Shot assists per 90"],
            "medium": ["Assists per 90", "Successful dribbles, %", "Touches in box per 90", "Passes to penalty area per 90"],
            "low": ["Defensive duels per 90", "Defensive duels won, %", "Accelerations per 90"]
        },
        "weights": {
            "Goals per 90": 0.15, "xG per 90": 0.15, "xA per 90": 0.15, "Smart passes per 90": 0.10, "Shot assists per 90": 0.10,
            "Assists per 90": 0.05, "Successful dribbles, %": 0.05, "Touches in box per 90": 0.05, "Passes to penalty area per 90": 0.05,
            "Defensive duels per 90": 0.05, "Defensive duels won, %": 0.05, "Accelerations per 90": 0.05
        },
        "description": "Minimal defensive involvement, stays higher for transitions.",
        "color": "#9C27B0"
    }
}

# ==========================================
# CAM PROFILES
# ==========================================
CAM_PROFILES = {
    "Classic No. 10": {
        "metrics": {
            "high": ["xA per 90", "Assists per 90", "Shot assists per 90", "Smart passes per 90", "Accurate through passes, %", "Accurate passes to final third, %", "Deep completions per 90"],
            "medium": ["Progressive passes per 90", "Crosses per 90", "Accurate crosses, %", "Successful attacking actions per 90"],
            "low": ["Defensive duels per 90", "PAdj Sliding tackles", "Accurate back passes, %"]
        },
        "weights": {
            "xA per 90": 0.12, "Assists per 90": 0.12, "Shot assists per 90": 0.10, "Smart passes per 90": 0.10, "Accurate through passes, %": 0.10, "Accurate passes to final third, %": 0.10, "Deep completions per 90": 0.10,
            "Progressive passes per 90": 0.05, "Crosses per 90": 0.05, "Accurate crosses, %": 0.05, "Successful attacking actions per 90": 0.05,
            "Defensive duels per 90": 0.02, "PAdj Sliding tackles": 0.02, "Accurate back passes, %": 0.02
        },
        "description": "Operates exclusively in the final third; creates high-quality chances with exceptional vision and precise final balls.",
        "color": "#7B1FA2"
    },
    "Second Striker": {
        "metrics": {
            "high": ["Non-penalty goals per 90", "xG per 90", "Shots per 90", "Touches in box per 90", "Shots on target, %"],
            "medium": ["Goal conversion, %", "Progressive runs per 90", "Accelerations per 90", "Assists per 90", "Offensive duels won, %"],
            "low": ["Passes per 90", "Accurate back passes, %", "Defensive duels per 90"]
        },
        "weights": {
            "Non-penalty goals per 90": 0.15, "xG per 90": 0.15, "Shots per 90": 0.15, "Touches in box per 90": 0.15, "Shots on target, %": 0.10,
            "Goal conversion, %": 0.05, "Progressive runs per 90": 0.05, "Accelerations per 90": 0.05, "Assists per 90": 0.05, "Offensive duels won, %": 0.05,
            "Passes per 90": 0.02, "Accurate back passes, %": 0.01, "Defensive duels per 90": 0.02
        },
        "description": "Plays between midfield and attack; makes intelligent runs into the box and prioritizes goal-scoring over creation.",
        "color": "#C62828"
    },
    "Deep Playmaker": {
        "metrics": {
            "high": ["Passes per 90", "Accurate passes, %", "Accurate back passes, %", "Progressive passes per 90", "Forward passes per 90", "Accurate long passes, %"],
            "medium": ["Deep completions per 90", "Smart passes per 90", "xA per 90", "Accurate passes to final third, %", "Defensive duels per 90"],
            "low": ["Shots per 90", "Touches in box per 90", "Accelerations per 90"]
        },
        "weights": {
            "Passes per 90": 0.12, "Accurate passes, %": 0.12, "Accurate back passes, %": 0.10, "Progressive passes per 90": 0.10, "Forward passes per 90": 0.10, "Accurate long passes, %": 0.10,
            "Deep completions per 90": 0.05, "Smart passes per 90": 0.05, "xA per 90": 0.05, "Accurate passes to final third, %": 0.05, "Defensive duels per 90": 0.05,
            "Shots per 90": 0.03, "Touches in box per 90": 0.04, "Accelerations per 90": 0.04
        },
        "description": "Drops deep to collect the ball from defenders; orchestrates play from the first phase with excellent passing range and vision.",
        "color": "#00695C"
    },
    "Aggressive Presser": {
        "metrics": {
            "high": ["Successful defensive actions per 90", "Defensive duels per 90", "PAdj Interceptions", "Accelerations per 90"],
            "medium": ["Defensive duels won, %", "Fouls per 90", "Offensive duels per 90", "Progressive runs per 90"],
            "low": ["Accurate back passes, %", "Aerial duels per 90"]
        },
        "weights": {
            "Successful defensive actions per 90": 0.20, "Defensive duels per 90": 0.20, "PAdj Interceptions": 0.15, "Accelerations per 90": 0.15,
            "Defensive duels won, %": 0.05, "Fouls per 90": 0.05, "Offensive duels per 90": 0.05, "Progressive runs per 90": 0.05,
            "Accurate back passes, %": 0.05, "Aerial duels per 90": 0.05
        },
        "description": "Leads the press from advanced positions; aggressively closes down opponents and triggers team pressing sequences.",
        "color": "#2E7D32"
    },
    "Passive Presser": {
        "metrics": {
            "high": ["xA per 90", "Smart passes per 90", "Accurate passes, %"],
            "medium": ["Progressive passes per 90", "Shot assists per 90", "Assists per 90", "Successful attacking actions per 90"],
            "low": ["Defensive duels per 90", "Successful defensive actions per 90", "PAdj Sliding tackles", "Accelerations per 90", "Progressive runs per 90"]
        },
        "weights": {
            "xA per 90": 0.20, "Smart passes per 90": 0.20, "Accurate passes, %": 0.15,
            "Progressive passes per 90": 0.08, "Shot assists per 90": 0.08, "Assists per 90": 0.08, "Successful attacking actions per 90": 0.08,
            "Defensive duels per 90": 0.02, "Successful defensive actions per 90": 0.02, "PAdj Sliding tackles": 0.03, "Accelerations per 90": 0.03, "Progressive runs per 90": 0.03
        },
        "description": "Conserves energy for attacking phases; rarely engages defensively and focuses entirely on creative output.",
        "color": "#AD1457"
    }
}
