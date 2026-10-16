import tkinter as tk
import random

BARIS = 15
KOLOM = 10
UKURAN_BLOK = 30

BENTUK = [
    [(0,0), (0,1), (1,0), (1,1)], 
    [(0,0), (0,1), (0,2), (0,3)], 
    [(0,0), (0,1), (0,2), (1,2)]  
]
WARNA = ["red", "cyan", "orange"]


class TetrisSimpel:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris Presentasi")
        
       
        self.canvas = tk.Canvas(root, width=KOLOM*UKURAN_BLOK, height=BARIS*UKURAN_BLOK, bg="black")
        self.canvas.pack()
        
        self.label_skor = tk.Label(root, text="Skor: 0", font=("Arial", 14, "bold"))
        self.label_skor.pack()

        self.papan = {} 
        self.skor = 0
        
        self.root.bind("<Left>", lambda e: self.gerak(-1, 0))
        self.root.bind("<Right>", lambda e: self.gerak(1, 0))
        self.root.bind("<Down>", lambda e: self.gerak(0, 1))
        
        self.buat_balok_baru()
        self.update_game() 
    
    def buat_balok_baru(self):
        idx = random.randint(0, len(BENTUK)-1)
        self.balok_aktif = BENTUK[idx]
        self.warna_aktif = WARNA[idx]
        self.x_aktif = KOLOM // 2 - 1
        self.y_aktif = 0
        
        if self.cek_tabrakan(self.x_aktif, self.y_aktif):
            self.papan.clear()
            self.skor = 0

    def cek_tabrakan(self, geser_x, geser_y):
        for (x, y) in self.balok_aktif:
            pos_x, pos_y = geser_x + x, geser_y + y
            if pos_x < 0 or pos_x >= KOLOM or pos_y >= BARIS or (pos_x, pos_y) in self.papan:
                return True
        return False

    def gerak(self, dx, dy):
        if not self.cek_tabrakan(self.x_aktif + dx, self.y_aktif + dy):
            self.x_aktif += dx
            self.y_aktif += dy
            self.gambar_layar()
        elif dy == 1: 
            self.kunci_balok()
            self.hapus_baris_penuh()
            self.buat_balok_baru()

    def kunci_balok(self):
        for (x, y) in self.balok_aktif:
            self.papan[(self.x_aktif + x, self.y_aktif + y)] = self.warna_aktif

    def hapus_baris_penuh(self):
        baris_hancur = []
        for y in range(BARIS):
            if sum(1 for x in range(KOLOM) if (x, y) in self.papan) == KOLOM:
                baris_hancur.append(y)
        
        for y in baris_hancur:
            self.skor += 10
            papan_baru = {}
            for (bx, by), warna in self.papan.items():
                if by < y:
                    papan_baru[(bx, by + 1)] = warna
                elif by > y:
                    papan_baru[(bx, by)] = warna
            self.papan = papan_baru
        
        self.label_skor.config(text=f"Skor: {self.skor}")

    def gambar_layar(self):
        self.canvas.delete("all")
        for (x, y), warna in self.papan.items():
            self.gambar_kotak(x, y, warna)
        for (x, y) in self.balok_aktif:
            self.gambar_kotak(self.x_aktif + x, self.y_aktif + y, self.warna_aktif)

    def gambar_kotak(self, x, y, warna):
        x1, y1 = x * UKURAN_BLOK, y * UKURAN_BLOK
        x2, y2 = x1 + UKURAN_BLOK, y1 + UKURAN_BLOK
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=warna, outline="white")

    def update_game(self):
        self.gerak(0, 1) 
        self.root.after(400, self.update_game) 

if __name__ == "__main__":
    jendela = tk.Tk()
    game = TetrisSimpel(jendela)
    jendela.mainloop()