# Profile definitions for Defensive and Central Midfielder positions

# ==========================================
# DEFENSIVE MIDFIELDER (DMF) PROFILES
# ==========================================
DMF_PROFILES = {
    "Deep-Lying Playmaker (Regista)": {
        "metrics": {
            "high": ["Progressive passes per 90", "Forward passes per 90",  
                    "Accurate passes, %", "xA per 90", "Accurate through passes, %", "Passes per 90"],
            "medium": ["Ball recoveries per 90", "PAdj Interceptions", 
                      "Successful dribbles, %", "Accelerations per 90"],
            "low": ["Successful defensive actions per 90", "Defensive duels per 90", "Touches in box per 90", "xG per 90", 
                    "Progressive runs per 90","Shot assists per 90"]
        },
        "weights": {
            "Progressive passes per 90": 0.12, "Forward passes per 90": 0.10,  
            "Accurate passes, %": 0.10, "xA per 90": 0.10, "Accurate through passes, %": 0.08, "Passes per 90": 0.08,
            "Ball recoveries per 90": 0.07, "PAdj Interceptions": 0.07, 
            "Successful dribbles, %": 0.06, "Accelerations per 90": 0.05,
            "Successful defensive actions per 90": 0.04, "Defensive duels per 90": 0.04, "Touches in box per 90": 0.03, "xG per 90": 0.02, 
            "Progressive runs per 90": 0.02,"Shot assists per 90": 0.02
        },
        "description": "Dictates tempo with passing and vision",
        "color": "#D32F2F"
    },
    
    "Box-to-Box Holding Midfielder (Hybrid 6/8)": {
        "metrics": {
            "high": ["Progressive passes per 90", "Defensive duels per 90", "Ball recoveries per 90", "Accurate passes, %",
                    "Progressive runs per 90", "Successful dribbles, %", "Accelerations per 90", "xG per 90"],
            "medium": ["Forward passes per 90", "Shot assists per 90",  
                      "xA per 90", "Accurate through passes, %", "Passes per 90", "PAdj Interceptions", 
                      "Successful defensive actions per 90", "Touches in box per 90"],
            "low": []
        },
        "weights": {
            "Progressive passes per 90": 0.09, "Defensive duels per 90": 0.08, "Ball recoveries per 90": 0.08, "Accurate passes, %": 0.08,
            "Progressive runs per 90": 0.08, "Successful dribbles, %": 0.07, "Accelerations per 90": 0.07, "xG per 90": 0.07,
            "Forward passes per 90": 0.06, "Shot assists per 90": 0.05,  
            "xA per 90": 0.05, "Accurate through passes, %": 0.05, "Passes per 90": 0.05, "PAdj Interceptions": 0.05, 
            "Successful defensive actions per 90": 0.04, "Touches in box per 90": 0.03
        },
        "description": "Energetic, mobile link between defense and attack",
        "color": "#FFC107"
    },
    
    "Destroyer": {
        "metrics": {
            "high": ["Defensive duels per 90", "Ball recoveries per 90", "PAdj Interceptions", 
                    "Defensive duels won, %", "Passes per 90", "Aerial duels won, %", 
                    "Successful defensive actions per 90"],
            "medium": ["Accurate passes, %", "Progressive passes per 90", "Progressive runs per 90", 
                      "Successful dribbles, %", "Accelerations per 90"],
            "low": ["Touches in box per 90", "Shot assists per 90"]
        },
        "weights": {
            "Defensive duels per 90": 0.13, "Ball recoveries per 90": 0.12, "PAdj Interceptions": 0.11, 
            "Defensive duels won, %": 0.10, "Passes per 90": 0.08, "Aerial duels won, %": 0.08, 
            "Successful defensive actions per 90": 0.08,
            "Accurate passes, %": 0.06, "Progressive passes per 90": 0.06, "Progressive runs per 90": 0.05, 
            "Successful dribbles, %": 0.05, "Accelerations per 90": 0.04,
            "Touches in box per 90": 0.02, "Shot assists per 90": 0.02
        },
        "description": "Aggressive ball winner in deeper areas. Out-of-possession enforcer focused on duels and regaining control",
        "color": "#2E7D32"
    },
    
    "Defensive-Anchor": {
        "metrics": {
            "high": ["Defensive duels per 90", "Ball recoveries per 90", "PAdj Interceptions", 
                    "Defensive duels won, %", "Aerial duels won, %", "Successful defensive actions per 90"],
            "medium": ["Passes per 90", "Accurate passes, %"],
            "low": ["Progressive passes per 90", "Touches in box per 90", "Shot assists per 90", 
                   "Progressive runs per 90", "Successful dribbles, %", "Accelerations per 90"]
        },
        "weights": {
            "Defensive duels per 90": 0.15, "Ball recoveries per 90": 0.13, "PAdj Interceptions": 0.13, 
            "Defensive duels won, %": 0.12, "Aerial duels won, %": 0.10, "Successful defensive actions per 90": 0.10,
            "Passes per 90": 0.07, "Accurate passes, %": 0.07,
            "Progressive passes per 90": 0.04, "Touches in box per 90": 0.03, "Shot assists per 90": 0.02, 
            "Progressive runs per 90": 0.02, "Successful dribbles, %": 0.01, "Accelerations per 90": 0.01
        },
        "description": "Pure shield in front of defense and positionally discipline; try to recover via interceptions and blocks",
        "color": "#0288D1"
    },
   
    "Organizer (Tempo Controller)": {
        "metrics": {
            "high": ["Passes per 90", "Accurate passes, %", "Progressive passes per 90", "Forward passes per 90",
                    "Ball recoveries per 90", "PAdj Interceptions"],
            "medium": ["xA per 90", "Accurate through passes, %", "Successful dribbles, %", 
                      "Accelerations per 90", "Progressive runs per 90"],
            "low": ["Defensive duels per 90", "Successful defensive actions per 90", "xG per 90", 
                   "Touches in box per 90", "Shot assists per 90"]
        },
        "weights": {
            "Passes per 90": 0.12, "Accurate passes, %": 0.12, "Progressive passes per 90": 0.11, "Forward passes per 90": 0.10,
            "Ball recoveries per 90": 0.09, "PAdj Interceptions": 0.08,
            "xA per 90": 0.07, "Accurate through passes, %": 0.06, "Successful dribbles, %": 0.05, 
            "Accelerations per 90": 0.05, "Progressive runs per 90": 0.05,
            "Defensive duels per 90": 0.03, "Successful defensive actions per 90": 0.03, "xG per 90": 0.02, 
            "Touches in box per 90": 0.01, "Shot assists per 90": 0.01
        },
        "description": "Controls tempo and organizes play from deep positions",
        "color": "#9C27B0"
    },
    
    "Connector (Link Play Facilitator)": {
        "metrics": {
            "high": ["Progressive passes per 90", "xA per 90", "Accurate through passes, %", "Shot assists per 90",
                    "Progressive runs per 90", "Successful dribbles, %", "Accelerations per 90"],
            "medium": ["Passes per 90", "Accurate passes, %", "Forward passes per 90", "Ball recoveries per 90",
                      "PAdj Interceptions", "xG per 90", "Touches in box per 90"],
            "low": ["Defensive duels per 90", "Successful defensive actions per 90"]
        },
        "weights": {
            "Progressive passes per 90": 0.12, "xA per 90": 0.12, "Accurate through passes, %": 0.10, "Shot assists per 90": 0.10,
            "Progressive runs per 90": 0.09, "Successful dribbles, %": 0.08, "Accelerations per 90": 0.07,
            "Passes per 90": 0.06, "Accurate passes, %": 0.06, "Forward passes per 90": 0.05, "Ball recoveries per 90": 0.04,
            "PAdj Interceptions": 0.04, "xG per 90": 0.03, "Touches in box per 90": 0.02,
            "Defensive duels per 90": 0.01, "Successful defensive actions per 90": 0.01
        },
        "description": "Links play between midfield and attack with creative passing and carrying",
        "color": "#FF5722"
    },
    
    "Shuttlers": {
        "metrics": {
            "high": ["Ball recoveries per 90", "Progressive runs per 90", "Accelerations per 90", 
                    "Successful dribbles, %", "Progressive passes per 90"],
            "medium": ["Passes per 90", "Accurate passes, %", "Forward passes per 90", "PAdj Interceptions",
                      "Defensive duels per 90", "xA per 90", "Shot assists per 90"],
            "low": ["Successful defensive actions per 90", "xG per 90", "Touches in box per 90"]
        },
        "weights": {
            "Ball recoveries per 90": 0.13, "Progressive runs per 90": 0.13, "Accelerations per 90": 0.12, 
            "Successful dribbles, %": 0.10, "Progressive passes per 90": 0.10,
            "Passes per 90": 0.07, "Accurate passes, %": 0.07, "Forward passes per 90": 0.06, "PAdj Interceptions": 0.06,
            "Defensive duels per 90": 0.05, "xA per 90": 0.04, "Shot assists per 90": 0.04,
            "Successful defensive actions per 90": 0.01, "xG per 90": 0.01, "Touches in box per 90": 0.01
        },
        "description": "All-action engine covering large zones. Pressing, recovering, and carrying the ball from deep to attack",
        "color": "#795548"
    },
    
    "Sitters": {
        "metrics": {
            "high": ["PAdj Interceptions", "Ball recoveries per 90", "Successful defensive actions per 90",
                    "Defensive duels per 90", "Defensive duels won, %"],
            "medium": ["Passes per 90", "Accurate passes, %", "Progressive passes per 90",
                      "Aerial duels won, %"],
            "low": ["Progressive runs per 90", "Successful dribbles, %", "Accelerations per 90",
                   "xG per 90", "Touches in box per 90", "Shot assists per 90", "xA per 90"]
        },
        "weights": {
            "PAdj Interceptions": 0.15, "Ball recoveries per 90": 0.14, "Successful defensive actions per 90": 0.13,
            "Defensive duels per 90": 0.11, "Defensive duels won, %": 0.10,
            "Passes per 90": 0.07, "Accurate passes, %": 0.07, "Progressive passes per 90": 0.06,
            "Aerial duels won, %": 0.06,
            "Progressive runs per 90": 0.03, "Successful dribbles, %": 0.03, "Accelerations per 90": 0.02,
            "xG per 90": 0.01, "Touches in box per 90": 0.01, "Shot assists per 90": 0.01, "xA per 90": 0.00
        },
        "description": "Stays central to block attacks, maintains compact shape",
        "color": "#607D8B"
    }
}

