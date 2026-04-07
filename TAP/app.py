import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

from config import (
    BASE_PATH, INDEX_NAMES, INDEX_SHORT,
    METRIC_GROUPS, METRIC_NAMES, COLORS,
    OUTPUT_METRICS, OUTPUT_AGAINST_METRICS,
)
from src.data_processor import TAPDataPipeline
from src.tap_calculator import TAPMetricsCalculator, TAPIndexCalculator
from src.visualizations import (
    TAPRadarChart, TAPPizzaChart,
    TAPOutputRadar, TAPMetricPizza,
)
from src.insights_engine import TAPInsightsEngine
from src.utils import get_quadrant_explanation

# ═══════════════════════════════════════════════════════════════════════════
#  Page config
# ═══════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="TAP — Tactical Analysis Platform",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_custom_css():
    css_path = os.path.join("assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
#  Session state
# ═══════════════════════════════════════════════════════════════════════════
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = TAPDataPipeline(BASE_PATH)
    st.session_state.metrics_calc = TAPMetricsCalculator()
    st.session_state.index_calc = TAPIndexCalculator()
    st.session_state.insights = TAPInsightsEngine()


# ═══════════════════════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════════════════════
def main():
    load_custom_css()

    # Sidebar logo
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=140)

    st.sidebar.markdown(
        "<h2 style='text-align:center; margin-bottom:0;'>TAP Framework</h2>"
        "<p style='text-align:center; color:#90A4AE; font-size:0.8rem; margin-top:0;'>"
        "Tactical Analysis Platform</p>",
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    coaches = st.session_state.pipeline.discover_coaches()
    if not coaches:
        st.error(f"No coach folders found in {BASE_PATH}")
        return

    selected_coach = st.sidebar.selectbox("🎓 Select Coach", coaches)
    structure = st.session_state.pipeline.load_coach_structure(selected_coach)

    page = st.sidebar.radio(
        "📂 Navigation",
        ["Dashboard", "Performance Output", "Team Profile", "Tactical Outlook"],
    )

    if not structure['team_file']:
        st.warning(f"No team data found for {selected_coach}")
        return

    # ── Data processing ─────────────────────────────────────────────────
    team_raw = st.session_state.pipeline.load_excel_file(structure['team_file'])
    team_df, opp_df = st.session_state.metrics_calc.extract_team_opponent(team_raw)
    team_metrics = st.session_state.metrics_calc.calculate_component_metrics(team_df, opp_df)

    # Output metrics
    output_perf, output_against = st.session_state.metrics_calc.calculate_output_metrics(team_df, opp_df)

    # League data
    league_all_metrics = []
    league_team_names = []
    league_outputs = []
    league_against = []

    for l_file in structure['league_files']:
        l_name = os.path.basename(l_file).replace("Team Stats ", "").replace(".xlsx", "")
        league_team_names.append(l_name)
        l_raw = st.session_state.pipeline.load_excel_file(l_file)
        l_team, l_opp = st.session_state.metrics_calc.extract_team_opponent(l_raw)
        l_metrics = st.session_state.metrics_calc.calculate_component_metrics(l_team, l_opp)
        league_all_metrics.append(l_metrics.mean())
        l_out, l_ag = st.session_state.metrics_calc.calculate_output_metrics(l_team, l_opp)
        league_outputs.append(l_out)
        league_against.append(l_ag)

    league_metrics_df = pd.DataFrame(league_all_metrics, index=league_team_names)

    # Normalise & indices
    team_avg = team_metrics.mean()
    z_metrics = st.session_state.index_calc.normalize_league_relative(team_avg, league_metrics_df)
    team_indices = st.session_state.index_calc.calculate_indices(pd.DataFrame([z_metrics])).iloc[0]

    # League indices for every team
    league_z = st.session_state.index_calc.normalize_league_relative(league_metrics_df, league_metrics_df)
    league_indices_df = st.session_state.index_calc.calculate_indices(league_z)
    league_indices_df.index = league_team_names

    # Percentiles
    percentiles = st.session_state.index_calc.calculate_percentiles(team_indices, league_indices_df)

    # Sub-metrics for tree
    sub_metrics = st.session_state.metrics_calc.calculate_sub_metrics(team_df)

    # Team name
    team_name = os.path.basename(structure['team_file']).replace("Team Stats ", "").replace(".xlsx", "")

    # ── Routing ─────────────────────────────────────────────────────────
    if page == "Dashboard":
        render_dashboard(selected_coach, team_indices, percentiles,
                         league_indices_df, team_metrics, league_metrics_df, sub_metrics)
    elif page == "Performance Output":
        render_performance_output(selected_coach, output_perf, output_against,
                                  league_outputs, league_against, league_team_names)
    elif page == "Team Profile":
        render_team_profile(selected_coach, team_name, team_indices, league_indices_df)
    elif page == "Tactical Outlook":
        render_tactical_outlook(selected_coach, team_indices, percentiles,
                                 team_avg, league_metrics_df)


# ═══════════════════════════════════════════════════════════════════════════
#  Dashboard
# ═══════════════════════════════════════════════════════════════════════════
def render_dashboard(coach, indices, percentiles, league_indices,
                     team_metrics, league_metrics, sub_metrics):
    st.title(f"📊 Tactical Dashboard — {coach}")
    st.caption("Composite tactical profile against the league")

    # ── Index cards ─────────────────────────────────────────────────────
    cols = st.columns(5)
    for i, idx in enumerate(indices.index):
        pct = percentiles.get(idx, 50)
        delta_label = f"{pct:.0f}th pctl"
        delta_color = "normal" if pct >= 50 else "inverse"
        cols[i].metric(
            label=INDEX_SHORT.get(idx, idx),
            value=f"{indices[idx]:+.2f}",
            delta=delta_label,
            delta_color=delta_color,
        )

    st.divider()

    # ── Two-column: Pizza + Summary ─────────────────────────────────────
    col_chart, col_text = st.columns([3, 2])

    with col_chart:
        tab_pizza, tab_radar = st.tabs(["📉 Index Pizza", "📡 Radar"])
        with tab_pizza:
            pct_values = [percentiles.get(idx, 50) for idx in indices.index]
            fig_pizza = TAPPizzaChart.create_index_pizza(
                params=list(indices.index),
                values=pct_values,
                title=f"{coach} — League Percentiles",
            )
            st.pyplot(fig_pizza, use_container_width=True)

        with tab_radar:
            fig_radar = TAPRadarChart().create_single_radar(indices, coach)
            st.pyplot(fig_radar, use_container_width=True)

    with col_text:
        st.subheader("Executive Summary")
        summary = st.session_state.insights.generate_executive_summary(
            indices, coach, percentiles
        )
        st.markdown(summary)

        with st.expander("📖 Index Explanation Guide"):
            explanations = st.session_state.insights.index_explanations()
            for key, info in explanations.items():
                st.markdown(f"#### {info['emoji']} {key} — {info['name']}")
                st.markdown(f"**High:** {info['high']}")
                st.markdown(f"**Low:** {info['low']}")
                st.caption(f"Applicability: {info['applicability']}")
                st.divider()

    # ── Percentile bars ─────────────────────────────────────────────────
    st.divider()
    st.subheader("League Percentile Ranking")

    pct_colors = []
    for idx in indices.index:
        p = percentiles.get(idx, 50)
        if p >= 75:
            pct_colors.append(COLORS['accent_green'])
        elif p >= 40:
            pct_colors.append(COLORS['accent_orange'])
        else:
            pct_colors.append(COLORS['accent_red'])

    fig_bar = go.Figure(go.Bar(
        x=[percentiles.get(idx, 50) for idx in indices.index],
        y=[f"{idx} — {INDEX_NAMES[idx]}" for idx in indices.index],
        orientation='h',
        marker=dict(color=pct_colors, line=dict(width=0)),
        text=[f"{percentiles.get(idx, 50):.0f}%" for idx in indices.index],
        textposition='auto',
        textfont=dict(color='white', size=14, family='Inter'),
    ))
    fig_bar.update_layout(
        xaxis=dict(title="Percentile (%)", range=[0, 100],
                   gridcolor='rgba(255,255,255,0.05)', color='#90A4AE'),
        yaxis=dict(autorange="reversed", color='#ECEFF1'),
        margin=dict(l=20, r=40, t=10, b=40),
        height=320,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ECEFF1', family='Inter'),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # ── Metric tree ─────────────────────────────────────────────────────
    st.divider()
    st.subheader("📂 Metric Tree Breakdown")
    render_metric_tree(team_metrics, league_metrics, sub_metrics)


# ═══════════════════════════════════════════════════════════════════════════
#  Performance Output (NEW)
# ═══════════════════════════════════════════════════════════════════════════
def render_performance_output(coach, output_perf, output_against,
                               league_outputs, league_against, league_names):
    st.title(f"⚽ Performance Output — {coach}")
    st.caption("Team output production vs what opponents produce against you")

    # Compute league maxes for scaling
    if league_outputs:
        out_df = pd.DataFrame(league_outputs)
        league_out_max = out_df.max().to_dict()
    else:
        league_out_max = None

    if league_against:
        ag_df = pd.DataFrame(league_against)
        league_ag_max = ag_df.max().to_dict()
    else:
        league_ag_max = None

    viz = TAPOutputRadar()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🟢 Team Output")
        fig_out = viz.create_output_radar(
            output_perf,
            league_maxes=league_out_max,
            title=f"{coach} — Attacking Output",
        )
        st.pyplot(fig_out, use_container_width=True)

    with col2:
        st.subheader("🔴 Output Against")
        fig_ag = viz.create_output_against_radar(
            output_against,
            league_maxes=league_ag_max,
            title=f"{coach} — Conceded / Defensive",
        )
        st.pyplot(fig_ag, use_container_width=True)

    # ── Raw numbers table ───────────────────────────────────────────────
    st.divider()
    st.subheader("📊 Raw Averages per Match")

    tab_out, tab_ag = st.tabs(["Output", "Output Against"])

    with tab_out:
        out_display = {OUTPUT_METRICS.get(k, k): v for k, v in output_perf.items()}
        df_out = pd.DataFrame.from_dict(out_display, orient='index', columns=['Avg / Match'])
        st.dataframe(df_out.style.format("{:.2f}").background_gradient(
            cmap='Blues', axis=0), use_container_width=True)

    with tab_ag:
        ag_display = {OUTPUT_AGAINST_METRICS.get(k, k): v for k, v in output_against.items()}
        df_ag = pd.DataFrame.from_dict(ag_display, orient='index', columns=['Avg / Match'])
        st.dataframe(df_ag.style.format("{:.2f}").background_gradient(
            cmap='Reds', axis=0), use_container_width=True)

    # ── Output insight ──────────────────────────────────────────────────
    st.divider()
    st.subheader("📝 Output Insight")

    goals = output_perf.get('Goals', 0)
    xg = output_perf.get('xG', 0)
    conceded = output_against.get('ConcededGoals', 0)
    opp_xg = output_against.get('OppxG', 0)

    cols_i = st.columns(4)
    cols_i[0].metric("Goals / Match", f"{goals:.2f}")
    cols_i[1].metric("xG / Match", f"{xg:.2f}",
                     delta=f"{goals - xg:+.2f} vs xG")
    cols_i[2].metric("Conceded / Match", f"{conceded:.2f}")
    cols_i[3].metric("Opp xG / Match", f"{opp_xg:.2f}",
                     delta=f"{conceded - opp_xg:+.2f} vs Opp xG")

    if goals > xg:
        st.success("📈 **Over-performing xG** — the team is clinical, converting chances above expected rates.")
    elif goals < xg * 0.85:
        st.warning("📉 **Under-performing xG** — chance quality is there, but finishing or luck is lacking.")

    if conceded < opp_xg:
        st.success("🛡️ **Defensive over-performance** — conceding fewer goals than expected; strong goalkeeping or defensive blocks.")
    elif conceded > opp_xg * 1.15:
        st.warning("⚠️ **Defensive under-performance** — conceding more than expected; check set-piece and transition vulnerabilities.")


# ═══════════════════════════════════════════════════════════════════════════
#  Metric Tree
# ═══════════════════════════════════════════════════════════════════════════
def render_metric_tree(team_metrics, league_metrics, sub_metrics):
    team_avg = team_metrics.mean()
    league_avg = league_metrics.mean()

    for group, metrics_list in METRIC_GROUPS.items():
        with st.expander(f"{INDEX_NAMES[group]} — Components", expanded=(group == 'IGC')):
            for m in metrics_list:
                t_val = team_avg.get(m, np.nan)
                l_val = league_avg.get(m, np.nan)

                if pd.isna(t_val) or pd.isna(l_val) or l_val == 0:
                    diff = 0
                else:
                    diff = (t_val - l_val) / abs(l_val)

                if diff > 0.1:
                    color, icon = COLORS['accent_green'], "▲"
                elif diff < -0.1:
                    color, icon = COLORS['accent_red'], "▼"
                else:
                    color, icon = COLORS['accent_orange'], "●"

                full_name = METRIC_NAMES.get(m, m)
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"**{full_name}**")
                c2.markdown(
                    f"<span style='color:{color}; font-weight:700;'>{t_val:.2f} {icon}</span>",
                    unsafe_allow_html=True,
                )
                c3.caption(f"League: {l_val:.2f}" if not pd.isna(l_val) else "—")

                # Sub-metric breakdown
                if m in sub_metrics and sub_metrics[m]:
                    sub_cols = st.columns(len(sub_metrics[m]) + 1)
                    sub_cols[0].markdown("&nbsp;&nbsp;└─")
                    for i, (sk, sv) in enumerate(sub_metrics[m].items()):
                        sub_cols[i + 1].caption(f"{sk}: {sv:.2f}")


# ═══════════════════════════════════════════════════════════════════════════
#  Team Profile (scatter landscape)
# ═══════════════════════════════════════════════════════════════════════════
def render_team_profile(coach, team_name, indices, league_indices_df):
    st.title("🗺️ Tactical Landscape")
    st.caption("Position your team against the league across any two indices")

    col_main, col_side = st.columns([3, 1])

    with col_main:
        display_map = {f"{k} — {v}": k for k, v in INDEX_NAMES.items()}
        display_keys = list(display_map.keys())
        x_choice = st.selectbox("X Axis", display_keys, index=0)
        y_choice = st.selectbox("Y Axis", display_keys, index=1)

        x_axis = display_map[x_choice]
        y_axis = display_map[y_choice]

        df_plot = league_indices_df.copy()
        df_plot['Team'] = df_plot.index
        df_plot['IsFocus'] = df_plot['Team'] == team_name
        df_plot = df_plot.sort_values('IsFocus')

        fig = px.scatter(
            df_plot, x=x_axis, y=y_axis, hover_name='Team',
            color='IsFocus',
            color_discrete_map={True: COLORS['accent_cyan'], False: '#555555'},
            title=f"League Landscape: {x_axis} vs {y_axis}",
        )

        focus_data = df_plot[df_plot['IsFocus']]
        if not focus_data.empty:
            row = focus_data.iloc[0]
            fig.add_annotation(
                x=row[x_axis], y=row[y_axis],
                text=f"<b>{coach}</b>",
                showarrow=True, arrowhead=2, ax=0, ay=-40,
                bgcolor=COLORS['bg_card'],
                bordercolor=COLORS['accent_cyan'],
                borderwidth=2, borderpad=4,
                font=dict(size=12, color=COLORS['accent_cyan']),
                opacity=0.95,
            )

        fig.add_hline(y=0, line_dash="dash", line_color="#333", opacity=0.6)
        fig.add_vline(x=0, line_dash="dash", line_color="#333", opacity=0.6)

        fig.update_layout(
            height=620, showlegend=False,
            margin=dict(l=20, r=20, t=60, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#ECEFF1', family='Inter'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='#333'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', zerolinecolor='#333'),
        )
        fig.update_traces(marker=dict(size=13, line=dict(width=1, color='#222')))
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.subheader("Quadrant Analysis")
        explanations = get_quadrant_explanation(x_axis, y_axis)
        team_x = indices[x_axis]
        team_y = indices[y_axis]
        q_key = f"{'H' if team_x >= 0 else 'L'}{'H' if team_y >= 0 else 'L'}"

        st.info(f"**Current Position: {q_key}**")
        st.write(explanations.get(q_key, "Tactical archetype insight for this combination."))
        st.divider()
        st.markdown("### Quadrant Guide")
        for k, v in explanations.items():
            st.markdown(f"**{k}**: {v}")

    # ── Comparison radar ────────────────────────────────────────────────
    st.divider()
    st.subheader("📡 Compare with League Team")
    compare_team = st.selectbox("Select comparison team", league_indices_df.index.tolist())

    if compare_team:
        ref_indices = league_indices_df.loc[compare_team]
        fig_cmp = TAPRadarChart().create_comparison_radar(
            indices, ref_indices, coach, compare_team
        )
        st.pyplot(fig_cmp, use_container_width=True)


# ═══════════════════════════════════════════════════════════════════════════
#  Tactical Outlook
# ═══════════════════════════════════════════════════════════════════════════
def render_tactical_outlook(coach, indices, percentiles, team_avg, league_metrics_df):
    st.title(f"🧠 Tactical Outlook — {coach}")

    # Tactical recommendations
    outlook = st.session_state.insights.generate_tactical_outlook(indices, coach)
    st.markdown(outlook)

    st.divider()

    # ── Per-index deep dive ─────────────────────────────────────────────
    st.subheader("🔍 Index Deep Dive")

    for idx_key, components in METRIC_GROUPS.items():
        with st.expander(f"{INDEX_NAMES[idx_key]}", expanded=False):
            # Calculate component percentiles
            comp_pcts = {}
            for m in components:
                t_val = team_avg.get(m, np.nan)
                if pd.isna(t_val) or m not in league_metrics_df.columns:
                    comp_pcts[METRIC_NAMES.get(m, m)] = 50
                else:
                    pct = (league_metrics_df[m] < t_val).mean() * 100
                    comp_pcts[METRIC_NAMES.get(m, m)] = round(pct, 0)

            col_text, col_chart = st.columns([2, 1])

            with col_text:
                insight_md = st.session_state.insights.generate_index_deep_insight(
                    idx_key,
                    indices[idx_key],
                    percentiles.get(idx_key, 50),
                    comp_pcts,
                )
                st.markdown(insight_md)

            with col_chart:
                fig_bp = TAPMetricPizza.create_breakdown_pizza(
                    params=list(comp_pcts.keys()),
                    percentiles=list(comp_pcts.values()),
                    index_name=idx_key,
                )
                st.pyplot(fig_bp, use_container_width=True)

    # ── Index meanings reference ────────────────────────────────────────
    st.divider()
    st.subheader("📖 Index Meanings Reference")
    explanations = st.session_state.insights.index_explanations()
    for key, info in explanations.items():
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.markdown(f"### {info['emoji']} {key}")
            c1.caption(info['name'])
            with c2:
                st.markdown(f"**High {key}:** {info['high']}")
                st.markdown(f"**Low {key}:** {info['low']}")
                st.info(f"**Relevance:** {info['applicability']}")
            st.divider()


# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()
