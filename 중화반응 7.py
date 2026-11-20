
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

# =========================================
# NEUTRALIZATION ARENA
# =========================================

BG = "#080d19"
PANEL = "#142036"
RED = "#ff4058"
BLUE = "#35baff"
GOLD = "#ffd34e"
WHITE = "#f5f7ff"
GRAY = "#9caec9"

NA = 6.02214076e23
KW = 1e-14

# 종류, H+ 또는 OH- 계수, 구경꾼 이온
CHEMICALS = {
    "HCl": ("acid", 1, "Cl⁻"),
    "HNO3": ("acid", 1, "NO₃⁻"),
    "H2SO4": ("acid", 2, "SO₄²⁻"),
    "NaOH": ("base", 1, "Na⁺"),
    "KOH": ("base", 1, "K⁺"),
    "Ca(OH)2": ("base", 2, "Ca²⁺"),
    "Ba(OH)2": ("base", 2, "Ba²⁺")
}


# =========================================
# ROOT WINDOW
# =========================================

root = tk.Tk()
root.title("NEUTRALIZATION ARENA")
root.geometry("1280x850")
root.configure(bg=BG)
root.resizable(False, False)

main_container = tk.Frame(root, bg=BG)
main_container.pack(fill="both", expand=True)

# 왼쪽 전투 화면
left_panel = tk.Frame(
    main_container,
    bg=BG,
    width=850
)
left_panel.pack(side="left", fill="y")
left_panel.pack_propagate(False)

# 오른쪽 결과 화면
right_panel = tk.Frame(
    main_container,
    bg=BG,
    width=430
)
right_panel.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(0, 15),
    pady=15
)

acid_var = tk.StringVar(value="HCl")
base_var = tk.StringVar(value="NaOH")

acid_c = tk.StringVar(value="0.1")
acid_v = tk.StringVar(value="50")
base_c = tk.StringVar(value="0.1")
base_v = tk.StringVar(value="50")

busy = False
battle_data = None


# =========================================
# NUMBER FORMATTING
# =========================================

def format_number(number):
    if abs(number) < 1e-15:
        return "0"

    return f"{number:,.6g}"


def format_ion_count(number):
    if number == 0:
        return "0"

    exponent = math.floor(math.log10(abs(number)))
    coefficient = number / (10 ** exponent)

    return f"{coefficient:.2f} × 10^({exponent})"


# =========================================
# HEADER
# =========================================

tk.Label(
    left_panel,
    text="NEUTRALIZATION ARENA",
    font=("Arial", 26, "bold"),
    bg=BG,
    fg=GOLD
).pack(pady=(18, 3))

tk.Label(
    left_panel,
    text="CHEMICAL COMBAT SYSTEM // ACID VS BASE",
    font=("Arial", 10, "bold"),
    bg=BG,
    fg=GRAY
).pack()


# =========================================
# BATTLE SCREEN
# =========================================

canvas = tk.Canvas(
    left_panel,
    width=800,
    height=230,
    bg="#0c1628",
    highlightthickness=0
)
canvas.pack(pady=15)

# 배경 격자
for x in range(0, 850, 40):
    canvas.create_line(
        x, 0, x - 100, 230,
        fill="#17263e"
    )

canvas.create_text(
    400, 22,
    text="ROUND 01 - NEUTRALIZATION",
    fill=GRAY,
    font=("Arial", 11, "bold")
)

acid_name = canvas.create_text(
    180, 85,
    text="HCl",
    fill=RED,
    font=("Arial", 36, "bold")
)

base_name = canvas.create_text(
    620, 85,
    text="NaOH",
    fill=BLUE,
    font=("Arial", 36, "bold")
)

canvas.create_text(
    400, 85,
    text="VS",
    fill=GOLD,
    font=("Arial", 38, "bold")
)

canvas.create_text(
    180, 125,
    text="ACID FIGHTER",
    fill=RED,
    font=("Arial", 11, "bold")
)

canvas.create_text(
    620, 125,
    text="BASE FIGHTER",
    fill=BLUE,
    font=("Arial", 11, "bold")
)

# 체력바 배경
canvas.create_rectangle(
    55, 150, 375, 173,
    fill="#301923",
    outline=""
)

