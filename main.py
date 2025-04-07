import tkinter as tk
from tkinter import messagebox
from chemical_reaction import ReactionSimulator

def calculate():
    try:
        order = reaction_order.get()
        A0 = float(entry_A0.get())
        At = float(entry_At.get())
        t = float(entry_time.get())

        if At > A0:
            raise ValueError("최종 농도는 초기 농도보다 작거나 같아야 합니다.")

        # 계산
        reaction_amount = A0 - At
        k = ReactionSimulator.calculate_rate_constant(order, A0, At, t)
        rate = ReactionSimulator(order, A0, k).calculate_rate(At)

        # 결과 표시
        result_text.set(f"""[결과]
반응량: {reaction_amount:.4f} M
속도 상수 (k): {k:.4f}
현재 반응 속도: {rate:.4f} M/s""")

    except ValueError as ve:
        messagebox.showerror("입력 오류", str(ve))
    except Exception:
        messagebox.showerror("오류", "유효한 숫자를 모두 입력했는지 확인하세요.")

# GUI 생성
root = tk.Tk()
root.title("반응 속도 계산기")

# 반응 차수 선택
reaction_order = tk.IntVar(value=1)
tk.Label(root, text="반응 차수:").grid(row=0, column=0, sticky='w')
tk.Radiobutton(root, text="0차", variable=reaction_order, value=0).grid(row=0, column=1)
tk.Radiobutton(root, text="1차", variable=reaction_order, value=1).grid(row=0, column=2)
tk.Radiobutton(root, text="2차", variable=reaction_order, value=2).grid(row=0, column=3)

# 입력 필드
tk.Label(root, text="[A]₀ (M):").grid(row=1, column=0, sticky='w')
entry_A0 = tk.Entry(root)
entry_A0.grid(row=1, column=1, columnspan=3)

tk.Label(root, text="[A]ₜ (M):").grid(row=2, column=0, sticky='w')
entry_At = tk.Entry(root)
entry_At.grid(row=2, column=1, columnspan=3)

tk.Label(root, text="시간 (s):").grid(row=3, column=0, sticky='w')
entry_time = tk.Entry(root)
entry_time.grid(row=3, column=1, columnspan=3)

# 버튼
tk.Button(root, text="계산하기", command=calculate).grid(row=4, column=0, columnspan=4, pady=10)

# 결과 출력
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, justify="left").grid(row=5, column=0, columnspan=4)

root.mainloop()