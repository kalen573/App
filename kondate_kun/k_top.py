# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:25:32 2024

@author: kalen
"""

import tkinter as tk
# ↓移管ページ先のファイルをインポート
from k_reco import RecoFrame
from k_list import ListFrame
from k_cho import ChoFrame

class TopFrame(tk.Frame):

    def __init__(self, master:tk.Tk=None):

        super().__init__(master, width=400, height=400, bg="#ffebcd")

        self.create_widgets()
        
    def create_widgets(self):
        
        # ====== TOPフレーム　行列配置と背景画像の設定 ======
        
        # 行の配置
        for i in range(5):
            self.rowconfigure(i, weight=1)

        # 列の配置
        self.columnconfigure(0, weight=1)

        # 背景画像の表示
        img = tk.PhotoImage(file="./img/bg_r.png")

        # 各行にLabelを作成し、画像を設定
        for n in range(5):
            label_n = tk.Label(self, image=img)
            label_n.image = img  # ガベージコレクションの防止
            label_n.grid(row=n, column=0, columnspan=3, sticky="nsew")


        
        # ====== タイトル ======
        
        # タイトルの配置
        label_1 = tk.Label(
            self, 
            text="こ ん だ て 君", 
            font=("HG丸ｺﾞｼｯｸM-PRO", 20, "bold"), 
            fg="#8b4513",
            bg="#ffebcd") 
        label_1.grid(row=0, column=0, columnspan=3)
        
        # アプリの説明
        label_2 = tk.Label(self, text="献立君は登録したメニューから\n1週間分の献立を自動で作成してくれます。", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 10, "bold"), fg="#dc143c", bg="#ffebcd")
        label_2.grid(row=1, column=0, columnspan=3, sticky="n")
        
        # 
        label_3 = tk.Label(self, text="やりたいことを選んでね", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 10, "bold"), fg="#8b4513", bg="#ffebcd")
        label_3.grid(row=1, column=0, columnspan=3, stick="s")
        
        # ====== ボタン ======

        # 選出用ボタン
        self.button_3 = tk.Button(self, text="メニューを選ぶ", 
                              font=("HG丸ｺﾞｼｯｸM-PRO", 11, "bold"), bg="#ff4500", fg="#ffffff",
                              width=18, command=self.open_cho_frame)
        self.button_3.grid(row=2, column=0, columnspan=3, sticky="s")
        
        # 登録用ボタン
        self.button_1 = tk.Button(self, text="メニューを登録", 
                              font=("HG丸ｺﾞｼｯｸM-PRO", 10), bg="#ff7f50", 
                              fg="#ffffff",
                              width=18, 
                              command=self.open_reco_frame)
        self.button_1.grid(row=3, column=0, columnspan=3)
        
        
        # 一覧用ボタン
        self.button_2 = tk.Button(self, text="メニュー一覧　編集　削除", 
                              font=("HG丸ｺﾞｼｯｸM-PRO", 10), bg="#ff7f50", fg="#ffffff",
                              width=18, command=self.open_list_frame)
        self.button_2.grid(row=4, column=0, columnspan=3, sticky="n")       
        
        
    def open_reco_frame(self):
        menu_reco = RecoFrame(self.master)
        menu_reco.grid(row=0, column=0, sticky="nsew")
        
    def open_list_frame(self):
        menu_list = ListFrame(self.master)
        menu_list.grid(row=0, column=0, sticky="nsew")
        
    def open_cho_frame(self):
        menu_cho = ChoFrame(self.master)
        menu_cho.grid(row=0, column=0, sticky="nsew")
       