canvas.create_rectangle(
    425, 150, 745, 173,
    fill="#142d43",
    outline=""
)

# 산 체력바
acid_bar = canvas.create_rectangle(
    55, 150, 375, 173,
    fill=RED,
    outline=""
)

# 염기 체력바
base_bar = canvas.create_rectangle(
    425, 150, 745, 173,
    fill=BLUE,
    outline=""
)

status_id = canvas.create_text(
    400, 205,
    text="READY TO BATTLE",
    fill=WHITE,
    font=("Arial", 17, "bold")
)


def update_names(*args):
    canvas.itemconfig(acid_name, text=acid_var.get())
    canvas.itemconfig(base_name, text=base_var.get())


acid_var.trace_add("write", update_names)
base_var.trace_add("write", update_names)


# =========================================
# INPUT PANELS
# =========================================

input_area = tk.Frame(left_panel, bg=BG)
input_area.pack(fill="x", padx=25)


def create_panel(title, color, options,
                 chemical, concentration, volume):

    frame = tk.Frame(
        input_area,
        bg=PANEL,
        highlightbackground=color,
        highlightthickness=2
    )

    frame.pack(
        side="left",
        expand=True,
        fill="both",
        padx=8
    )

    tk.Label(
        frame,
        text=title,
        font=("Arial", 16, "bold"),
        bg=PANEL,
        fg=color
    ).pack(pady=10)

    ttk.Combobox(
        frame,
        textvariable=chemical,
        values=options,
        state="readonly",
        width=18
    ).pack(pady=5)

    for label, variable in [
        ("농도 (mol/L)", concentration),
        ("부피 (mL)", volume)
    ]:

        tk.Label(
            frame,
            text=label,
            bg=PANEL,
            fg=GRAY,
            font=("Arial", 10, "bold")
        ).pack(pady=(8, 2))

        tk.Entry(
            frame,
            textvariable=variable,
            font=("Arial", 13),
            justify="center",
            bg="#25344e",
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        ).pack(pady=(0, 8), ipady=5)


create_panel(
    "ACID FIGHTER",
    RED,
    ["HCl", "HNO3", "H2SO4"],
    acid_var, acid_c, acid_v
)

create_panel(
    "BASE FIGHTER",
    BLUE,
    ["NaOH", "KOH", "Ca(OH)2", "Ba(OH)2"],
    base_var, base_c, base_v
)


# =========================================
# RIGHT RESULT PANEL
# =========================================

result_frame = tk.Frame(
    right_panel,
    bg=PANEL,
    highlightbackground="#344765",
    highlightthickness=2
)

result_frame.pack(
    fill="both",
    expand=True
)

tk.Label(
    result_frame,
    text="전투 결과 보고서",
    bg=PANEL,
    fg=GOLD,
    font=("Arial", 21, "bold")
).pack(pady=(20, 12))

winner_label = tk.Label(
    result_frame,
    text="전투 대기 중",
    bg=PANEL,
    fg=GOLD,
    font=("Arial", 15, "bold"),
    wraplength=350
)

winner_label.pack(pady=10)

tk.Label(
    result_frame,
    text="화학 반응 분석 결과",
    bg=PANEL,
    fg=GRAY,
    font=("Arial", 10, "bold")
).pack(pady=(5, 12))

# 결과 스크롤 영역
text_frame = tk.Frame(
    result_frame,
    bg=PANEL
)

text_frame.pack(
    fill="both",
    expand=True,
    padx=12,
    pady=(0, 15)
)

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(
    text_frame,
    bg="#0c1628",
    fg=WHITE,
    font=("Malgun Gothic", 10),
    relief="flat",
    wrap="word",
    yscrollcommand=scrollbar.set,
    padx=10,
    pady=10
)

result_box.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.config(command=result_box.yview)

result_box.insert(
    "1.0",
    "START BATTLE 버튼을 눌러 전투를 시작하세요.\n\n"
    "화학 반응 계산 결과가 이곳에 표시됩니다."
)

result_box.config(state="disabled")


def set_result(text):
    result_box.config(state="normal")
    result_box.delete("1.0", "end")
    result_box.insert("1.0", text)
    result_box.config(state="disabled")