# ==========================================
# CENTRAL MIDFIELDER (CMF) PROFILES
# Based on DMF profiles with adjusted weights for more attacking contribution
# ==========================================
CMF_PROFILES = {
    "Progressive Playmaker": {
        "metrics": {
            "high": ["Progressive passes per 90", "xA per 90", "Accurate through passes, %", "Shot assists per 90",
                    "Accurate passes, %", "Forward passes per 90"],
            "medium": ["Passes per 90", "Successful dribbles, %", "Progressive runs per 90",
                      "Ball recoveries per 90", "Accelerations per 90"],
            "low": ["Defensive duels per 90", "Successful defensive actions per 90", "Fouls per 90"]
        },
        "weights": {
            "Progressive passes per 90": 0.14, "xA per 90": 0.13, "Accurate through passes, %": 0.11, "Shot assists per 90": 0.10,
            "Accurate passes, %": 0.10, "Forward passes per 90": 0.09,
            "Passes per 90": 0.07, "Successful dribbles, %": 0.06, "Progressive runs per 90": 0.06,
            "Ball recoveries per 90": 0.05, "Accelerations per 90": 0.04,
            "Defensive duels per 90": 0.02, "Successful defensive actions per 90": 0.02, "Fouls per 90": 0.01
        },
        "description": "Creative force in midfield, dictates attacks with vision and passing range",
        "color": "#9C27B0"
    },
    
    "Complete Box-to-Box Midfielder": {
        "metrics": {
            "high": ["Progressive passes per 90", "Progressive runs per 90", "Ball recoveries per 90",
                    "Successful dribbles, %", "Defensive duels per 90", "xA per 90"],
            "medium": ["Accurate passes, %", "Shot assists per 90", "Touches in box per 90",
                      "Accelerations per 90", "PAdj Interceptions", "Successful defensive actions per 90"],
            "low": []
        },
        "weights": {
            "Progressive passes per 90": 0.11, "Progressive runs per 90": 0.11, "Ball recoveries per 90": 0.10,
            "Successful dribbles, %": 0.09, "Defensive duels per 90": 0.08, "xA per 90": 0.08,
            "Accurate passes, %": 0.07, "Shot assists per 90": 0.07, "Touches in box per 90": 0.06,
            "Accelerations per 90": 0.06, "PAdj Interceptions": 0.06, "Successful defensive actions per 90": 0.11
        },
        "description": "Dynamic all-rounder covering defensive and attacking phases with equal effectiveness",
        "color": "#FFC107"
    },
    
    "Possession Controller": {
        "metrics": {
            "high": ["Passes per 90", "Accurate passes, %", "Ball recoveries per 90",
                    "Progressive passes per 90", "Forward passes per 90"],
            "medium": ["PAdj Interceptions", "xA per 90", "Successful dribbles, %",
                      "Accelerations per 90", "Defensive duels per 90"],
            "low": ["Touches in box per 90", "Shot assists per 90", "Successful defensive actions per 90"]
        },
        "weights": {
            "Passes per 90": 0.14, "Accurate passes, %": 0.13, "Ball recoveries per 90": 0.11,
            "Progressive passes per 90": 0.11, "Forward passes per 90": 0.10,
            "PAdj Interceptions": 0.08, "xA per 90": 0.07, "Successful dribbles, %": 0.06,
            "Accelerations per 90": 0.05, "Defensive duels per 90": 0.05,
            "Touches in box per 90": 0.04, "Shot assists per 90": 0.03, "Successful defensive actions per 90": 0.03
        },
        "description": "Maintains team control through precise passing and intelligent positioning",
        "color": "#00897B"
    },
    
    "Attacking Midfielder": {
        "metrics": {
            "high": ["xA per 90", "Shot assists per 90", "Progressive runs per 90",
                    "Touches in box per 90", "Successful dribbles, %", "xG per 90"],
            "medium": ["Progressive passes per 90", "Accurate through passes, %", "Accelerations per 90",
                      "Offensive duels won, %", "Forward passes per 90"],
            "low": ["Defensive duels per 90", "Successful defensive actions per 90", "PAdj Interceptions"]
        },
        "weights": {
            "xA per 90": 0.15, "Shot assists per 90": 0.13, "Progressive runs per 90": 0.12,
            "Touches in box per 90": 0.11, "Successful dribbles, %": 0.10, "xG per 90": 0.09,
            "Progressive passes per 90": 0.07, "Accurate through passes, %": 0.06, "Accelerations per 90": 0.05,
            "Offensive duels won, %": 0.04, "Forward passes per 90": 0.04,
            "Defensive duels per 90": 0.02, "Successful defensive actions per 90": 0.01, "PAdj Interceptions": 0.01
        },
        "description": "Offensive-minded midfielder focused on creating and scoring chances",
        "color": "#E91E63"
    },
    
    "Destroyer": {
        "metrics": {
            "high": ["Defensive duels per 90", "Ball recoveries per 90", "PAdj Interceptions", 
                    "Defensive duels won, %", "Passes per 90", "Aerial duels won, %", 
                    "Successful defensive actions per 90"],
            "medium": ["Accurate passes, %", "Progressive passes per 90", "Progressive runs per 90", 
                      "Successful dribbles, %", "Accelerations per 90"],
            "low": ["Touches in box per 90", "Shot assists per 90"]
        },
        "weights": {
            "Defensive duels per 90": 0.13, "Ball recoveries per 90": 0.12, "PAdj Interceptions": 0.11, 
            "Defensive duels won, %": 0.10, "Passes per 90": 0.08, "Aerial duels won, %": 0.08, 
            "Successful defensive actions per 90": 0.08,
            "Accurate passes, %": 0.06, "Progressive passes per 90": 0.06, "Progressive runs per 90": 0.05, 
            "Successful dribbles, %": 0.05, "Accelerations per 90": 0.04,
            "Touches in box per 90": 0.02, "Shot assists per 90": 0.02
        },
        "description": "Aggressive ball winner in deeper areas. Out-of-possession enforcer focused on duels and regaining control",
        "color": "#2E7D32"
    },

    "Shuttlers": {
        "metrics": {
            "high": ["Ball recoveries per 90", "Progressive runs per 90", "Accelerations per 90", 
                    "Successful dribbles, %", "Progressive passes per 90"],
            "medium": ["Passes per 90", "Accurate passes, %", "Forward passes per 90", "PAdj Interceptions",
                      "Defensive duels per 90", "xA per 90", "Shot assists per 90"],
            "low": ["Successful defensive actions per 90", "xG per 90", "Touches in box per 90"]
        },
        "weights": {
            "Ball recoveries per 90": 0.13, "Progressive runs per 90": 0.13, "Accelerations per 90": 0.12, 
            "Successful dribbles, %": 0.10, "Progressive passes per 90": 0.10,
            "Passes per 90": 0.07, "Accurate passes, %": 0.07, "Forward passes per 90": 0.06, "PAdj Interceptions": 0.06,
            "Defensive duels per 90": 0.05, "xA per 90": 0.04, "Shot assists per 90": 0.04,
            "Successful defensive actions per 90": 0.01, "xG per 90": 0.01, "Touches in box per 90": 0.01
        },
        "description": "All-action engine covering large zones. Pressing, recovering, and carrying the ball from deep to attack",
        "color": "#795548"
    },
    
    "Sitters": {
        "metrics": {
            "high": ["PAdj Interceptions", "Ball recoveries per 90", "Successful defensive actions per 90",
                    "Defensive duels per 90", "Defensive duels won, %"],
            "medium": ["Passes per 90", "Accurate passes, %", "Progressive passes per 90",
                      "Aerial duels won, %"],
            "low": ["Progressive runs per 90", "Successful dribbles, %", "Accelerations per 90",
                   "xG per 90", "Touches in box per 90", "Shot assists per 90", "xA per 90"]
        },
        "weights": {
            "PAdj Interceptions": 0.15, "Ball recoveries per 90": 0.14, "Successful defensive actions per 90": 0.13,
            "Defensive duels per 90": 0.11, "Defensive duels won, %": 0.10,
            "Passes per 90": 0.07, "Accurate passes, %": 0.07, "Progressive passes per 90": 0.06,
            "Aerial duels won, %": 0.06,
            "Progressive runs per 90": 0.03, "Successful dribbles, %": 0.03, "Accelerations per 90": 0.02,
            "xG per 90": 0.01, "Touches in box per 90": 0.01, "Shot assists per 90": 0.01, "xA per 90": 0.00
        },
        "description": "Stays central to block attacks, maintains compact shape",
        "color": "#607D8B"
    }
}
