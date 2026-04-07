import matplotlib
matplotlib.use('Agg')    # non-interactive backend for Streamlit
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
import pandas as pd
from mplsoccer import Radar, PyPizza, FontManager
from typing import List, Dict, Optional, Tuple


# ── Colour helpers ──────────────────────────────────────────────────────────
_ACCENT   = '#4FC3F7'
_ACCENT2  = '#AB47BC'
_GREEN    = '#66BB6A'
_ORANGE   = '#FFA726'
_RED      = '#EF5350'
_DARK_BG  = '#0E1117'
_CARD_BG  = '#1A1E2E'


def _pct_color(pct: float) -> str:
    if pct >= 75:
        return _GREEN
    if pct >= 40:
        return _ORANGE
    return _RED


# ────────────────────────────────────────────────────────────────────────────
#  PyPizza — Index Overview
# ────────────────────────────────────────────────────────────────────────────
class TAPPizzaChart:
    """Create PyPizza charts for tactical index percentile profiles."""

    @staticmethod
    def create_index_pizza(params: List[str],
                           values: List[float],
                           title: str = '') -> plt.Figure:
        """
        PyPizza showing percentile values for 5 indices.
        `values` should be percentiles 0-100.
        """
        slice_colors = [_pct_color(v) for v in values]
        text_colors  = ['#FFFFFF'] * len(values)

        baker = PyPizza(
            params=params,
            background_color=_DARK_BG,
            straight_line_color='#333333',
            straight_line_lw=1,
            last_circle_color='#333333',
            last_circle_lw=1,
            other_circle_lw=0,
            inner_circle_size=20,
        )

        fig, ax = baker.make_pizza(
            values,
            figsize=(7, 7),
            color_blank_space='same',
            slice_colors=slice_colors,
            value_colors=text_colors,
            value_bck_colors=slice_colors,
            kwargs_slices=dict(edgecolor='#222222', zorder=2, linewidth=1.5, alpha=0.85),
            kwargs_params=dict(color='#ECEFF1', fontsize=12, weight='bold',
                               path_effects=[path_effects.withStroke(linewidth=2, foreground=_DARK_BG)]),
            kwargs_values=dict(color='#FFFFFF', fontsize=13, weight='bold',
                               bbox=dict(edgecolor='none', facecolor='none'),
                               path_effects=[path_effects.withStroke(linewidth=2, foreground=_DARK_BG)]),
        )

        if title:
            fig.suptitle(title, fontsize=16, color='#ECEFF1', weight='bold', y=0.98)

        fig.patch.set_facecolor(_DARK_BG)
        return fig


# ────────────────────────────────────────────────────────────────────────────
#  mplsoccer Radar — Index Radar
# ────────────────────────────────────────────────────────────────────────────
class TAPRadarChart:
    """Create mplsoccer Radar charts."""

    def __init__(self):
        self.params = ['IGC', 'IOB', 'IDI', 'IDO', 'ITS']

    def create_single_radar(self,
                            indices: pd.Series,
                            team_name: str,
                            low: float = -4.0,
                            high: float = 4.0) -> plt.Figure:
        """Radar chart for a single team's 5 indices."""
        mins = [low] * 5
        maxs = [high] * 5

        radar = Radar(params=self.params, min_range=mins, max_range=maxs,
                      round_int=[False] * 5, num_rings=6,
                      ring_width=1, center_circle_radius=1)

        fig, ax = radar.setup_axis(facecolor=_DARK_BG)
        fig.patch.set_facecolor(_DARK_BG)

        rings_inner = radar.draw_circles(ax=ax, facecolor=_CARD_BG,
                                         edgecolor='#333333', alpha=0.6)

        values = [float(indices.get(p, 0)) for p in self.params]
        radar_poly, rings, verts = radar.draw_radar(
            values, ax=ax,
            kwargs_radar={'facecolor': _ACCENT, 'alpha': 0.35,
                          'edgecolor': _ACCENT, 'lw': 2.5},
            kwargs_rings={'facecolor': _ACCENT, 'alpha': 0.08}
        )

        radar.draw_range_labels(ax=ax, fontsize=8, color='#90A4AE')
        radar.draw_param_labels(ax=ax, fontsize=13, color='#ECEFF1', weight='bold')

        ax.set_title(f'{team_name}', fontsize=15, color=_ACCENT, weight='bold', pad=15)
        return fig

    def create_comparison_radar(self,
                                team_indices: pd.Series,
                                reference_indices: pd.Series,
                                team_name: str,
                                reference_name: str,
                                low: float = -4.0,
                                high: float = 4.0) -> plt.Figure:
        """Overlapping radar for two teams."""
        mins = [low] * 5
        maxs = [high] * 5
        radar = Radar(params=self.params, min_range=mins, max_range=maxs,
                      round_int=[False] * 5, num_rings=6,
                      ring_width=1, center_circle_radius=1)

        fig, ax = radar.setup_axis(facecolor=_DARK_BG)
        fig.patch.set_facecolor(_DARK_BG)
        radar.draw_circles(ax=ax, facecolor=_CARD_BG, edgecolor='#333333', alpha=0.5)

        v1 = [float(team_indices.get(p, 0)) for p in self.params]
        v2 = [float(reference_indices.get(p, 0)) for p in self.params]

        radar.draw_radar_compare(v1, v2, ax=ax,
                                 kwargs_radar={'facecolor': _ACCENT, 'alpha': 0.3},
                                 kwargs_compare={'facecolor': _ACCENT2, 'alpha': 0.3})

        radar.draw_range_labels(ax=ax, fontsize=8, color='#90A4AE')
        radar.draw_param_labels(ax=ax, fontsize=12, color='#ECEFF1', weight='bold')

        # Legend
        ax.legend([team_name, reference_name], loc='upper right',
                  fontsize=10, facecolor=_CARD_BG, edgecolor='#333',
                  labelcolor='#ECEFF1')

        return fig


