import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class FMSVotingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FMS Voting App")
        
        # Cargar la imagen de fondo
        background_image = Image.open("/Users/axeloner/Pictures/Banner FMS España/header-fms-5.jpg")
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.competitors = ["MC 1", "MC 2"]
        self.rounds = ["Easy Mode", "Hard Mode", "Temática 1", "Temática 2", "Random Mode", "Minuto 1", "Minuto 2", "Deluxe"]
        self.current_round_index = 0
        
        self.votes = {competitor: {round_name: [tk.StringVar() for _ in range(9)] for round_name in self.rounds} for competitor in self.competitors}
        self.round_totals = {round_name: {competitor: tk.IntVar() for competitor in self.competitors} for round_name in self.rounds}
        self.total_rounds = {competitor: tk.IntVar() for competitor in self.competitors}

         # Configurar el fondo de la ventana con la imagen cargada
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.show_round()
        
        self.root.mainloop()
        
    def calculate_total(self, competitor, round_name):
        total = sum(int(value.get()) if value.get().isdigit() else 0 for value in self.votes[competitor][round_name])
        self.round_totals[round_name][competitor].set(total)
        
    def show_round(self):
        round_name = self.rounds[self.current_round_index]
        self.root.title(round_name)
        
        for widget in self.root.winfo_children():
            widget.destroy()
        
        for competitor in self.competitors:
            frame = tk.Frame(self.root)
            frame.pack(side="top", padx=20, pady=10)
            
            label_competitor = tk.Label(frame, text=competitor, font=("Helvetica", 14))
            label_competitor.pack(side="left", padx=10)
            
            pattern_entries = []
            for i in range(9):
                pattern_frame = tk.Frame(frame)
                pattern_frame.pack(side="left", padx=5)
                
                if i < 6:
                    tk.Label(pattern_frame, text=f"P{i+1}").pack(side="top")
                elif i == 6:
                    tk.Label(pattern_frame, text="Skills").pack(side="top")
                elif i == 7:
                    tk.Label(pattern_frame, text="Flow").pack(side="top")
                elif i == 8:
                    tk.Label(pattern_frame, text="P.Escena").pack(side="top")
                
                pattern_entry = tk.Entry(pattern_frame, width=5, textvariable=self.votes[competitor][round_name][i])
                pattern_entry.insert(0, "0")
                pattern_entry.pack(side="top")
                pattern_entries.append(pattern_entry)
        
        self.button_next = tk.Button(self.root, text="Next", command=self.next_round)
        self.button_next.pack(side="bottom", padx=20, pady=10)
        
        self.root.update_idletasks()
        self.root.geometry(f"{self.root.winfo_reqwidth()}x{self.root.winfo_reqheight()}")
        
    def next_round(self):
        round_name = self.rounds[self.current_round_index]
        for competitor in self.competitors:
            self.calculate_total(competitor, round_name)
        
        self.current_round_index += 1
        
        if self.current_round_index < len(self.rounds):
            self.show_round()
            if round_name == "Deluxe":
                self.button_next.config(text="Results", command=self.show_final_results)
        else:
            self.show_final_results()
        
    def show_final_results(self):
        for round_name in self.rounds:
            for competitor in self.competitors:
                self.calculate_total(competitor, round_name)
        
        for competitor in self.competitors:
            total_rounds = sum(self.round_totals[round_name][competitor].get() for round_name in self.rounds)
            self.total_rounds[competitor].set(total_rounds)
        
        for widget in self.root.winfo_children():
            widget.destroy()
            
        winner_diff = self.total_rounds["MC 1"].get() - self.total_rounds["MC 2"].get()
        
        if winner_diff >= 5:
            winner_msg = "Ganador: MC 1" if winner_diff > 0 else "Ganador: MC 2"
            self.button_close = tk.Button(self.root, text="Cerrar", command=self.root.destroy)
            self.button_close.pack(padx=20, pady=10)
        else:
            winner_msg = "Réplica"
            self.button_next_replica = tk.Button(self.root, text="Ronda Réplica", command=self.show_replica)
            self.button_next_replica.pack(padx=20, pady=10)
        
        for competitor in self.competitors:
            label = tk.Label(self.root, text=f"{competitor}: {self.total_rounds[competitor].get()}", font=("Helvetica", 12))
            label.pack()
            
        winner_label = tk.Label(self.root, text=winner_msg, font=("Helvetica", 14, "bold"))
        winner_label.pack(pady=10)
        
    def show_replica(self):
        self.current_round_index = len(self.rounds) - 1
        self.show_round()

if __name__ == "__main__":
    root = tk.Tk()
    app = FMSVotingApp(root)
