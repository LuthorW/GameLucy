import tkinter as tk
from tkinter import messagebox
import random

class RomanceRPG:
    def __init__(self, root):
        self.root = root
        self.root.title("Letícia Luthor e Lucy Williams - Um Romance no Campus <3")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Variáveis do jogo
        self.affinity = 0
        self.day = 1
        self.visited_locations = set()
        self.choices_made = {}
        self.lucy_mood = "neutra"
        self.current_scene = "inicio"
        
        # Configuração da interface
        self.setup_ui()
        
        # Iniciar jogo
        self.show_scene("inicio")  # Esta chamada está correta agora
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Texto da cena com scrollbar
        text_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_display = tk.Text(text_frame, wrap=tk.WORD, bg="#f0f0f0", 
                                  fg="#333333", font=("Helvetica", 12), 
                                  height=15, padx=10, pady=10,
                                  yscrollcommand=scrollbar.set)
        self.text_display.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_display.yview)
        self.text_display.config(state=tk.DISABLED)
        
        # Frame de opções
        self.options_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.options_frame.pack(fill=tk.X, pady=(10, 5))
        
        # Barra de status
        self.status_frame = tk.Frame(self.root, bg="#e0e0e0", height=40)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.affinity_label = tk.Label(self.status_frame, text=f"Afinidade: {self.affinity}", 
                                     bg="#e0e0e0", font=("Helvetica", 10, "bold"))
        self.affinity_label.pack(side=tk.LEFT, padx=15)
        
        self.day_label = tk.Label(self.status_frame, text=f"Dia: {self.day}", 
                                bg="#e0e0e0", font=("Helvetica", 10, "bold"))
        self.day_label.pack(side=tk.LEFT, padx=15)
        
        self.mood_label = tk.Label(self.status_frame, text=f"Humos de Lucy: {self.lucy_mood}", 
                                 bg="#e0e0e0", font=("Helvetica", 10, "bold"))
        self.mood_label.pack(side=tk.RIGHT, padx=15)
    
    def show_scene(self, scene_name):
        self.current_scene = scene_name
        self.clear_options()
        self.update_status()
        
        # Mostrar cena específica
        scene_method = getattr(self, f"scene_{scene_name}", None)
        if scene_method:
            scene_method()
        else:
            self.default_scene()
    
    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
    
    def update_status(self):
        self.affinity_label.config(text=f"Afinidade: {self.affinity}")
        self.day_label.config(text=f"Dia: {self.day}")
        self.mood_label.config(text=f"Humos de Lucy: {self.lucy_mood}")
    
    def add_option(self, text, action, args=None):
        btn = tk.Button(self.options_frame, text=text, 
                       command=lambda: action(args) if args else action,
                       bg="#4a7a8c", fg="white", 
                       font=("Helvetica", 10), padx=10, pady=5)
        btn.pack(side=tk.LEFT, padx=5, pady=5)
    
    def display_text(self, text):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        self.text_display.config(state=tk.DISABLED)
    
    def change_affinity(self, amount):
        self.affinity += amount
        self.update_mood()
        self.update_status()
    
    def update_mood(self):
        if self.affinity >= 50:
            self.lucy_mood = "apaixonada"
        elif self.affinity >= 30:
            self.lucy_mood = "feliz"
        elif self.affinity >= 10:
            self.lucy_mood = "amigável"
        elif self.affinity <= -10:
            self.lucy_mood = "irritada"
        elif self.affinity <= -30:
            self.lucy_mood = "furiosa"
        else:
            self.lucy_mood = "neutra"
    
    def next_day(self):
        self.day += 1
        if self.day > 30:
            self.show_scene("final")
        else:
            self.show_scene("novo_dia")
    
    def scene_inicio(self):
        self.display_text(
            "Bem-vinda ao campus da Universidade de Gotham, Leticia Luthor!\n\n"
            "Você acabou de se transferir para o curso de Ciência da Computação e, "
            "no seu primeiro dia, conhece Lucy Williams - uma garota inteligente, "
            "sarcástica e incrivelmente bonita que parece desprezar todos ao seu redor.\n\n"
            "Você sente uma atração imediata por ela, mas conquistar Lucy não será fácil. "
            "Você terá 30 dias para tentar conquistá-la antes que o semestre acabe.\n\n"
            "Suas escolhas afetarão o quanto Lucy gosta de você e como a história se desenvolve."
        )
        self.add_option("Começar jornada", self.show_scene, "novo_dia")
    
    def scene_novo_dia(self):
        locations = ["biblioteca", "cafeteria", "parque", "laboratorio"]
        available_locs = [loc for loc in locations if loc not in self.visited_locations]
        
        if not available_locs or random.random() < 0.3:
            available_locs = locations
            
        location = random.choice(available_locs)
        self.visited_locations.add(location)
        
        if location == "biblioteca":
            self.show_scene("biblioteca")
        elif location == "cafeteria":
            self.show_scene("cafeteria")
        elif location == "parque":
            self.show_scene("parque")
        elif location == "laboratorio":
            self.show_scene("laboratorio")
    
    def scene_biblioteca(self):
        self.display_text(
            f"Dia {self.day} - Biblioteca Universitária\n\n"
            "Você encontra Lucy na biblioteca, cercada por livros de física quântica. "
            "Ela parece profundamente concentrada, mas levanta os olhos quando você se aproxima.\n\n"
            "Lucy: 'Se você veio me perguntar sobre a lição de casa, pode esquecer. "
            "Não sou monitora de ninguém.'\n\n"
            "Como você responde?"
        )
        
        self.add_option("'Na verdade, vim te convidar para tomar um café'", 
                       lambda: self.choice_biblioteca("cafe"))
        self.add_option("'Eu só queria dizer que seu cabelo está lindo hoje'", 
                       lambda: self.choice_biblioteca("elogio"))
        self.add_option("'Desculpe, eu só estava procurando um livro sobre algoritmos'", 
                       lambda: self.choice_biblioteca("algoritmos"))
        self.add_option("Ignorar e sentar em outra mesa", 
                       lambda: self.choice_biblioteca("ignorar"))
    
    def choice_biblioteca(self, choice):
        if choice == "cafe":
            self.display_text(
                "Lucy arqueia uma sobrancelha, mas um pequeno sorriso aparece em seus lábios.\n\n"
                "Lucy: 'Ousada, hein? Normalmente recuso, mas estou precisando de uma pausa.'\n\n"
                "Vocês vão para a cafeteria juntas e passam uma hora agradável conversando sobre "
                "física e música. Lucy parece genuinamente interessada na sua opinião."
            )
            self.change_affinity(10)
        elif choice == "elogio":
            self.display_text(
                "Lucy parece surpresa e um pouco desconfiada.\n\n"
                "Lucy: 'Você está tentando ser legal ou quer algo de mim?'\n\n"
                "Você explica que estava apenas sendo sincera. Lucy parece não acreditar totalmente, "
                "mas seu tom fica um pouco mais suave."
            )
            self.change_affinity(5)
        elif choice == "algoritmos":
            self.display_text(
                "Lucy suspira e aponta para uma prateleira.\n\n"
                "Lucy: 'Lá na seção 12B. E por favor, não faça barulho.'\n\n"
                "Você pega o livro em silêncio e senta em outra mesa. Lucy ocasionalmente olha "
                "para você com curiosidade."
            )
            self.change_affinity(2)
        else:
            self.display_text(
                "Você decide não incomodar Lucy e senta em outra mesa. Ela continua estudando, "
                "mas você nota que ela olha para você algumas vezes, como se estivesse esperando "
                "que você dissesse algo."
            )
            self.change_affinity(-2)
        
        self.add_option("Continuar", self.next_day)

    # ... (adicionar aqui as outras cenas: cafeteria, parque, laboratorio, final)

    def default_scene(self):
        self.display_text("Cena não implementada ainda.")
        self.add_option("Voltar", self.show_scene, "inicio")

if __name__ == "__main__":
    root = tk.Tk()
    game = RomanceRPG(root)
    root.mainloop()