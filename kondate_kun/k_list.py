# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:35:03 2024

@author: kalen
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import datetime

class ListFrame(tk.Frame):
    def __init__(self, master=None):
        
        super().__init__(master, width=400, height=400, bg="#ffebcd")

        self.create_tablea()
        self.all_menu_list()
        self.create_list()
        self.create_widgets()
        
    def create_widgets(self):
        
        # ====== リストフレームの行列配置と背景画像の設定 ======
        
        self.configure(bg="#ffebcd")

        # 行指定
        for i in range(8):
            self.rowconfigure(i, weight=1)
        # 列指定
        for j in range(3):
            self.columnconfigure(j, weight=1)

        # # 背景画像の表示
        img_rs = tk.PhotoImage(file="./img/bg_rs.png")

        label_r0 = tk.Label(self, image=img_rs, bg="#ffebcd")
        label_r0.image = img_rs  # ガベージコレクションの防止
        label_r0.grid(row=0, column=0, columnspan=3, sticky="nsew")

        # ====== ウィジェット配置 ======
        

        # ページタイトル 
        self.label_1 = tk.Label(self, text="メニュー名をクリックすると詳細が見られます", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 11, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_1.grid(row=0, column=0, columnspan=4)
        
        
        # メニュー名ラベル 
        self.label_4 = tk.Label(self, text="メニュー名：", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 9, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_4.grid(row=2, column=1, sticky="sw")
        
        self.label_5 = tk.Label(self, text="※必須 全角15文字まで", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 8, "bold"), fg="#ff0000", bg="#ffebcd")
        self.label_5.grid(row=2, column=1, padx=20, sticky="s")

        # メニュー名入力欄
        self.menu_title = tk.Entry(self, font=("HG丸ｺﾞｼｯｸM-PRO", 9), width=20)
        self.menu_title.grid(row=3, column=1, sticky="n")
        
        # テキストボックス説明ラベル 
        self.label_6 = tk.Label(self, text="メモ：", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 9, "bold"), fg="#8b4513", bg="#ffebcd")
        self.label_6.grid(row=4, column=1, sticky="sw")
        
        # テキストボックス説明ラベル 
        self.label_7 = tk.Label(self, text="※１００文字入力可能 URLはリンク化しません", 
                                    font=("HG丸ｺﾞｼｯｸM-PRO", 8), fg="#8b4513", bg="#ffebcd")
        self.label_7.grid(row=4, column=1, sticky="se")

        #　詳細入力BOX 
        self.menu_body = scrolledtext.ScrolledText(self, font=("HG丸ｺﾞｼｯｸM-PRO", 9), width=20, height=5)
        # self.menu_body = tk.Text(self, font=("HG丸ｺﾞｼｯｸM-PRO", 9), width=20, height=5)
        self.menu_body.grid(row=5, column=1, sticky="n")
        
        
        
        # 更新ボタンを配置
        self.button_7 = tk.Button(self, text="更新", 
                              font=("HG丸ｺﾞｼｯｸM-PRO", 11), bg="#ff7f50", fg="#ffffff", command=self.re_reco_menu)
        self.button_7.grid(row=6, column=1, sticky="w")


        # 削除ボタンを配置
        self.button_8 = tk.Button(self, text="削除", 
                              font=("HG丸ｺﾞｼｯｸM-PRO", 11), bg="#ff0000", fg="#ffffff", command=self.del_data)
                              
        self.button_8.grid(row=6, column=1, sticky="e")
        
        
        
        
        # このページの終了ボタン
        self.button_1 = tk.Button(self, text="TOPに戻る", font=("HG丸ｺﾞｼｯｸM-PRO", 10),
                             bg="#800000", fg="#ffffff", command=self.destroy)
        self.button_1.grid(row=7, column=0, columnspan=4)
        
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
        
    # ====== リスト抽出 ======
    def all_menu_list(self):
        
        #全レコードを取り出す
        sql = """SELECT * FROM menu"""
        self.cursor.execute(sql)
        self.all_list = self.cursor.fetchall()
        
        self.all_menu = []
        set_list = []
        
        for s in range(len(self.all_list)):
            if self.all_list[s][1] != "":
                set_list.append(self.all_list[s][0])
                set_list.append(self.all_list[s][1])
                set_list.append(self.all_list[s][2])
                set_list.append(self.all_list[s][3])
                
                self.all_menu.append(set_list)
                
                set_list = []
    
    # ====== 一覧形成 ======
    def create_list(self):
        
        self.all_menu_list()
        
        # カラムを定義
        l_name = ['menu_name', 'body', "data"]

        #Treeviewを宣言
        self.menu_tree = ttk.Treeview(self, selectmode="browse", 
                                  show="headings", columns = l_name, 
                                  height=3)
        #  view_menu関数で編集削除用にテキストおよびボディフィールドに表示する
        self.menu_tree.bind("<<TreeviewSelect>>", self.view_menu)
        
        self.menu_tree.heading(l_name[0], text='メニュー名')
        self.menu_tree.heading(l_name[1], text='メニュー詳細')
        self.menu_tree.heading(l_name[2], text='登録日時')
        
        self.menu_tree.column(l_name[0], anchor="center", width=50)
        self.menu_tree.column(l_name[1], anchor="w", width=30)
        self.menu_tree.column(l_name[2], anchor="w", width=30)

        for n in range(len(self.all_menu)):
            self.menu_tree.insert(parent="", index="end", 
                                  values=(self.all_menu[n][1], self.all_menu[n][2], self.all_menu[n][3]))
            
        self.menu_tree.grid(row=1, column=1, sticky="nsew")
        
        # 縦のスクロール
        self.scroll_v = ttk.Scrollbar(self, orient = tk.VERTICAL, command = self.menu_tree.yview)
        # 一覧表示の横に設置
        self.menu_tree.configure(yscrollcommand = self.scroll_v.set)
        self.scroll_v.grid(row=1, column=2, sticky="ns"+"w")
        
    # --- 編集削除用に選択したメニューをEntryおよびＴｅｘｔに表示 ---

    def view_menu(self, event):
        global menu_title
        global menu_body
        global menu_id
        
        # 選択行の判別
        reco_id = self.menu_tree.focus()
        # オプション名valuesはレコードの値をすべて取得
        reco_val = self.menu_tree.item(reco_id, "values")
        
        # 既に表示されていたものがあったらそれを削除する
        if self.menu_title != "":
            self.menu_title.delete(0, tk.END)
            self.menu_body.delete("1.0","end")
        
        # エントリー欄とテキストBOXに表示
        self.menu_title.insert(tk.INSERT, reco_val[0])
        self.menu_body.insert(tk.INSERT, reco_val[1])
        
        
        
    # ------------- 選択したメニュー編集する ----------------------

    def re_reco_menu(self):
        
        # 選択行の判別
        reco_id = self.menu_tree.focus()
        # メニュー名、詳細、日付が入っている
        reco_val = self.menu_tree.item(reco_id, "values")
        
        # 選択されたメニューのIDをメニュー名でDBから検索
        sql = "SELECT * FROM menu WHERE menu_name=?;"
        d_menu_id = (reco_val[0],)
        self.cursor.execute(sql, d_menu_id)
        sel_menu_id = self.cursor.fetchall()
        for i in sel_menu_id:
            m_id = []
            m_id.append(i[0])
            
        # 選択されたメニューのIDを確保    
        select_menu_id = m_id[0]
        
        # 後から入力されたもの
        re_reco_m = self.menu_title.get()
        re_reco_b = self.menu_body.get("1.0", "end")
        
        if re_reco_m == "":
            messagebox.showwarning("警告", "レシピ名を入れてください！")
        
        elif len(re_reco_m) > 15:
            messagebox.showwarning("警告", str(len(re_reco_m)) + " 文字入力されています。\nメニュー名は15文字以内にしてください")

        elif len(re_reco_b) > 100:
            messagebox.showwarning("警告", str(len(re_reco_b)) + "文字入力されています！\nメモは100文字以内にしてください！")
            
        else:
            a = messagebox.askokcancel("確認", "更新しますか？")
            
            if a:
                date = datetime.datetime.now()
                re_date = date.strftime('%Y年%m月%d日 %H:%M:%S')
            
                sql = """UPDATE menu SET menu_name=?, body=?, date=? WHERE id=?"""
                
                re_data = (re_reco_m, re_reco_b, re_date, select_menu_id)
                
                self.cursor.execute(sql, re_data)
                self.conn.commit()
                
                self.menu_title.delete(0, tk.END)
                self.menu_body.delete("1.0","end")
                messagebox.showinfo("更新完了", re_reco_m + "を更新しました！")
                
                # リロード
                self.menu_tree.destroy()
                self.create_list()
 
            
    # ------------- 選択したメニュー削除する ----------------        
    def del_data(self):
        
        # 選択行の判別
        reco_id = self.menu_tree.focus()
        reco_val = self.menu_tree.item(reco_id, "values")
        
        del_menu = reco_val[0]
        
        a = messagebox.askokcancel("確認", "本当に削除しますか？")
        
        if a != True:
            messagebox.showinfo("確認", "削除をキャンセルしました")
            
        else:
                            
            sql ="""DELETE FROM menu WHERE menu_name=?;"""
            del_data = (del_menu,)
            self.cursor.execute(sql, del_data)
            self.conn.commit()
            
            self.menu_title.delete(0, tk.END)
            self.menu_body.delete("1.0","end")
            messagebox.showinfo("削除完了", del_menu + "を削除しました！")
            
            # リロードする
            self.menu_tree.destroy()
            self.create_list()