# =========================================
# CALCULATION
# =========================================

def calculate():

    try:
        ca = float(acid_c.get())
        va = float(acid_v.get())
        cb = float(base_c.get())
        vb = float(base_v.get())

        if not all(
            math.isfinite(x) and x > 0
            for x in [ca, va, cb, vb]
        ):
            raise ValueError

        acid = acid_var.get()
        base = base_var.get()

        # 용질의 몰수
        acid_mol = ca * va / 1000
        base_mol = cb * vb / 1000

        # H+와 OH-의 몰수
        h = acid_mol * CHEMICALS[acid][1]
        oh = base_mol * CHEMICALS[base][1]

        reacted = min(h, oh)

        remain_h = max(0, h - oh)
        remain_oh = max(0, oh - h)

        # 전체 용액 부피 (L)
        volume = (va + vb) / 1000

        # 중화점 판정
        neutral = math.isclose(
            h, oh,
            rel_tol=1e-10,
            abs_tol=1e-15
        )

        # 물의 자동 이온화까지 고려한 pH
        if neutral:
            ph = 7.0

        else:
            excess = (h - oh) / volume

            if excess > 0:
                h_conc = (
                    excess +
                    math.sqrt(excess ** 2 + 4 * KW)
                ) / 2

                ph = -math.log10(h_conc)

            else:
                oh_conc = (
                    -excess +
                    math.sqrt(excess ** 2 + 4 * KW)
                ) / 2

                ph = 14 + math.log10(oh_conc)

        # 개별 이온 목록
        ions = {}

        # 산의 음이온
        acid_ion = CHEMICALS[acid][2]
        ions[acid_ion] = acid_mol

        # 염기의 양이온
        base_ion = CHEMICALS[base][2]
        ions[base_ion] = base_mol

        # 남은 H+ 또는 OH-
        if remain_h > 0:
            ions["H⁺"] = remain_h

        if remain_oh > 0:
            ions["OH⁻"] = remain_oh

        # 양이온과 음이온의 총 몰수
        cations = sum(
            mol for ion, mol in ions.items()
            if ion.endswith("⁺")
        )

        anions = sum(
            mol for ion, mol in ions.items()
            if ion.endswith("⁻")
        )

        total = cations + anions

        # 액성 판정
        if neutral:
            nature = "중성"
            winner = "중화 성공!"
            color = GOLD

        elif ph < 7:
            nature = "산성"
            winner = "산성 용액 승리!"
            color = RED

        else:
            nature = "염기성"
            winner = "염기성 용액 승리!"
            color = BLUE

        # 남은 H+와 OH-의 비율
        acid_ratio = remain_h / h if h > 0 else 0
        base_ratio = remain_oh / oh if oh > 0 else 0

        # 비율이 0~1을 벗어나지 않도록 제한
        acid_ratio = max(0, min(1, acid_ratio))
        base_ratio = max(0, min(1, base_ratio))

        return {
            "acid": acid,
            "base": base,
            "h": h,
            "oh": oh,
            "reacted": reacted,
            "remain_h": remain_h,
            "remain_oh": remain_oh,
            "ions": ions,
            "cations": cations,
            "anions": anions,
            "total": total,
            "ph": ph,
            "nature": nature,
            "winner": winner,
            "color": color,
            "acid_ratio": acid_ratio,
            "base_ratio": base_ratio
        }

    except (ValueError, OverflowError, ZeroDivisionError):
        messagebox.showerror(
            "입력 오류",
            "농도와 부피에 0보다 큰 숫자를 입력해 주세요."
        )
        return None


# =========================================
# HEALTH BAR ANIMATION
# =========================================

