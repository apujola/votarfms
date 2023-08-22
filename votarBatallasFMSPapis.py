import tkinter as tk
from tkinter import messagebox

class FMSVotingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FMS Voting App")
        
        self.competitors = ["Competitor A", "Competitor B"]
        self.rounds = ["Easy Mode", "Hard Mode", "Temática 1", "Temática 2", "Random Mode", "Minuto 1", "Minuto 2", "Deluxe", "Réplica"]
        
        self.votes = {competitor: {round_name: [tk.StringVar() for _ in range(6)] for round_name in self.rounds} for competitor in self.competitors}
        self.user_totals = {competitor: {round_name: tk.IntVar() for round_name in self.rounds} for competitor in self.competitors}
        
        self.current_round_index = 0
        
        self.label_round = tk.Label(root, text=self.rounds[self.current_round_index], font=("Helvetica", 16, "bold"))
        self.label_round.pack(pady=10)
        
        self.frames = []
        for competitor in self.competitors:
            frame = tk.Frame(root)
            frame.pack(side="top", padx=20, pady=10)
            self.frames.append(frame)
            
            label_competitor = tk.Label(frame, text=competitor, font=("Helvetica", 14))
            label_competitor.pack(side="left", padx=10)
            
            pattern_entries = []
            for i in range(6):
                pattern_entry = tk.Entry(frame, width=5, textvariable=self.votes[competitor][self.rounds[0]][i])
                pattern_entry.insert(0, "0")
                pattern_entry.pack(side="left", padx=5)
                pattern_entries.append(pattern_entry)
            self.votes[competitor]["Total"] = tk.IntVar()
            total_value_label = tk.Label(frame, textvariable=self.votes[competitor]["Total"], font=("Helvetica", 12, "bold"))
            total_value_label.pack(side="left", padx=10)
        
        self.button_prev = tk.Button(root, text="Previous", command=self.prev_round)
        self.button_prev.pack(side="left", padx=20, pady=10)
        
        self.button_next = tk.Button(root, text="Next", command=self.next_round)
        self.button_next.pack(side="right", padx=20, pady=10)
        
        self.update_ui()
        
    def calculate_total(self, competitor, round_name):
        total = sum(int(value.get()) if value.get().isdigit() else 0 for value in self.votes[competitor][round_name])
        self.user_totals[competitor][round_name].set(total)
        
    def update_ui(self):
        round_name = self.rounds[self.current_round_index]
        self.label_round.config(text=round_name)
        
        for competitor in self.competitors:
            current_votes = self.votes[competitor][round_name]
            for i, pattern_entry in enumerate(self.votes[competitor][round_name]):
                pattern_entry.set(current_votes[i].get())
            
            self.calculate_total(competitor, round_name)
            
            total_rounds = sum(self.user_totals[competitor][round_name].get() for round_name in self.rounds)
            self.votes[competitor]["Total"].set(total_rounds)  # Update the total value label
        
    def next_round(self):
        round_name = self.rounds[self.current_round_index]
        for competitor in self.competitors:
            self.calculate_total(competitor, round_name)
            for pattern_entry in self.votes[competitor][round_name]:
                pattern_entry.set("0")
        
        if self.current_round_index < len(self.rounds) - 1:
            self.current_round_index += 1
            self.calculate_total("Competitor A", round_name)  # Calculate total for Competitor A
            self.calculate_total("Competitor B", round_name)  # Calculate total for Competitor B
            self.update_ui()
        else:
            self.calculate_total("Competitor A", round_name)  # Calculate total for Competitor A
            self.calculate_total("Competitor B", round_name)  # Calculate total for Competitor B
            self.show_final_results()
        
    def prev_round(self):
        if self.current_round_index > 0:
            round_name = self.rounds[self.current_round_index]
            for competitor in self.competitors:
                self.calculate_total(competitor, round_name)
            self.current_round_index -= 1
            self.update_ui()
        
    def show_final_results(self):
        winner_diff = self.determine_winner()
        winner_msg = "Ganador" if winner_diff > 5 else "Réplica"
        message = f"Resultados Finales:\n\n"
        
        for competitor in self.competitors:
            total_rounds = sum(self.user_totals[competitor][round_name].get() for round_name in self.rounds)
            message += f"{competitor}: {total_rounds}\n"
        
        message += f"\n{winner_msg}"
        messagebox.showinfo("Resultados Finales", message)
        
    def determine_winner(self):
        total_a = sum(self.user_totals["Competitor A"][round_name].get() for round_name in self.rounds)
        total_b = sum(self.user_totals["Competitor B"][round_name].get() for round_name in self.rounds)
        return abs(total_a - total_b)

if __name__ == "__main__":
    root = tk.Tk()
    app = FMSVotingApp(root)
    root.geometry("800x400")  # Set the initial size of the window
    root.mainloop()
