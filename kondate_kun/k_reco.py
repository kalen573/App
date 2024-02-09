# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:30:29 2024

@author: kalen
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import datetime

class RecoFrame(tk.Frame):
    def __init__(self, master=None):
        
        super().__init__(master, width=400, height=400, bg="#ffebcd")
        
        self.create_tablea()
        self.create_widgets()
        # self.tkraise()
        
        
    def create_widgets(self):
        
        # ====== Recoフレームの行列配置と背景画像の設定 ======
        
        self.configure(bg="#ffebcd")

        # 行指定
        for i in range(7):
            self.rowconfigure(i, weight=1)
        # 列指定
        for j in range(3):
            self.columnconfigure(j, weight=1)

        # 背景画像の表示
        img_rs = tk.PhotoImage(file="./img/bg_rs.png")

        label_r0 = tk.Label(self, image=img_rs, bg="#ffebcd")
        label_r0.image = img_rs  # ガベージコレクションの防止
        label_r0.grid(row=0, column=0, columnspan=3, sticky="nsew")

        
        # ====== ウィジェット配置 ======
       
        # ページタイトル 
        self.label_1 = tk.Label(self, text="新しいメニューを登録します", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 11, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_1.grid(row=0, column=0, columnspan=3)
        
        # メニュー名スラベル 
        self.label_4 = tk.Label(self, text="メニュー名：", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 9, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_4.grid(row=1, column=1, sticky="sw")
        
        self.label_5 = tk.Label(self, text="※必須 全角15文字まで", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 8, "bold"), fg="#ff0000", bg="#ffebcd")
        self.label_5.grid(row=1, column=1, padx=20, sticky="s")

        # メニュー名入力欄
        self.menu_title = tk.Entry(self, font=("HG丸ｺﾞｼｯｸM-PRO", 9), width=20)
        self.menu_title.grid(row=2, column=1, sticky="n")
        
        # テキストボックス説明ラベル 
        self.label_6 = tk.Label(self, text="メモ：", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 9, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_6.grid(row=3, column=1, sticky="sw")
        
        # テキストボックス説明ラベル 
        self.label_7 = tk.Label(self, text="※１００文字入力可能 URLはリンク化しません", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 8), fg="#8b4513", bg="#ffebcd")
        self.label_7.grid(row=3, column=1, sticky="se")

        #　詳細入力BOX 
        self.menu_body = scrolledtext.ScrolledText(self, font=("HG丸ｺﾞｼｯｸM-PRO", 9), width=20, height=5)

        # self.menu_body = tk.Text(self, font=("HG丸ｺﾞｼｯｸM-PRO", 9), width=20, height=5)
        self.menu_body.grid(row=4, column=1, sticky="n")
        
        # メニュー登録ボタン
        self.button_7 = tk.Button(self, text="登録", 
                              font=("HG丸ｺﾞｼｯｸM-PRO", 11), bg="#ff7f50", fg="#ffffff", command=self.input_menu)
        self.button_7.grid(row=5, column=0, columnspan=3)
        
        
        
        # このページの終了ボタン
        self.button_1 = tk.Button(self, text="TOPに戻る", font=("HG丸ｺﾞｼｯｸM-PRO", 10),
                             bg="#800000", fg="#ffffff", command=self.destroy)
        self.button_1.grid(row=6, column=0, columnspan=3)
        
        
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
    
    # ====== 登録 ======
    def input_menu(self):
        
        # 入力値を変数に取る
        g_menu = self.menu_title.get()
        m_body = self.menu_body.get(1.0, tk.END)

        # DBから登録済みメニュー名をリスト化
        sql = "SELECT menu_name FROM menu"
        self.cursor.execute(sql)
        self.all_name = self.cursor.fetchall()
        m_list =[]

        for i in self.all_name:
            if i[0] != "":
                m_list.append(i[0])

        if g_menu == "":
            messagebox.showwarning("警告", "レシピ名を入れてください！")

        elif len(g_menu) > 15:
            messagebox.showwarning("警告", str(len(g_menu)) + " 文字入力されています！\nメニュー名は15文字以内にしてください！")
            
        elif g_menu in m_list:
            messagebox.showwarning("警告", "そのメニュー名は既に登録されています！")

        elif len(m_body) > 100:
            messagebox.showwarning("警告", str(len(m_body)) + "文字入力されています！\nメモは100文字以内にしてください！")
                
        else:

            sql = """ INSERT INTO menu VALUES(NULL, ?, ?, ?)"""
            
            menu_name = self.menu_title.get()
            m_body = self.menu_body.get(1.0, tk.END)
            date = datetime.datetime.now()
            date = date.strftime('%Y年%m月%d日 %H:%M:%S')
            
            in_data = (menu_name, m_body, date)



            self.cursor.execute(sql, in_data)
            self.conn.commit()



            self.menu_title.delete(0, tk.END)
            self.menu_body.delete("1.0","end")
            
            messagebox.showinfo("登録完了", menu_name + "を登録しました！")
               