def animate(frame=0):

    global busy

    if frame <= 40:

        progress = frame / 40

        # 남은 산과 염기의 비율
        acid_target = battle_data["acid_ratio"]
        base_target = battle_data["base_ratio"]

        # 처음에는 100%, 마지막에는 실제 남은 비율
        acid_current = 1 - progress * (1 - acid_target)
        base_current = 1 - progress * (1 - base_target)

        # 산 체력바
        acid_width = 320 * acid_current

        canvas.coords(
            acid_bar,
            55, 150,
            55 + acid_width, 173
        )

        # 염기 체력바
        base_width = 320 * base_current

        canvas.coords(
            base_bar,
            745 - base_width, 150,
            745, 173
        )

        messages = [
            "ENERGY CHARGING...",
            "ION COLLISION!",
            "NEUTRALIZATION!",
            "FINAL IMPACT!"
        ]

        index = min(frame // 11, 3)

        canvas.itemconfig(
            status_id,
            text=messages[index],
            fill=GOLD if frame % 4 < 2 else WHITE
        )

        # 충돌 파티클
        if frame % 3 == 0:

            x = random.randint(370, 430)
            y = random.randint(60, 170)

            particle = canvas.create_oval(
                x - 4, y - 4,
                x + 4, y + 4,
                fill=random.choice([RED, BLUE, GOLD]),
                outline=""
            )

            root.after(
                500,
                lambda p=particle: canvas.delete(p)
            )

        root.after(45, animate, frame + 1)

    else:
        show_result()

        busy = False

        start_button.config(
            state="normal",
            text="START BATTLE"
        )


# =========================================
# SHOW RESULT
# =========================================

def show_result():

    d = battle_data

    canvas.itemconfig(
        status_id,
        text=d["winner"],
        fill=d["color"]
    )

    winner_label.config(
        text=d["winner"],
        fg=d["color"]
    )

    # 전체 이온 목록
    ion_text = ""

    for ion, mol in d["ions"].items():

        count = mol * NA

        ion_text += (
            f"\n[{ion}]\n"
            f"  몰수 : {format_number(mol)} mol\n"
            f"  실제 개수 : {format_ion_count(count)} 개\n"
        )

    report = (
        "========== 전투 결과 보고서 ==========\n\n"

        "[ 중화 반응 분석 ]\n"
        f"반응한 H⁺ : {format_number(d['reacted'])} mol\n"
        f"반응한 OH⁻ : {format_number(d['reacted'])} mol\n"
        f"남은 H⁺ : {format_number(d['remain_h'])} mol\n"
        f"남은 OH⁻ : {format_number(d['remain_oh'])} mol\n"

        "\n-----------------------------------\n"
        "[ 전체 이온 목록 ]\n"
        + ion_text +

        "\n-----------------------------------\n"
        "[ 이온 개수 합계 ]\n"
        f"양이온 수 : {format_ion_count(d['cations'] * NA)} 개\n"
        f"음이온 수 : {format_ion_count(d['anions'] * NA)} 개\n"
        f"총 이온 수 : {format_ion_count(d['total'] * NA)} 개\n"

        "\n-----------------------------------\n"
        "[ 최종 용액 분석 ]\n"
        f"용액의 액성 : {d['nature']}\n"
        f"최종 pH : {d['ph']:.2f}\n"

        "\n==================================="
    )

    set_result(report)


# =========================================
# START BATTLE
# =========================================

def start_battle():

    global busy, battle_data

    if busy:
        return

    data = calculate()

    if data is None:
        return

    battle_data = data
    busy = True

    start_button.config(
        state="disabled",
        text="BATTLE IN PROGRESS..."
    )

    winner_label.config(
        text="반응 계산 중...",
        fg=GOLD
    )

    set_result("중화 반응을 분석하고 있습니다...")

    # 체력바 초기화
    canvas.coords(
        acid_bar, 55, 150, 375, 173
    )

    canvas.coords(
        base_bar, 425, 150, 745, 173
    )

    animate()


# =========================================
# START BUTTON
# =========================================

start_button = tk.Button(
    left_panel,
    text="START BATTLE",
    command=start_battle,
    font=("Arial", 17, "bold"),
    bg="#b91c2d",
    fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    relief="flat",
    cursor="hand2",
    padx=40,
    pady=12
)

start_button.pack(
    fill="x",
    padx=33,
    pady=(15, 8)
)


# =========================================
# FOOTER
# =========================================

tk.Label(
    left_panel,
    text="25 C | IDEAL STRONG ACID-BASE MODEL",
    font=("Arial", 9),
    bg=BG,
    fg=GRAY
).pack(pady=(8, 8))


# =========================================
# RUN
# =========================================

root.mainloop()
