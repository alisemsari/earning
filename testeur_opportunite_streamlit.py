import streamlit as st

st.set_page_config(page_title="Testeur d'opportunité", page_icon="📈", layout="wide")

st.markdown("""
<style>
.metric-card{background:#eee;border:1px solid #bbb;border-radius:12px;padding:14px;text-align:center;min-height:110px;box-shadow:0 3px 8px #0002}
.metric-label{font-size:16px;font-weight:700;margin-bottom:12px}
.metric-value{background:#70b7f5;border-radius:5px;padding:12px;font-size:27px}
.result-ok{background:#d9f2df;color:#146c2e;border:2px solid #42a85a;border-radius:12px;padding:18px;text-align:center;font-size:25px;font-weight:800}
.result-no{background:#f7dddd;color:#9d1c1c;border:2px solid #d45b5b;border-radius:12px;padding:18px;text-align:center;font-size:25px;font-weight:800}
</style>
""", unsafe_allow_html=True)

st.title("📈 Testeur d'opportunité boursière")
st.caption("Entre les cinq variations. Les écarts et le résultat sont calculés automatiquement.")

st.subheader("1. Saisir les variations")
c1, c2, c3 = st.columns(3)
with c1:
    v_actuel = st.number_input("Variation Actuel (%)", value=20.0, step=0.5, format="%.2f")
    v5j = st.number_input("Variation 5 Derniers Jours (%)", value=30.0, step=0.5, format="%.2f")
with c2:
    v1m = st.number_input("Variation 1 Mois (%)", value=10.0, step=0.5, format="%.2f")
    v3m = st.number_input("Variation 3 Mois (%)", value=10.0, step=0.5, format="%.2f")
with c3:
    v1a = st.number_input("Variation 1 An (%)", value=20.0, step=0.5, format="%.2f")

# Calculs identiques aux colonnes d'écart Power BI
e_5j_1m = v5j - v1m
e_5j_1a = v5j - v1a

# Reproduction exacte de la logique DAX Opportunite 1
conditions_obligatoires = e_5j_1m >= -10 and v1m >= 0 and v_actuel > 10
regle_1 = v5j >= 30 and v1m >= 5 and v3m >= 5
regle_2 = e_5j_1m >= 10 and e_5j_1a >= 40
opportunite = conditions_obligatoires and (regle_1 or regle_2)

st.subheader("2. Écarts calculés automatiquement")
a, b = st.columns(2)
with a:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Ecart_5J_1M</div><div class="metric-value">{e_5j_1m:.2f} %</div></div>', unsafe_allow_html=True)
with b:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Ecart_5J_1A</div><div class="metric-value">{e_5j_1a:.2f} %</div></div>', unsafe_allow_html=True)

st.subheader("3. Résultat de l'algorithme")
if opportunite:
    st.markdown('<div class="result-ok">✓ OPPORTUNITÉ DÉTECTÉE</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="result-no">✕ NON RETENUE</div>', unsafe_allow_html=True)

with st.expander("Voir le détail des conditions"):
    st.write("**Conditions obligatoires**")
    st.write(f"{'✅' if e_5j_1m >= -10 else '❌'} Ecart_5J_1M ≥ -10 : {e_5j_1m:.2f}")
    st.write(f"{'✅' if v1m >= 0 else '❌'} Variation 1 Mois ≥ 0 : {v1m:.2f}")
    st.write(f"{'✅' if v_actuel > 10 else '❌'} Variation Actuel > 10 : {v_actuel:.2f}")
    st.write("**Règles reliées par OU**")
    st.write(f"{'✅' if regle_1 else '❌'} Règle 1 : V5J ≥ 30, V1M ≥ 5, V3M ≥ 5")
    st.write(f"{'✅' if regle_2 else '❌'} Règle 2 : Ecart_5J_1M ≥ 10 et Ecart_5J_1A ≥ 40")

st.caption("Les valeurs sont saisies en points de pourcentage : 23 signifie 23 %. Seuils et logique repris de DAX Opportunite 1.")
