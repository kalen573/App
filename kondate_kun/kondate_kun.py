# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 10:21:58 2024

@author: kalen
"""
import tkinter as tk
# ↓TOPページをインポート
# from k_top import TopFrame
import locale
locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

# ↓移管ページ先のファイルをインポート
# from k_reco import RecoFrame
# from k_list import ListFrame
# from k_cho import ChoFrame

from tkinter import ttk, messagebox, scrolledtext
import sqlite3
import datetime
import random

# このクラスがベースのウィンドウ設定になる
class TestBaseWindow(tk.Tk):

    def __init__(self):

        super().__init__()
        self.iconfile = '.\img\gohan.ico'
        self.iconbitmap(default=self.iconfile)
        self.title("こんだて君")
        self.geometry("400x400")
        self.configure(bg="#ffebcd")
        self.resizable(False, False)

        self.top = TopFrame(self)
        # この記述が無いと配置がズレる
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.top.grid(row=0, column=0, sticky="nsew")

# ========== TOPページのクラス ============
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


# ========== 登録ページのクラス ============

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


# ========== 一覧/編集/削除ページのクラス ============

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

# ========== 選出ページのクラス ============

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


if __name__ == "__main__":

    app = TestBaseWindow()
    app.mainloop()