import math
import random
import time
import streamlit as st

# NEUTRALIZATION ARENA - Web edition
# Based on the original Tkinter program's chemical choices and calculation model.

BG = "#080d19"
PANEL = "#142036"
RED = "#ff4058"
BLUE = "#35baff"
GOLD = "#ffd34e"
WHITE = "#f5f7ff"
GRAY = "#9caec9"
NA = 6.02214076e23
KW = 1e-14

CHEMICALS = {
    "HCl": ("acid", 1, "Cl⁻"),
    "HNO3": ("acid", 1, "NO₃⁻"),
    "H2SO4": ("acid", 2, "SO₄²⁻"),
    "NaOH": ("base", 1, "Na⁺"),
    "KOH": ("base", 1, "K⁺"),
    "Ca(OH)2": ("base", 2, "Ca²⁺"),
    "Ba(OH)2": ("base", 2, "Ba²⁺"),
}

st.set_page_config(
    page_title="NEUTRALIZATION ARENA",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');
:root { color-scheme: dark; }
.stApp {
  background:
    radial-gradient(circle at 50% -15%, rgba(53,186,255,.13), transparent 38%),
    #080d19;
  color: #f5f7ff;
  font-family: 'Noto Sans KR', sans-serif;
}
.block-container { max-width: 1440px; padding-top: 1.4rem; padding-bottom: 2rem; }
h1, h2, h3, .orbitron { font-family: 'Orbitron', 'Noto Sans KR', sans-serif !important; }
.arena-title {
  text-align:center; color:#ffd34e; font-family:Orbitron,sans-serif;
  font-size:clamp(1.55rem,3vw,2.5rem); font-weight:800; letter-spacing:2px;
  text-shadow:0 0 18px rgba(255,211,78,.24); margin-bottom:0;
}
.arena-subtitle { text-align:center; color:#9caec9; letter-spacing:2px; font-size:.78rem; margin:4px 0 22px; }
.battle {
  position:relative; overflow:hidden; border:1px solid #263b5a; border-radius:14px;
  background:
    repeating-linear-gradient(125deg, transparent 0 38px, rgba(53,186,255,.06) 39px 40px),
    linear-gradient(135deg,#0c1628,#101c31);
  padding:20px 22px 16px; min-height:230px; box-shadow:0 12px 35px rgba(0,0,0,.22);
}
.round { text-align:center; color:#9caec9; font:700 .76rem Orbitron,sans-serif; letter-spacing:1.5px; }
.fighters { display:grid; grid-template-columns:1fr auto 1fr; align-items:center; gap:12px; margin-top:18px; }
.fighter { text-align:center; min-width:0; }
.chemical { font:800 clamp(1.5rem,3.5vw,2.4rem) Orbitron,sans-serif; overflow-wrap:anywhere; }
.acid { color:#ff4058; text-shadow:0 0 18px rgba(255,64,88,.22); }
.base { color:#35baff; text-shadow:0 0 18px rgba(53,186,255,.22); }
.role { font:700 .7rem Orbitron,sans-serif; letter-spacing:1.4px; margin-top:4px; }
.vs { color:#ffd34e; font:800 2rem Orbitron,sans-serif; }
.health-row { display:grid; grid-template-columns:1fr 1fr; gap:34px; margin:20px 2% 8px; }
.health-bg { height:18px; border-radius:99px; overflow:hidden; background:#301923; }
.health-bg.bluebg { background:#142d43; }
.health-fill { height:100%; border-radius:99px; transition:width .12s linear; }
.health-fill.redfill { background:linear-gradient(90deg,#ff4058,#ff8291); }
.health-fill.bluefill { background:linear-gradient(90deg,#35baff,#8cddff); float:right; }
.status { text-align:center; color:#f5f7ff; font:700 .9rem Orbitron,sans-serif; letter-spacing:1px; margin-top:12px; min-height:22px; }
.panel {
  background:linear-gradient(145deg,#172640,#111d31); border:1px solid #344765;
  border-radius:14px; padding:18px; height:100%;
}
.panel-title { font:700 1rem Orbitron,sans-serif; letter-spacing:1px; margin:0 0 14px; }
.result-panel { background:#0c1628; border:1px solid #263b5a; border-radius:10px; padding:16px; }
.winner { font:800 1.15rem Orbitron,sans-serif; margin:4px 0 14px; }
.metric { background:#101e33; border:1px solid #263b5a; border-radius:10px; padding:12px; margin-bottom:8px; }
.metric-label { color:#9caec9; font-size:.76rem; }
.metric-value { color:#f5f7ff; font:700 1.15rem Orbitron,sans-serif; margin-top:4px; }
.report { background:#0c1628; border:1px solid #263b5a; border-radius:10px; padding:14px; }
.footer { text-align:center; color:#71839f; font: .7rem Orbitron,sans-serif; letter-spacing:1px; margin-top:18px; }
div.stButton > button {
  width:100%; border:1px solid #ff4058; border-radius:9px; color:#fff;
  background:linear-gradient(90deg,#9f1728,#c52b40); font-family:Orbitron,sans-serif;
  font-weight:800; letter-spacing:1.2px; min-height:3.2rem;
  box-shadow:0 5px 18px rgba(185,28,45,.2);
}
div.stButton > button:hover { border-color:#ff8291; background:linear-gradient(90deg,#c52b40,#e13a52); color:#fff; }
[data-testid="stNumberInput"] label, [data-testid="stSelectbox"] label { color:#c8d4e8 !important; font-weight:700; }
[data-testid="stNumberInput"] input { background:#25344e !important; color:#f5f7ff !important; }
[data-testid="stSelectbox"] > div > div { background:#25344e !important; }
@media(max-width:700px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .battle { padding:16px 10px; }
  .health-row { gap:12px; }
  .role { font-size:.58rem; }
  .vs { font-size:1.35rem; }
}
</style>
""", unsafe_allow_html=True)

def fmt_num(number):
    if abs(number) < 1e-15:
        return "0"
    return f"{number:,.6g}"

def fmt_ion_count(number):
    if number == 0:
        return "0"
    exponent = math.floor(math.log10(abs(number)))
    coefficient = number / (10 ** exponent)
    return f"{coefficient:.2f} × 10^{exponent}"

def calculate(acid, base, ca, va, cb, vb):
    if not all(math.isfinite(x) and x > 0 for x in (ca, va, cb, vb)):
        raise ValueError("농도와 부피에는 0보다 큰 숫자를 입력해 주세요.")

    acid_mol = ca * va / 1000
    base_mol = cb * vb / 1000
    h = acid_mol * CHEMICALS[acid][1]
    oh = base_mol * CHEMICALS[base][1]
    reacted = min(h, oh)
    remain_h = max(0.0, h - oh)
    remain_oh = max(0.0, oh - h)
    volume = (va + vb) / 1000

    neutral = math.isclose(h, oh, rel_tol=1e-10, abs_tol=1e-15)
    if neutral:
        ph = 7.0
    else:
        excess = (h - oh) / volume
        if excess > 0:
            h_conc = (excess + math.sqrt(excess ** 2 + 4 * KW)) / 2
            ph = -math.log10(h_conc)
        else:
            oh_conc = (-excess + math.sqrt(excess ** 2 + 4 * KW)) / 2
            ph = 14 + math.log10(oh_conc)

    ions = {
        CHEMICALS[acid][2]: acid_mol,
        CHEMICALS[base][2]: base_mol,
    }
    if remain_h > 0:
        ions["H⁺"] = remain_h
    if remain_oh > 0:
        ions["OH⁻"] = remain_oh

    cations = sum(mol for ion, mol in ions.items() if ion.endswith("⁺"))
    anions = sum(mol for ion, mol in ions.items() if ion.endswith("⁻"))
    total = cations + anions

    if neutral:
        nature, winner, color = "중성", "중화 성공!", GOLD
    elif ph < 7:
        nature, winner, color = "산성", "산성 용액 승리!", RED
    else:
        nature, winner, color = "염기성", "염기성 용액 승리!", BLUE

    acid_ratio = max(0, min(1, remain_h / h if h > 0 else 0))
    base_ratio = max(0, min(1, remain_oh / oh if oh > 0 else 0))

    return {
        "acid": acid, "base": base, "h": h, "oh": oh, "reacted": reacted,
        "remain_h": remain_h, "remain_oh": remain_oh, "ions": ions,
        "cations": cations, "anions": anions, "total": total, "ph": ph,
        "nature": nature, "winner": winner, "color": color,
        "acid_ratio": acid_ratio, "base_ratio": base_ratio,
    }

st.markdown('<div class="arena-title">NEUTRALIZATION ARENA</div>', unsafe_allow_html=True)
st.markdown('<div class="arena-subtitle">CHEMICAL COMBAT SYSTEM // ACID VS BASE</div>', unsafe_allow_html=True)

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_inputs" not in st.session_state:
    st.session_state.last_inputs = ("HCl", "NaOH", 0.1, 50.0, 0.1, 50.0)

left, right = st.columns([1.65, 1], gap="large")

with left:
    acid_col, base_col = st.columns(2, gap="medium")
    with acid_col:
        st.markdown('<div class="panel"><div class="panel-title" style="color:#ff4058">ACID FIGHTER</div>', unsafe_allow_html=True)
        acid = st.selectbox("산 선택", ["HCl", "HNO3", "H2SO4"], key="acid")
        ca = st.number_input("농도 (mol/L)", min_value=0.000001, value=0.1, step=0.1, format="%.4f", key="acid_c")
        va = st.number_input("부피 (mL)", min_value=0.000001, value=50.0, step=5.0, format="%.2f", key="acid_v")
        st.markdown("</div>", unsafe_allow_html=True)
    with base_col:
        st.markdown('<div class="panel"><div class="panel-title" style="color:#35baff">BASE FIGHTER</div>', unsafe_allow_html=True)
        base = st.selectbox("염기 선택", ["NaOH", "KOH", "Ca(OH)2", "Ba(OH)2"], key="base")
        cb = st.number_input("농도 (mol/L)", min_value=0.000001, value=0.1, step=0.1, format="%.4f", key="base_c")
        vb = st.number_input("부피 (mL)", min_value=0.000001, value=50.0, step=5.0, format="%.2f", key="base_v")
        st.markdown("</div>", unsafe_allow_html=True)

    battle_slot = st.empty()
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    start = st.button("⚔  START BATTLE  ⚔", use_container_width=True)

    st.markdown('<div class="footer">25 °C | IDEAL STRONG ACID-BASE MODEL</div>', unsafe_allow_html=True)

    if start:
        try:
            data = calculate(acid, base, ca, va, cb, vb)
            st.session_state.last_result = data
            st.session_state.last_inputs = (acid, base, ca, va, cb, vb)
            progress_slot = st.empty()
            status_slot = st.empty()
            for frame in range(41):
                progress = frame / 40
                acid_current = 1 - progress * (1 - data["acid_ratio"])
                base_current = 1 - progress * (1 - data["base_ratio"])
                messages = ["ENERGY CHARGING...", "ION COLLISION!", "NEUTRALIZATION!", "FINAL IMPACT!"]
                message = messages[min(frame // 11, 3)]
                particles = "".join(
                    f'<i style="position:absolute;left:{random.randint(35,65)}%;top:{random.randint(28,72)}%;'
                    f'width:7px;height:7px;border-radius:50%;background:{random.choice([RED,BLUE,GOLD])};'
                    f'box-shadow:0 0 12px currentColor;opacity:.85"></i>'
                    for _ in range(5 if frame % 3 == 0 else 0)
                )
                battle_html = f"""
                <div class="battle">
                  <div class="round">ROUND 01 - NEUTRALIZATION</div>
                  <div class="fighters">
                    <div class="fighter"><div class="chemical acid">{acid}</div><div class="role acid">ACID FIGHTER</div></div>
                    <div class="vs">VS</div>
                    <div class="fighter"><div class="chemical base">{base}</div><div class="role base">BASE FIGHTER</div></div>
                  </div>
                  <div class="health-row">
                    <div class="health-bg"><div class="health-fill redfill" style="width:{acid_current*100:.2f}%"></div></div>
                    <div class="health-bg bluebg"><div class="health-fill bluefill" style="width:{base_current*100:.2f}%"></div></div>
                  </div>
                  <div class="status">{message}</div>{particles}
                </div>"""
                battle_slot.markdown(battle_html, unsafe_allow_html=True)
                status_slot.empty()
                time.sleep(0.045)
            st.session_state.last_result = data
        except (ValueError, OverflowError, ZeroDivisionError) as exc:
            st.error(str(exc))

    data = st.session_state.last_result
    if data is None:
        battle_slot.markdown("""
        <div class="battle">
          <div class="round">ROUND 01 - NEUTRALIZATION</div>
          <div class="fighters">
            <div class="fighter"><div class="chemical acid">HCl</div><div class="role acid">ACID FIGHTER</div></div>
            <div class="vs">VS</div>
            <div class="fighter"><div class="chemical base">NaOH</div><div class="role base">BASE FIGHTER</div></div>
          </div>
          <div class="health-row">
            <div class="health-bg"><div class="health-fill redfill" style="width:100%"></div></div>
            <div class="health-bg bluebg"><div class="health-fill bluefill" style="width:100%"></div></div>
          </div>
          <div class="status">READY TO BATTLE</div>
        </div>""", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="color:#ffd34e">전투 결과 보고서</div>', unsafe_allow_html=True)
    data = st.session_state.last_result
    if data is None:
        st.markdown('<div class="result-panel"><div class="winner" style="color:#ffd34e">전투 대기 중</div><p style="color:#9caec9">START BATTLE 버튼을 눌러 전투를 시작하세요.<br><br>화학 반응 계산 결과가 이곳에 표시됩니다.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="winner" style="color:{data["color"]}">{data["winner"]}</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f'<div class="metric"><div class="metric-label">최종 pH</div><div class="metric-value">{data["ph"]:.2f}</div></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric"><div class="metric-label">용액의 액성</div><div class="metric-value">{data["nature"]}</div></div>', unsafe_allow_html=True)

        report = []
        report.append("========== 전투 결과 보고서 ==========")
        report.append("")
        report.append("[ 중화 반응 분석 ]")
        report.append(f"반응한 H⁺ : {fmt_num(data['reacted'])} mol")
        report.append(f"반응한 OH⁻ : {fmt_num(data['reacted'])} mol")
        report.append(f"남은 H⁺ : {fmt_num(data['remain_h'])} mol")
        report.append(f"남은 OH⁻ : {fmt_num(data['remain_oh'])} mol")
        report.append("")
        report.append("-----------------------------------")
        report.append("[ 전체 이온 목록 ]")
        for ion, mol in data["ions"].items():
            report.extend([f"\n[{ion}]", f"  몰수 : {fmt_num(mol)} mol", f"  실제 개수 : {fmt_ion_count(mol * NA)} 개"])
        report.extend([
            "", "-----------------------------------", "[ 이온 개수 합계 ]",
            f"양이온 수 : {fmt_ion_count(data['cations'] * NA)} 개",
            f"음이온 수 : {fmt_ion_count(data['anions'] * NA)} 개",
            f"총 이온 수 : {fmt_ion_count(data['total'] * NA)} 개",
            "", "-----------------------------------", "[ 최종 용액 분석 ]",
            f"용액의 액성 : {data['nature']}", f"최종 pH : {data['ph']:.2f}",
            "", "===================================",
        ])
        st.code("\n".join(report), language=None)
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("※ 원본 프로그램의 강산·강염기 및 25 °C 이상 용액 모델을 웹 화면으로 옮겼습니다. 계산 결과는 입력값과 원본 모델의 가정에 따릅니다.")
