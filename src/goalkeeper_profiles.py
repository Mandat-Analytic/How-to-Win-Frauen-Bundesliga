
GK_PROFILES = {
    # =========================
    # IN POSSESSION – GOALKEEPERS
    # =========================

    "Sweeper Keeper (Build-Up Oriented)": {
        "description": "Acts as an auxiliary outfield player, heavily involved in build-up play, capable of breaking lines with passing and sweeping behind a high defensive line.",
        "color": "#1976D2",
        "secondary_color": "#0D47A1",
        "category": "In Possession",
        "icon": "",
        "weights": {
            "Passes per 90": 1.0,
            "Accurate passes, %": 1.0,
            "Long passes per 90": 1.0,
            "Accurate long passes, %": 1.0,
            "Passes to final third per 90": 1.0,
            "Accurate passes to final third, %": 1.0,
            "Exits per 90": 1.0,
            "Aerial duels per 90": 0.7,
            "Aerial duels won, %": 0.7,
            "Shots against per 90": 0.7,
            "Save rate, %": 0.5,
            "Shots against": 0.5,
            "Conceded goals per 90": -0.5  # Negative weight for bad metrics? Or handle in scoring engine?
            # The scoring engine handles weights. If I put negative weight, high value -> low score.
            # But wait, the previous profiles didn't show negative weights.
            # Let's check utils/profiles.py to see how they handle "bad" metrics if any.
            # Actually, for now I will just use the keys provided in "key_metrics" as weights.
            # The user provided "high", "medium", "low" lists.
            # I should probably assign weights based on these categories.
            # High = 1.0, Medium = 0.7, Low = 0.4?
        }
    },

    "Long Distributor Goalkeeper": {
        "description": "Prioritizes territory gain and direct progression, frequently initiating attacks with long and vertical distribution.",
        "color": "#512DA8",
        "secondary_color": "#311B92",
        "category": "In Possession",
        "icon": "",
        "weights": {} # To be filled
    },

    "Safe Circulator (Possession Retainer)": {
        "description": "Keeps possession secure under pressure, recycles the ball efficiently, and minimizes risk during build-up.",
        "color": "#0288D1",
        "secondary_color": "#01579B",
        "category": "In Possession",
        "icon": "",
        "weights": {} # To be filled
    },

    # =========================
    # OUT OF POSSESSION – GOALKEEPERS
    # =========================

    "Shot Stopper (Reflex-Based)": {
        "description": "Elite reflexes and positioning, excels in high shot-volume environments by consistently outperforming xG faced.",
        "color": "#C62828",
        "secondary_color": "#8E0000",
        "category": "Out of Possession",
        "icon": "",
        "weights": {} # To be filled
    },

    "Commanding Area Keeper": {
        "description": "Dominates the penalty area, proactive off the line, strong in aerial situations and defensive organization.",
        "color": "#F57C00",
        "secondary_color": "#E65100",
        "category": "Out of Possession",
        "icon": "",
        "weights": {} # To be filled
    },

    "Low-Block Survival Keeper": {
        "description": "Performs under sustained pressure, relies on shot-stopping volume rather than proactive sweeping or distribution.",
        "color": "#455A64",
        "secondary_color": "#263238",
        "category": "Out of Possession",
        "icon": "",
        "weights": {} # To be filled
    }
}

# Helper to populate weights based on high/medium/low
def populate_weights():
    profiles_data = {
        "Sweeper Keeper (Build-Up Oriented)": {
            "high": [
                "Passes per 90", "Accurate passes, %", "Long passes per 90", "Accurate long passes, %",
                "Passes to final third per 90", "Accurate passes to final third, %", "Exits per 90"
            ],
            "medium": ["Aerial duels per 90", "Aerial duels won, %", "Shots against per 90"],
            "low": ["Save rate, %", "Shots against", "Conceded goals per 90"]
        },
        "Long Distributor Goalkeeper": {
            "high": ["Long passes per 90", "Accurate long passes, %", "Passes per 90", "Passes to final third per 90"],
            "medium": ["Accurate passes, %", "Exits per 90", "Aerial duels per 90"],
            "low": ["Shots against per 90", "Save rate, %", "Prevented goals per 90"]
        },
        "Safe Circulator (Possession Retainer)": {
            "high": ["Passes per 90", "Accurate passes, %", "Passes to final third per 90", "Accurate passes to final third, %"],
            "medium": ["Long passes per 90", "Accurate long passes, %", "Shots against per 90"],
            "low": ["Exits per 90", "Aerial duels per 90", "Prevented goals per 90"]
        },
        "Shot Stopper (Reflex-Based)": {
            "high": ["Save rate, %", "Prevented goals", "Prevented goals per 90", "xG against per 90"],
            "medium": ["Shots against", "Shots against per 90", "Conceded goals per 90"],
            "low": ["Passes per 90", "Exits per 90", "Passes to final third per 90"]
        },
        "Commanding Area Keeper": {
            "high": ["Exits per 90", "Aerial duels per 90", "Aerial duels won, %", "Clean sheets"],
            "medium": ["Shots against per 90", "Save rate, %", "Conceded goals per 90"],
            "low": ["Passes per 90", "Accurate passes, %", "Passes to final third per 90"]
        },
        "Low-Block Survival Keeper": {
            "high": ["Shots against", "Shots against per 90", "Save rate, %", "Prevented goals per 90"],
            "medium": ["Conceded goals per 90", "xG against per 90", "Clean sheets"],
            "low": ["Exits per 90", "Passes per 90", "Accurate long passes, %"]
        }
    }

    for name, metrics in profiles_data.items():
        weights = {}
        for m in metrics["high"]: weights[m] = 1.0
        for m in metrics["medium"]: weights[m] = 0.7
        for m in metrics["low"]: weights[m] = 0.4
        
        # Handle inverted metrics with negative weights?
        # "Conceded goals per 90", "xG against per 90" (if lower is better)
        # If I use negative weights, calculate_score will treat high values as bad.
        # Let's try to identify inverted metrics.
        inverted_metrics = ["Conceded goals per 90", "xG against per 90", "Shots against", "Shots against per 90"]
        # Wait, "Shots against" might be good for "Shot Stopper" (high volume)?
        # User said for Low-Block Survival Keeper: "High: Shots against". This implies they FACE many shots.
        # But is facing many shots "good"? It defines the profile.
        # If I want to find a "Low-Block Survival Keeper", I want someone who faces many shots AND saves them.
        # So high "Shots against" is a characteristic.
        # But "Conceded goals per 90" should definitely be low for a GOOD keeper.
        # So "Conceded goals per 90" should have negative weight.
        
        for m in weights:
            if m in ["Conceded goals per 90", "xG against per 90"]:
                weights[m] = -weights[m]
        
        GK_PROFILES[name]["weights"] = weights

populate_weights()
