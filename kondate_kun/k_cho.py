# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:35:35 2024

@author: kalen
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

class ChoFrame(tk.Frame):
    def __init__(self, master=None):
        
        super().__init__(master, width=400, height=400, bg="#ffebcd")
        self.configure(bg="#ffebcd")
        self.create_tablea()
        self.create_widgets()
        self.cho_menu()
        
    def create_widgets(self):
        
        # ====== TOPフレームに配置 ======
        
        self.columnconfigure(0, weight=1)

        # 行指定
        for i in range(5):
            self.rowconfigure(i, weight=1)

        # 背景画像の表示
        img_rs = tk.PhotoImage(file="./img/bg_rs.png")

        label_r0 = tk.Label(self, image=img_rs, bg="#ffebcd")
        label_r0.image = img_rs  # ガベージコレクションの防止
        label_r0.grid(row=0, column=0, columnspan=3, sticky="nsew")

       
        # ページタイトル 
        self.label_1 = tk.Label(self, text="７日分のメニューを選ぶ", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 11, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_1.grid(row=0, column=0)
        
        
        # 登録ボタンを配置
        button_1 = tk.Button(
            self, 
            text="メニューを選ぶ", 
            font=("HG丸ｺﾞｼｯｸM-PRO", 10), 
            bg="#ff7f50", 
            fg="#ffffff", command=self.cho_menu)
        button_1.grid(row=1, column=0)        
        
        
        # お知らせラベル
        label_7 = tk.Label(
            self, 
            text="★何度でも選び直しできます！", 
            font=("HG丸ｺﾞｼｯｸM-PRO", 10), 
            fg="#8b4513",
            bg="#ffebcd") 
        label_7.grid(row=3, column=0)
        
        # このページの終了ボタン
        self.button_1 = tk.Button(self, text="TOPに戻る", font=("HG丸ｺﾞｼｯｸM-PRO", 10),
                             bg="#800000", fg="#ffffff", command=self.destroy)
        self.button_1.grid(row=4, column=0)
        
        
        
        
    # ====== テーブル作成 ======
    def create_tablea(self):
        
        self.dbname = ('menu.db')
        self.conn = sqlite3.connect(self.dbname, isolation_level=None)#データベースを作成、自動コミット機能ON
        self.cursor = self.conn.cursor() #カーソルオブジェクトを作成
        
        sql = """CREATE TABLE IF NOT EXISTS menu(
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      menu_name STRING NOT NULL,
                      body STRING,
                      date INT
                  )"""
      
        # テーブルの作成
        self.cursor.execute(sql)
        self.conn.commit()
        
        
    #  メニューを選ぶロジック -----------------
    def cho_menu(self):
        global treeview_1
        
        # 登録数を数えるためにメニュー名列を取得
        sql = "SELECT menu_name FROM menu"
        self.cursor.execute(sql)
        # ↓メニュー名のタプルが入ったリスト
        len_menu = self.cursor.fetchall()

        # 登録数が7個未満の時は警告する
        if len(len_menu) < 7:
            messagebox.showwarning("注意", "登録メニューを７個以上にしてください")
        
            # この関数をブレイクして登録ページに飛ばす
        else:
            # 7個以上の登録がある時
            week = ["月", "火", "水", "木", "金", "土", "日"]
            
            #全レコードを取り出す
            sql = """SELECT * FROM menu"""
            self.cursor.execute(sql)
            all_list = self.cursor.fetchall()
            
            menu_list =[]
            for i in all_list:
                if i[1] != "":
                    menu_list.append(i[1])
                
            set_menu = []
            for j in range(7):
                
                cho = random.choice(menu_list)
                while cho in set_menu:
                    cho = random.choice(menu_list)
                set_menu.append(cho)
                
            # 選出メニューを一覧表示する
                
            c_name = ["week", "menu_name"]
            self.treeview_1 = ttk.Treeview(self, height=7, 
                                      selectmode="browse", show="headings", columns=c_name)
            self.treeview_1.heading(c_name[0], text="曜日")
            self.treeview_1.heading(c_name[1], text="メニュー名")
            
            self.treeview_1.column(c_name[0], anchor="center", width=30)
            self.treeview_1.column(c_name[1], anchor="center", width=100)
            
            for n in range(7):
                self.treeview_1.insert(parent="", index=n, values=(week[n], set_menu[n]))            
        
            self.treeview_1.grid(row=2, column=0)