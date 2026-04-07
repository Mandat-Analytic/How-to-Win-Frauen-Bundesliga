# Profile definitions for Defender positions (CB and FB)

# ===========================================
# CENTER BACK (CB) PROFILES
# ==========================================
CB_PROFILES = {
    "Ball-Playing Centerback": {
        "metrics": {
            "high": ["Forward passes per 90", "Accurate forward passes, %", "Progressive passes per 90", 
                     "Accurate progressive passes, %", "Long passes per 90"],
            "medium": ["Accurate long passes, %", "xA per 90", "Successful dribbles, %",
                      "Progressive runs per 90"],
            "low": ["Fouls per 90", "PAdj Sliding tackles"]
        },
        "weights": {
            "Forward passes per 90": 0.12, "Accurate forward passes, %": 0.12, "Progressive passes per 90": 0.12, 
            "Accurate progressive passes, %": 0.12, "Long passes per 90": 0.10,
            "Accurate long passes, %": 0.08, "xA per 90": 0.06, "Successful dribbles, %": 0.06,
            "Progressive runs per 90": 0.06,
            "Fouls per 90": 0.08, "PAdj Sliding tackles": 0.08
        },
        "description": "Comfortable advancing play with passing and carrying",
        "color": "#1976D2"
    },
    
    "Classic Stopper Centerback": {
        "metrics": {
            "high": ["Successful defensive actions per 90", "Defensive duels per 90", "Defensive duels won, %", 
                     "Aerial duels per 90", "Aerial duels won, %"],
            "medium": ["PAdj Interceptions", "PAdj Sliding tackles", "Fouls per 90"],
            "low": ["Progressive passes per 90", "Successful dribbles, %", "Progressive runs per 90"]
        },
        "weights": {
            "Successful defensive actions per 90": 0.15, "Defensive duels per 90": 0.12, "Defensive duels won, %":0.12, 
            "Aerial duels per 90": 0.12, "Aerial duels won, %": 0.12,
            "PAdj Interceptions": 0.08, "PAdj Sliding tackles": 0.08, "Fouls per 90": 0.06,
            "Progressive passes per 90": 0.05, "Successful dribbles, %": 0.05, "Progressive runs per 90": 0.05
        },
        "description": "Pure defender, simple passes, focuses on risk-free clearances",
        "color": "#D32F2F"
    },
    
    "Aggressive Centerback (Front-footed)": {
        "metrics": {
            "high": ["PAdj Interceptions", "Progressive runs per 90", "Offensive duels won, %", 
                     "Successful dribbles, %", "PAdj Sliding tackles"],
            "medium": ["Defensive duels per 90", "Progressive passes per 90", "Forward passes per 90"],
            "low": ["Fouls per 90", "Aerial duels per 90"]
        },
        "weights": {
            "PAdj Interceptions": 0.15, "Progressive runs per 90": 0.12, "Offensive duels won, %": 0.12, 
            "Successful dribbles, %": 0.12, "PAdj Sliding tackles": 0.10,
            "Defensive duels per 90": 0.08, "Progressive passes per 90": 0.08, "Forward passes per 90": 0.08,
            "Fouls per 90": 0.08, "Aerial duels per 90": 0.07
        },
        "description": "Steps out to break up play, high-risk defender",
        "color": "#FF5722"
    },
    
    "Sweeper Centerback (Covering Type)": {
        "metrics": {
            "high": ["Successful defensive actions per 90", "PAdj Interceptions", "Accurate progressive passes, %", 
                     "Accurate forward passes, %", "Accurate long passes, %"],
            "medium": ["Defensive duels won, %", "Progressive passes per 90", "Long passes per 90"],
            "low": ["PAdj Sliding tackles", "Progressive runs per 90", "Offensive duels won, %"]
        },
        "weights": {
            "Successful defensive actions per 90": 0.13, "PAdj Interceptions": 0.13, "Accurate progressive passes, %": 0.12, 
            "Accurate forward passes, %": 0.12, "Accurate long passes, %": 0.10,
            "Defensive duels won, %": 0.08, "Progressive passes per 90": 0.08, "Long passes per 90": 0.08,
            "PAdj Sliding tackles": 0.06, "Progressive runs per 90": 0.05, "Offensive duels won, %": 0.05
        },
        "description": "Reads play, protects space behind, calmer defender",
        "color": "#388E3C"
    }
}

