import pandas as pd
from typing import Dict, List


class TAPInsightsEngine:
    """Generate natural-language insights from TAP indices."""

    # ── Archetype classification ────────────────────────────────────────────
    def identify_archetype(self, indices: pd.Series) -> str:
        iob = indices.get('IOB', 0)
        idi = indices.get('IDI', 0)

        style = ('Possession-Based' if iob > 1
                 else 'Direct Play' if iob < -1
                 else 'Balanced')

        pressure = ('High Press' if idi > 1
                    else 'Low Block' if idi < -1
                    else 'Moderate Press')

        return f"{style} · {pressure}"

    # ── Index explanation cards ─────────────────────────────────────────────
    def index_explanations(self) -> Dict[str, Dict[str, str]]:
        return {
            'IGC': {
                'name': 'Squad Quality (Game Control)',
                'emoji': '🎯',
                'high': 'Superior squad quality — the team dictates tempo, dominates possession, and restricts opponent build-up. Pass accuracy and progressive passing are well above the league average.',
                'low': 'A quality deficit relative to the league — the team loses possession battles and concedes territorial control. Tactical discipline is needed to compensate.',
                'applicability': 'Benchmark for raw squad competitiveness. Teams with low IGC must over-perform tactically or rely on set-piece / transition moments.',
                'team_metrics': 'Pass Accuracy, Possession %, Avg Passes/Possession, Progressive Passes',
                'opp_metrics': 'Opponent Possession (suppression), Opponent PPDA (press resistance)',
            },
            'IOB': {
                'name': 'Offensive Behavior (Possessional vs Direct)',
                'emoji': '⚽',
                'high': 'Possession-oriented: favours positional attacks, patient build-up, and short passing sequences. The team dominates territory through sustained ball circulation.',
                'low': 'Direct & vertical: prioritises counterattacks, long balls, and rapid transitions behind the defensive line.',
                'applicability': 'Defines offensive identity — neither is inherently superior. A high IOB suits technical rosters; a low IOB suits athletic, pacey squads.',
                'team_metrics': 'Positional Attacks, Match Tempo, Back Passes',
                'opp_metrics': 'N/A — style indicator, not quality',
            },
            'IDI': {
                'name': 'Defensive Intensity',
                'emoji': '🔥',
                'high': 'Aggressive, high-press defence — wins the ball early, engages in frequent duels, and recovers high on the pitch. Physically demanding.',
                'low': 'Passive, deep-block defence — absorbs pressure, protects the box, and prioritises shape over ball-winning. Energy-conserving.',
                'applicability': 'Measures defensive energy expenditure and disruption capability. High IDI teams risk tiring late in matches; low IDI teams risk ceding territory.',
                'team_metrics': 'High Recoveries, PPDA (inv.), Defensive Duels Won, Sliding Tackles',
                'opp_metrics': 'Opponent Progressive Passes (suppression)',
            },
            'IDO': {
                'name': 'Defensive Organization',
                'emoji': '🏰',
                'high': 'Structurally sound: disciplined positional play, strong aerial presence, and effective at limiting opponent penetration. Difficult to break down.',
                'low': 'Structurally exposed: high volumes of opponent shots and entries into the penalty area indicate disorganisation or a deliberate high-line risk.',
                'applicability': 'Measures defensive reliability regardless of pressing intensity. A team can press aggressively (high IDI) but still be organised (high IDO) or not.',
                'team_metrics': 'Interceptions, Clearances, Total Recoveries, Aerial Duels Won',
                'opp_metrics': 'Opponent Shots on Target (suppression), Opponent Penalty Area Entries (suppression)',
            },
            'ITS': {
                'name': 'Transition Effectiveness',
                'emoji': '⚡',
                'high': 'Elite transition engine — converts defensive actions into attacking opportunities quickly and efficiently. Counter-attacks lead to shots.',
                'low': 'Methodical transition — prefers to secure possession before progressing, sacrificing speed for safety.',
                'applicability': 'The "lethality" gauge. Teams with high ITS and low IOB are classic counter-attacking units. High ITS + high IOB = total football.',
                'team_metrics': 'Counterattacks, Counter-attack Conversion %, Deep Completed Passes, Smart Passes',
                'opp_metrics': 'Opponent Recoveries (suppression — preventing quick opponent transitions)',
            },
        }

    # ── Executive summary ───────────────────────────────────────────────────
    def generate_executive_summary(self,
                                   indices: pd.Series,
                                   coach_name: str,
                                   percentiles: Dict[str, float] = None) -> str:
        archetype = self.identify_archetype(indices)

        md = f"### **{coach_name}** — *{archetype}*\n\n"

        # Quality insight
        if indices.get('IGC', 0) > 1:
            md += "🟢 **Squad quality is elite** — the team has the personnel to dominate possession and dictate games.\n\n"
        elif indices.get('IGC', 0) > 0:
            md += "🟡 **Squad quality is above average** — competitive in possession battles but not dominant.\n\n"
        else:
            md += "🔴 **Squad quality is below average** — success requires tactical discipline and efficient use of moments.\n\n"

        # Playstyle
        iob = indices.get('IOB', 0)
        if iob > 0.5:
            md += "The team employs a **possession-based** system, favouring positional attacks and patient build-up.\n\n"
        elif iob < -0.5:
            md += "The team is **direct and vertical**, seeking rapid transitions and counter-attacks rather than sustained possession.\n\n"
        else:
            md += "The team is **tactically flexible**, balancing possession phases with direct vertical opportunities.\n\n"

        # Defensive posture
        idi = indices.get('IDI', 0)
        ido = indices.get('IDO', 0)
        if idi > 0.5 and ido > 0.5:
            md += "Defensively, the team combines **aggressive pressing** with **strong structural organisation** — a complete defensive profile.\n\n"
        elif idi > 0.5:
            md += "The team **presses aggressively**, but structural organisation may leave gaps when the press is broken.\n\n"
        elif ido > 0.5:
            md += "Defensively **well-organised and disciplined**, though pressing intensity is moderate.\n\n"
        else:
            md += "Defensive phase is an **area for development** — both intensity and organisation are below average.\n\n"

        # Transition
        its = indices.get('ITS', 0)
        if its > 0.5:
            md += "⚡ **Transitions are a weapon** — the team converts turnovers into scoring opportunities effectively.\n\n"
        elif its < -0.5:
            md += "Transition play is **conservative** — ball security is prioritised over rapid vertical progression.\n\n"

        # Strengths / weaknesses
        strengths = indices.nlargest(2)
        weaknesses = indices.nsmallest(1)
        md += f"**Primary strengths:** {strengths.index[0]}, {strengths.index[1]}  \n"
        md += f"**Key area to develop:** {weaknesses.index[0]}\n"

        return md

    # ── Tactical outlook ────────────────────────────────────────────────────
    def generate_tactical_outlook(self, indices: pd.Series, coach_name: str) -> str:
        md = f"## Tactical Outlook & Recommendations — {coach_name}\n\n"

        # IGC
        igc = indices.get('IGC', 0)
        if igc > 1:
            md += "### 💎 Squad Quality Advantage\n"
            md += f"The elite IGC ({igc:+.2f}) provides the foundation for a **dominant** approach. The team should exploit creative freedom and high-risk attacking patterns.\n\n"
        elif igc < -1:
            md += "### ⚙️ Technical Gap — Tactical Compensation Required\n"
            md += f"The low IGC ({igc:+.2f}) indicates a **quality deficit**. Success hinges on maximising set-pieces, transitions, and extreme tactical discipline.\n\n"
        else:
            md += "### ⚖️ Competitive Squad Quality\n"
            md += f"IGC ({igc:+.2f}) is within the league norm — the team is **competitive** but must find marginal gains through tactical preparation.\n\n"

        # IOB
        iob = indices.get('IOB', 0)
        if iob > 0.5:
            md += "### ⚽ Possession Engine\n"
            md += "High IOB confirms a **patient, construction-based** attacking style. Key: ensure possession translates into threat through progressive passing and penalty-area entries.\n\n"
        elif iob < -0.5:
            md += "### ⚡ Vertical Identity\n"
            md += "Low IOB reflects **directness**. Key: ITS components must remain sharp so vertical play is faster than opponent recovery.\n\n"

        # IDI vs IDO
        idi = indices.get('IDI', 0)
        ido = indices.get('IDO', 0)
        if idi > ido + 0.5:
            md += "### 🛡️ Press-Dependent Defence\n"
            md += "IDI exceeds IDO — the team relies on **pressing intensity** over structural solidity. Risk: opponents who break the first press can expose gaps. Focus on **recovery speed** and secondary pressing triggers.\n\n"
        elif ido > idi + 0.5:
            md += "### 🏰 Structural Fortress\n"
            md += "IDO exceeds IDI — the team is **hard to break down** but potentially passive. Look for **pressing triggers** in specific match states to increase ball-recovery frequency.\n\n"
        else:
            md += "### 🔄 Balanced Defensive Profile\n"
            md += "IDI and IDO are balanced — the team maintains **reasonable intensity with adequate structure**. Fine-tuning pressing triggers and positional discipline will yield marginal defensive gains.\n\n"

        # ITS
        its = indices.get('ITS', 0)
        if its > 0.5:
            md += "### 🚀 Transition Weapon\n"
            md += "High ITS means the team is **lethal in transition** — quick counter-attacks convert into genuine scoring chances. Maintain deep-completion quality and smart-pass accuracy.\n\n"
        elif its < -0.5:
            md += "### 🐢 Transition Development Needed\n"
            md += "Low ITS suggests **cautious transitions** — consider targeted improvements in counter-attack conversion and deep ball progression.\n\n"

        return md

    # ── Per-index deep insight ──────────────────────────────────────────────
    def generate_index_deep_insight(self,
                                    index_key: str,
                                    index_value: float,
                                    percentile: float,
                                    component_pcts: Dict[str, float]) -> str:
        """Generate detailed narrative for one index."""
        info = self.index_explanations()[index_key]
        md = f"### {info['emoji']} {index_key} — {info['name']}\n\n"
        md += f"**Score:** {index_value:+.2f} &nbsp;&nbsp;|&nbsp;&nbsp; **League Percentile:** {percentile:.0f}%\n\n"

        if percentile >= 75:
            md += f"This places the team in the **top quartile** of the league for {info['name']}.\n\n"
        elif percentile >= 40:
            md += f"The team sits in the **middle band** for {info['name']} — neither a strength nor a weakness.\n\n"
        else:
            md += f"This is in the **lower quartile** — {info['name']} is an area for focused development.\n\n"

        # Component breakdown
        if component_pcts:
            md += "**Component Breakdown:**\n\n"
            md += "| Metric | Percentile |\n|--------|:-----------:|\n"
            for m, p in component_pcts.items():
                badge = '🟢' if p >= 75 else '🟡' if p >= 40 else '🔴'
                md += f"| {m} | {badge} {p:.0f}% |\n"
            md += "\n"

        # Metric source info
        md += f"**Team metrics used:** {info['team_metrics']}  \n"
        md += f"**Opponent metrics used:** {info['opp_metrics']}\n\n"

        return md

    # ── Matchup analysis ────────────────────────────────────────────────────
    def analyze_tactical_matchup(self,
                                 team_a_indices: pd.Series,
                                 team_b_indices: pd.Series) -> Dict:
        analysis = {}
        if team_a_indices['IOB'] > team_b_indices['IOB']:
            analysis['possession_battle'] = "Team A is expected to control the ball."
        else:
            analysis['possession_battle'] = "Team B is expected to control the ball."
        return analysis