# ────────────────────────────────────────────────────────────────────────────
#  Output / Output-Against Radar Charts
# ────────────────────────────────────────────────────────────────────────────
class TAPOutputRadar:
    """Radar charts for team output and output-against performance."""

    @staticmethod
    def _build_radar(params: List[str],
                     values: List[float],
                     title: str,
                     color: str = _ACCENT,
                     mins: Optional[List[float]] = None,
                     maxs: Optional[List[float]] = None) -> plt.Figure:
        n = len(params)
        if mins is None:
            mins = [0.0] * n
        if maxs is None:
            maxs = [max(v * 1.5, 1.0) for v in values]

        # Ensure max > min
        for i in range(n):
            if maxs[i] <= mins[i]:
                maxs[i] = mins[i] + 1.0

        radar = Radar(params=params, min_range=mins, max_range=maxs,
                      round_int=[False] * n, num_rings=4,
                      ring_width=1, center_circle_radius=1)

        fig, ax = radar.setup_axis(facecolor=_DARK_BG)
        fig.patch.set_facecolor(_DARK_BG)
        radar.draw_circles(ax=ax, facecolor=_CARD_BG, edgecolor='#333333', alpha=0.5)

        radar.draw_radar(
            values, ax=ax,
            kwargs_radar={'facecolor': color, 'alpha': 0.35,
                          'edgecolor': color, 'lw': 2},
            kwargs_rings={'facecolor': color, 'alpha': 0.06}
        )

        radar.draw_range_labels(ax=ax, fontsize=7, color='#90A4AE')
        radar.draw_param_labels(ax=ax, fontsize=9, color='#ECEFF1', weight='bold')

        ax.set_title(title, fontsize=14, color=color, weight='bold', pad=12)
        return fig

    def create_output_radar(self,
                            output_metrics: Dict[str, float],
                            league_maxes: Optional[Dict[str, float]] = None,
                            title: str = 'Team Output') -> plt.Figure:
        params = list(output_metrics.keys())
        values = list(output_metrics.values())
        maxs = None
        if league_maxes:
            maxs = [league_maxes.get(p, v * 1.5) for p, v in zip(params, values)]
        return self._build_radar(params, values, title, color=_ACCENT, maxs=maxs)

    def create_output_against_radar(self,
                                    against_metrics: Dict[str, float],
                                    league_maxes: Optional[Dict[str, float]] = None,
                                    title: str = 'Output Against') -> plt.Figure:
        params = list(against_metrics.keys())
        values = list(against_metrics.values())
        maxs = None
        if league_maxes:
            maxs = [league_maxes.get(p, v * 1.5) for p, v in zip(params, values)]
        return self._build_radar(params, values, title, color=_RED, maxs=maxs)


# ────────────────────────────────────────────────────────────────────────────
#  Metric Breakdown PyPizza
# ────────────────────────────────────────────────────────────────────────────
class TAPMetricPizza:
    """PyPizza for component metrics within a single index."""

    @staticmethod
    def create_breakdown_pizza(params: List[str],
                               percentiles: List[float],
                               index_name: str) -> plt.Figure:
        slice_colors = [_pct_color(v) for v in percentiles]
        text_colors  = ['#FFFFFF'] * len(percentiles)

        baker = PyPizza(
            params=params,
            background_color=_DARK_BG,
            straight_line_color='#333333',
            straight_line_lw=1,
            last_circle_color='#333333',
            last_circle_lw=1,
            other_circle_lw=0,
            inner_circle_size=15,
        )

        fig, ax = baker.make_pizza(
            percentiles,
            figsize=(6, 6),
            color_blank_space='same',
            slice_colors=slice_colors,
            value_colors=text_colors,
            value_bck_colors=slice_colors,
            kwargs_slices=dict(edgecolor='#222222', zorder=2, linewidth=1, alpha=0.85),
            kwargs_params=dict(color='#ECEFF1', fontsize=9, weight='bold'),
            kwargs_values=dict(color='#FFFFFF', fontsize=10, weight='bold',
                               bbox=dict(edgecolor='none', facecolor='none')),
        )

        fig.suptitle(f'{index_name} — Component Breakdown',
                     fontsize=13, color='#ECEFF1', weight='bold', y=0.98)
        fig.patch.set_facecolor(_DARK_BG)
        return fig