# ==========================================
# FULLBACK (FB) PROFILES
# ==========================================
FB_PROFILES = {
    "Inverted Fullback (Connector-Hybrid Midfielder)": {
        "metrics": {
            "high": ["Accurate forward passes, %", "Progressive passes per 90", 
                     "Accurate progressive passes, %", "Forward passes per 90"],
            "medium": ["xA per 90", "Long passes per 90", "Accurate long passes, %",
                      "Progressive runs per 90", "Offensive duels won, %"],
            "low": ["Aerial duels per 90", "PAdj Sliding tackles", "Fouls per 90"]
        },
        "weights": {
            "Accurate forward passes, %": 0.13, "Progressive passes per 90": 0.13, 
            "Accurate progressive passes, %": 0.12, "Forward passes per 90": 0.12,
            "xA per 90": 0.08, "Long passes per 90": 0.08, "Accurate long passes, %": 0.08,
            "Progressive runs per 90": 0.06, "Offensive duels won, %": 0.06,
            "Aerial duels per 90": 0.05, "PAdj Sliding tackles": 0.05, "Fouls per 90": 0.04
        },
        "description": "Facilitates ball circulation; prioritizes short, safe passes to link defense with midfield",
        "color": "#1976D2"
    },
    
    "Inverted Fullback (Creator-Hybrid Midfielder)": {
        "metrics": {
            "high": ["xA per 90", "Progressive passes per 90", "Long passes per 90",
                     "Accurate long passes, %", "Progressive runs per 90"],
            "medium": ["Forward passes per 90", "Accurate forward passes, %",
                      "Successful dribbles, %", "Offensive duels won, %"],
            "low": ["Defensive duels per 90", "PAdj Sliding tackles", "Aerial duels per 90"]
        },
        "weights": {
            "xA per 90": 0.15, "Progressive passes per 90": 0.12, "Long passes per 90": 0.10,
            "Accurate long passes, %": 0.10, "Progressive runs per 90": 0.10,
            "Forward passes per 90": 0.08, "Accurate forward passes, %": 0.08,
            "Successful dribbles, %": 0.07, "Offensive duels won, %": 0.06,
            "Defensive duels per 90": 0.05, "PAdj Sliding tackles": 0.05, "Aerial duels per 90": 0.04
        },
        "description": "More progressive intent; actively looks to break lines with passes and forward movement",
        "color": "#00897B"
    },
    
    "Overlapping Fullback (Traditional Wide Runner)": {
        "metrics": {
            "high": ["Progressive runs per 90", "xA per 90", "Offensive duels won, %",
                     "Successful dribbles, %"],
            "medium": ["Long passes per 90", "Accurate long passes, %", "Forward passes per 90",
                      "Progressive passes per 90", "Non-penalty goals per 90"],
            "low": ["Defensive duels per 90", "PAdj Interceptions", "Aerial duels won, %"]
        },
        "weights": {
            "Progressive runs per 90": 0.15, "xA per 90": 0.13, "Offensive duels won, %": 0.12,
            "Successful dribbles, %": 0.12,
            "Long passes per 90": 0.07, "Accurate long passes, %": 0.07, "Forward passes per 90": 0.07,
            "Progressive passes per 90": 0.07, "Non-penalty goals per 90": 0.06,
            "Defensive duels per 90": 0.05, "PAdj Interceptions": 0.05, "Aerial duels won, %": 0.04
        },
        "description": "Stretches the play wide; overlaps winger to deliver crosses and provide width in attack",
        "color": "#F9A825"
    },
    
    "Defensive Fullback": {
        "metrics": {
            "high": ["Successful defensive actions per 90", "Defensive duels won, %",
                     "PAdj Sliding tackles", "PAdj Interceptions"],
            "medium": ["Defensive duels per 90", "Aerial duels won, %", "Fouls per 90",
                      "Accurate forward passes, %"],
            "low": ["Progressive runs per 90", "xA per 90", "Successful dribbles, %"]
        },
        "weights": {
            "Successful defensive actions per 90": 0.15, "Defensive duels won, %": 0.13,
            "PAdj Sliding tackles": 0.12, "PAdj Interceptions": 0.12,
            "Defensive duels per 90": 0.09, "Aerial duels won, %": 0.08, "Fouls per 90": 0.06,
            "Accurate forward passes, %": 0.07,
            "Progressive runs per 90": 0.06, "xA per 90": 0.06, "Successful dribbles, %": 0.06
        },
        "description": "Remains disciplined in backline; prioritizes defensive duties and maintaining positional structure",
        "color": "#5E35B1"
    },
    
    "High-Pressing Fullback (Aggressive Presser)": {
        "metrics": {
            "high": ["Defensive duels per 90", "Successful defensive actions per 90",
                     "Progressive runs per 90", "Fouls per 90"],
            "medium": ["Defensive duels won, %", "PAdj Interceptions", "Offensive duels won, %",
                      "Progressive passes per 90"],
            "low": ["Aerial duels per 90", "Long passes per 90", "xG per 90"]
        },
        "weights": {
            "Defensive duels per 90": 0.15, "Successful defensive actions per 90": 0.13,
            "Progressive runs per 90": 0.12, "Fouls per 90": 0.10,
            "Defensive duels won, %": 0.09, "PAdj Interceptions": 0.09, "Offensive duels won, %": 0.08,
            "Progressive passes per 90": 0.07,
            "Aerial duels per 90": 0.06, "Long passes per 90": 0.06, "xG per 90": 0.05
        },
        "description": "Steps high to press and regain ball early; aggressive in winning possession back quickly",
        "color": "#43A047"
    },
    
    "Counter-Attacking Fullback": {
        "metrics": {
            "high": ["Progressive runs per 90", "Successful dribbles, %", "xA per 90"],
            "medium": ["Offensive duels won, %", "Progressive passes per 90", 
                      "Defensive duels won, %", "Non-penalty goals per 90"],
            "low": ["PAdj Sliding tackles", "Aerial duels per 90", "Fouls per 90"]
        },
        "weights": {
            "Progressive runs per 90": 0.17, "Successful dribbles, %": 0.15, "xA per 90": 0.13,
            "Offensive duels won, %": 0.10, "Progressive passes per 90": 0.09, 
            "Defensive duels won, %": 0.08, "Non-penalty goals per 90": 0.08,
            "PAdj Sliding tackles": 0.07, "Aerial duels per 90": 0.07, "Fouls per 90": 0.06
        },
        "description": "Explosive transitions from defense to attack; capitalizes on space during counter-attacks",
        "color": "#FF5722"
    },
    
    "Aerial Dominant Fullback": {
        "metrics": {
            "high": ["Aerial duels per 90", "Aerial duels won, %", "Defensive duels won, %",
                     "Long passes per 90"],
            "medium": ["Successful defensive actions per 90", "Accurate long passes, %",
                      "PAdj Interceptions", "Forward passes per 90"],
            "low": ["Progressive runs per 90", "Successful dribbles, %", "xG per 90"]
        },
        "weights": {
            "Aerial duels per 90": 0.15, "Aerial duels won, %": 0.15, "Defensive duels won, %": 0.12,
            "Long passes per 90": 0.10,
            "Successful defensive actions per 90": 0.09, "Accurate long passes, %": 0.09,
            "PAdj Interceptions": 0.08, "Forward passes per 90": 0.07,
            "Progressive runs per 90": 0.05, "Successful dribbles, %": 0.05, "xG per 90": 0.05
        },
        "description": "Dominates aerial situations; excellent at defending crosses and winning headers in both boxes",
        "color": "#6A1B9A"
    }
}
