import tkinter as tk
from tkinter import messagebox
from chemical_reaction import ChemicalReaction  # 이전과 동일한 모듈 사용

def calculate_rate():
    try:
        # 사용자 입력값 받기
        concentration = float(concentration_entry.get())
        time = float(time_entry.get())
        order = int(order_var.get())

        # ChemicalReaction 객체 생성
        reaction = ChemicalReaction(order)

        # 반응 속도 계산
        rate = reaction.calculate_rate(concentration, time, order)
        
        # 결과 출력
        result_label.config(text=f"계산된 반응 속도: {rate:.2f}")
    except ValueError:
        # 잘못된 입력 처리
        messagebox.showerror("입력 오류", "잘못된 값을 입력했습니다. 농도와 시간은 숫자로 입력하세요.")

# GUI 윈도우 설정
root = tk.Tk()
root.title("반응 속도 계산기")

# 레이아웃 설정
tk.Label(root, text="반응 차수를 선택하세요 (0, 1, 2):").pack(pady=5)
order_var = tk.StringVar()
order_menu = tk.OptionMenu(root, order_var, "0", "1", "2")
order_menu.pack(pady=5)

tk.Label(root, text="반응물 농도 (단위: M):").pack(pady=5)
concentration_entry = tk.Entry(root)
concentration_entry.pack(pady=5)

tk.Label(root, text="반응 시간 (단위: s):").pack(pady=5)
time_entry = tk.Entry(root)
time_entry.pack(pady=5)

# 계산 버튼
calculate_button = tk.Button(root, text="계산", command=calculate_rate)
calculate_button.pack(pady=20)

# 결과 레이블
result_label = tk.Label(root, text="계산된 반응 속도: ")
result_label.pack(pady=5)

# 프로그램 실행
root.mainloop()