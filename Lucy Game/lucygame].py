import os
import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import pygame

import pygame

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

        # Caminho absoluto da pasta de imagens
        IMG_PATH = r"C:\Users\letic\Documents\Projetos VS\Lucy Game\imgs"

        # Inicializar mixer do pygame
        pygame.mixer.init()

        self.music_muted = False # Variável para mute/desmute

        # Caminho para a trilha sonora
        MUSIC_PATH = r"C:\Users\letic\Documents\Projetos VS\Lucy Game\musicas\trilha.mp3"

        # Carregar e tocar em loop
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.play(-1)  # -1 = loop infinito

        self.lucy_images = {
        "neutra":       ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_neutra.jpg")).resize((200, 200))),
        "impassivel":   ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_impassivel.jpg")).resize((200, 200))),
        "amigável":     ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_amigavel.jpg")).resize((200, 200))),
        "sorridente":   ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_sorridente.jpg")).resize((200, 200))),
        "feliz":        ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_feliz.jpg")).resize((200, 200))),
        "encantada":    ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_encantada.jpg")).resize((200, 200))),
        "apaixonada":   ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_apaixonada.jpg")).resize((200, 200))),
        "irritada":     ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_irritada.jpg")).resize((200, 200))),
        "furiosa":      ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_furiosa.jpg")).resize((200, 200))),
        "descontrolada":ImageTk.PhotoImage(Image.open(os.path.join(IMG_PATH, "lucy_descontrolada.jpg")).resize((200, 200)))
    }

        # Configuração da interface
        self.setup_ui()

        # Iniciar jogo
        self.show_scene("inicio")
    
    def setup_ui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame para Lucy (imagem)
        self.lucy_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.lucy_frame.pack(side=tk.RIGHT, padx=20, pady=10)

        # Exibir imagem inicial de Lucy
        self.lucy_label = tk.Label(
            self.lucy_frame,
            image=self.lucy_images[self.lucy_mood],
            bg="#f0f0f0"
        )
        self.lucy_label.pack()

        # Frame de texto
        text_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Texto com Scrollbar
        self.text_display = tk.Text(
            text_frame,
            wrap=tk.WORD,
            bg="#f0f0f0",
            fg="#333333",
            font=("Helvetica", 12),
            relief="flat",
            insertbackground="#333333",
            height=15, padx=10, pady=10
        )
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.text_scrollbar = tk.Scrollbar(text_frame, bg="#f0f0f0", troughcolor="#e0e0e0")
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Conecta Scrollbar ao Text
        self.text_display.config(yscrollcommand=self.text_scrollbar.set)
        self.text_scrollbar.config(command=self.text_display.yview)
        self.text_display.config(state=tk.DISABLED)

        # Frame para opções (botões) abaixo do texto
        self.options_frame = tk.Frame(self.main_frame, bg="#f0f0f0")
        self.options_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 5))

        # Frame de status (inferior)
        self.status_frame = tk.Frame(self.root, bg="#e0e0e0", height=40)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Labels de status
        self.affinity_label = tk.Label(
            self.status_frame, text=f"Afinidade: {self.affinity}",
            bg="#e0e0e0", font=("Helvetica", 10, "bold")
        )
        self.affinity_label.pack(side=tk.LEFT, padx=15)

        self.day_label = tk.Label(
            self.status_frame, text=f"Dia: {self.day}",
            bg="#e0e0e0", font=("Helvetica", 10, "bold")
        )
        self.day_label.pack(side=tk.LEFT, padx=15)

        self.mood_label = tk.Label(
            self.status_frame, text=f"Humor de Lucy: {self.lucy_mood}",
            bg="#e0e0e0", font=("Helvetica", 10, "bold")
        )
        self.mood_label.pack(side=tk.RIGHT, padx=15)

        # Botão do modo escuro
        self.mode_button = tk.Button(
            self.status_frame, text="🌙 / ☀️", command=self.toggle_dark_mode
        )
        self.mode_button.pack(side=tk.RIGHT, padx=5)

        # Botão de volume
        self.volume_button = tk.Button(
            self.status_frame, text="🔊", command=self.toggle_volume
        )
        self.volume_button.pack(side=tk.RIGHT, padx=5)


    def toggle_dark_mode(self):
        # Alterna o modo escuro
        self.dark_mode = not getattr(self, "dark_mode", False)

        # Cores
        bg_main = "#1e1e1e" if self.dark_mode else "#FFFFFF"
        fg_text = "white" if self.dark_mode else "#333333"
        btn_bg = "#333333" if self.dark_mode else "#4a7a8c"
        bg_status = "#2e2e2e" if self.dark_mode else "#e0e0e0"
        bg_text_frame = "#1e1e1e" if self.dark_mode else "#f0f0f0"

        # Atualiza frames
        self.main_frame.config(bg=bg_main)
        self.lucy_frame.config(bg=bg_main)
        self.options_frame.config(bg=bg_main)
        self.status_frame.config(bg=bg_status)

        # Atualiza texto
        self.text_display.config(bg=bg_text_frame, fg=fg_text, insertbackground=fg_text)

        # Atualiza Scrollbar
        self.text_scrollbar.config(
            bg="#333333" if self.dark_mode else "#f0f0f0",
            troughcolor="#555555" if self.dark_mode else "#e0e0e0",
            activebackground="#555555" if self.dark_mode else "#c0c0c0"
        )

        # Atualiza labels de status
        self.affinity_label.config(bg=bg_status, fg=fg_text)
        self.day_label.config(bg=bg_status, fg=fg_text)
        self.mood_label.config(bg=bg_status, fg=fg_text)

        # Atualiza botões de escolha
        for btn in self.options_frame.winfo_children():
            btn.config(bg=btn_bg, fg=fg_text, activebackground=bg_status, activeforeground=fg_text)

        # Botões de status (modo escuro e volume)
        self.mode_button.config(bg=btn_bg, fg=fg_text, activebackground=bg_status, activeforeground=fg_text)
        self.volume_button.config(bg=btn_bg, fg=fg_text, activebackground=bg_status, activeforeground=fg_text)

    def toggle_volume(self):
        if self.music_muted:
            pygame.mixer.music.set_volume(1.0)  # liga o som
            self.volume_button.config(text="🔊")
        else:
            pygame.mixer.music.set_volume(0.0)  # silencia
            self.volume_button.config(text="🔇")
        self.music_muted = not self.music_muted

    def update_status(self):
        # Atualiza labels de afinidade, dia e humor
        self.affinity_label.config(text=f"Afinidade: {self.affinity}")
        self.day_label.config(text=f"Dia: {self.day}")
        self.mood_label.config(text=f"Humor de Lucy: {self.lucy_mood}")
        # Atualiza a imagem
        if self.lucy_mood in self.lucy_images:
            self.lucy_label.config(image=self.lucy_images[self.lucy_mood])
            self.lucy_label.image = self.lucy_images[self.lucy_mood]  # garante que o Tkinter não descarte a imagem

    def change_affinity(self, amount):
        self.affinity += amount
        self.update_mood()
        self.update_status()

    def show_scene(self, scene_name):
        self.current_scene = scene_name
        self.clear_options()
        self.update_status()
        scene_method = getattr(self, f"scene_{scene_name}", None)
        if scene_method:
            scene_method()
        else:
            self.default_scene()
    
    def clear_options(self):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
    
    def add_option(self, text, action, args=None):
        # Cria o botão
        if args is not None:
            btn = tk.Button(
                self.options_frame,
                text=text,
                command=lambda: action(args),
                bg="#4a7a8c" if not getattr(self, "dark_mode", False) else "#333333",
                fg="white",
                font=("Helvetica", 10),
                padx=10,
                pady=5
            )
        else:
            btn = tk.Button(
                self.options_frame,
                text=text,
                command=action,
                bg="#4a7a8c" if not getattr(self, "dark_mode", False) else "#333333",
                fg="white",
                font=("Helvetica", 10),
                padx=10,
                pady=5
            )

        # Alinha verticalmente abaixo do texto
        btn.pack(fill=tk.X, pady=5)

        # Atualiza cores do botão se o modo escuro estiver ativo
        if getattr(self, "dark_mode", False):
            btn.config(
                bg="#333333",
                fg="white",
                activebackground="#2e2e2e",
                activeforeground="white"
            )
    
    def update_mood(self):
        if self.affinity >= 50:
            self.lucy_mood = "apaixonada"
        elif self.affinity >= 40:
            self.lucy_mood = "encantada"
        elif self.affinity >= 30:
            self.lucy_mood = "feliz"
        elif self.affinity >= 20:
            self.lucy_mood = "sorridente"
        elif self.affinity >= 10:
            self.lucy_mood = "amigável"
        elif self.affinity >= 0:
            self.lucy_mood = "neutra"
        elif self.affinity <= -10:
            self.lucy_mood = "irritada"
        elif self.affinity <= -30:
            self.lucy_mood = "furiosa"
        elif self.affinity <= -50:
            self.lucy_mood = "descontrolada"
        else:
            self.lucy_mood = "impassivel"
    
    def next_day(self):
        self.day += 1
        if self.day > 10:
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
        self.add_option("Começar jornada", lambda: self.show_scene("novo_dia"))
    
    def scene_novo_dia(self):
        locations = ["biblioteca", "cafeteria", "parque", "laboratorio"]
        if self.affinity > 5:
            locations.append("sexo")
        available_locs = [loc for loc in locations if loc not in self.visited_locations]
        if not available_locs or random.random() < 0.3:
            available_locs = locations
        location = random.choice(available_locs)
        self.visited_locations.add(location)
        self.show_scene(location)
    
    def scene_biblioteca(self):
        self.display_text(
            f"Dia {self.day} - Biblioteca Universitária\n\n"
            "Você encontra Lucy na biblioteca, cercada por livros de física quântica. "
            "Ela parece profundamente concentrada, mas levanta os olhos quando você se aproxima.\n\n"
            "Lucy: 'Se você veio me perguntar sobre a lição de casa, pode esquecer. "
            "Não sou monitora de ninguém.'\n\n"
            "Como você responde?"
        )
        self.add_option("'Na verdade, vi você sozinha e vim te convidar para tomar um café'", 
                       lambda: self.choice_biblioteca("cafe"))
        self.add_option("'Eu só queria dizer que seu cabelo está lindo'", 
                       lambda: self.choice_biblioteca("elogio"))
        self.add_option("'Desculpe, eu só estava procurando um livro'", 
                       lambda: self.choice_biblioteca("livro"))
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

    def scene_cafeteria(self):
        self.display_text(
            f"Dia {self.day} - Cafeteria do Campus\n\n"
            "Você vê Lucy sentada sozinha na cafeteria, mexendo no celular enquanto "
            "come um sanduíche. Ela parece entediada.\n\n"
            "Quando você se aproxima, ela olha para cima com uma expressão neutra.\n\n"
            "O que você faz?"
        )
        self.add_option("Sentar à mesa dela sem perguntar", 
                       lambda: self.choice_cafeteria("sentar"))
        self.add_option("Perguntar se pode se sentar", 
                       lambda: self.choice_cafeteria("perguntar"))
        self.add_option("Comprar um café e levar para ela", 
                       lambda: self.choice_cafeteria("cafe"))
        self.add_option("Fingir que não a viu", 
                       lambda: self.choice_cafeteria("ignorar"))
    
    def choice_cafeteria(self, choice):
        if choice == "sentar":
            self.display_text(
                "Lucy parece chocada com sua audácia.\n\n"
                "Lucy: 'Você tem algum problema de compreensão de espaço pessoal ou só é mal-educada?'\n\n"
                "Antes que você possa responder, ela pega suas coisas e vai embora, "
                "mas você nota um brilho de diversão em seus olhos."
            )
            self.change_affinity(-5 if self.affinity < 20 else 5)
        elif choice == "perguntar":
            self.display_text(
                "Lucy olha para a cadeira vazia e depois para você.\n\n"
                "Lucy: 'Se eu disser não, você vai embora?' Ela faz uma pausa dramática. "
                "'Brincadeira. Pode sentar.'\n\n"
                "Vocês conversam sobre as aulas e Lucy surpreendentemente faz algumas piadas."
            )
            self.change_affinity(8)
        elif choice == "cafe":
            self.display_text(
                "Você chega na mesa com dois cafés e coloca um na frente dela.\n\n"
                "Lucy: 'Eu não pedi isso.' Ela olha desconfiada. 'O que tem nele?'\n\n"
                "Você ri e diz que é apenas café preto, como viu ela bebendo antes. "
                "Ela experimenta cautelosamente e acena com a cabeça em aprovação."
            )
            self.change_affinity(7 if self.affinity < 30 else 12)
        else:
            self.display_text(
                "Você decide não se aproximar de Lucy hoje. Enquanto pega seu lanche, "
                "você nota que ela está olhando para você com uma expressão curiosa, "
                "como se estivesse esperando algo."
            )
            self.change_affinity(-3)
        self.add_option("Continuar", self.next_day)
    
    def scene_parque(self):
        self.display_text(
            f"Dia {self.day} - Parque do Campus\n\n"
            "Você está caminhando pelo parque quando vê Lucy sentada sob uma árvore, "
            "desenhando em um caderno. Ela parece relaxada, diferente de sua postura "
            "habitualmente tensa.\n\n"
            "Quando ela percebe sua presença, fecha rapidamente o caderno, mas não "
            "parece irritada como de costume.\n\n"
            "O que você faz?"
        )
        self.add_option("Perguntar o que ela está desenhando", 
                       lambda: self.choice_parque("desenho"))
        self.add_option("Sentar em silêncio perto dela", 
                       lambda: self.choice_parque("sentar"))
        self.add_option("Dizer que o parque está bonito hoje", 
                       lambda: self.choice_parque("parque"))
        self.add_option("Ir embora sem dizer nada", 
                       lambda: self.choice_parque("sair"))
    
    def choice_parque(self, choice):
        if choice == "desenho":
            self.display_text(
                "Lucy inicialmente parece defensiva, mas depois suspira.\n\n"
                "Lucy: 'São apenas... esboços. Nada especial.' Ela hesita, "
                "mas então abre o caderno mostrando desenhos incríveis de paisagens.\n\n"
                "Lucy: 'Não conte para ninguém. Não quero que me importunem sobre isso.'\n\n"
                "Você promete guardar o segredo e elogia seu talento. Lucy parece genuinamente "
                "agradecida, um raro sorriso aparecendo em seu rosto."
            )
            self.change_affinity(15)
        elif choice == "sentar":
            self.display_text(
                "Você se senta a uma distância respeitosa e fica em silêncio, "
                "apreciando a paisagem. Depois de alguns minutos, Lucy fala sem olhar para você:\n\n"
                "Lucy: 'Você é estranha. A maioria das pessoas não consegue ficar quieta.'\n\n"
                "Ela não parece incomodada, apenas observadora. Depois de um tempo, "
                "ela volta a desenhar, mas não fecha o caderno desta vez."
            )
            self.change_affinity(10)
        elif choice == "parque":
            self.display_text(
                "Lucy olha ao redor e concorda com a cabeça.\n\n"
                "Lucy: 'É por isso que vim aqui. É um dos poucos lugares tranquilos "
                "nesse campus cheio de idiotas.'\n\n"
                "Ela parece considerar algo por um momento.\n\n"
                "Lucy: 'Se você quiser, pode sentar. Mas sem conversa fiada.'"
            )
            self.change_affinity(7)
        else:
            self.display_text(
                "Você decide não incomodar Lucy e continua seu caminho. "
                "Quando olha para trás, vê que ela está observando você sair "
                "com uma expressão que você não consegue decifrar."
            )
            self.change_affinity(-2)
        self.add_option("Continuar", self.next_day)
    
    def scene_laboratorio(self):
        self.display_text(
            f"Dia {self.day} - Laboratório de Computação\n\n"
            "Você está trabalhando em um projeto quando Lucy entra no laboratório, "
            "parecendo frustrada. Ela joga sua mochila em uma mesa e começa a digitar "
            "furiosamente no computador.\n\n"
            "Depois de alguns minutos, ela solta um palavrão alto o suficiente para "
            "que todos no laboratório ouçam.\n\n"
            "O que você faz?"
        )
        self.add_option("Oferecer ajuda", 
                       lambda: self.choice_laboratorio("ajuda"))
        self.add_option("Perguntar educadamente se ela pode fazer menos barulho", 
                       lambda: self.choice_laboratorio("barulho"))
        self.add_option("Levar um copo d'água para ela", 
                       lambda: self.choice_laboratorio("agua"))
        self.add_option("Ignorar e continuar trabalhando", 
                       lambda: self.choice_laboratorio("ignorar"))
    
    def choice_laboratorio(self, choice):
        if choice == "ajuda":
            if self.affinity < 10:
                self.display_text(
                    "Lucy olha para você com desdém.\n\n"
                    "Lucy: 'Oh, por favor. Você nem sabe qual é o problema.'\n\n"
                    "Ela vira as costas e continua trabalhando, claramente irritada."
                )
                self.change_affinity(-5)
            else:
                self.display_text(
                    "Lucy suspira e explica o problema com seu código. "
                    "Você sugere uma solução que ela não havia considerado.\n\n"
                    "Lucy: 'Hmm... isso pode funcionar.' Ela implementa sua sugestão "
                    "e o código funciona. Lucy olha para você com novo respeito.\n\n"
                    "Lucy: 'Não é todo dia que alguém me surpreende. Obrigada.'"
                )
                self.change_affinity(15)
        elif choice == "barulho":
            self.display_text(
                "Lucy vira para você com olhos furiosos.\n\n"
                "Lucy: 'Oh, desculpe por incomodar sua programação perfeita com "
                "meus problemas reais!' Ela pega suas coisas e sai batendo a porta.\n\n"
                "Parece que você tocou em um nervo sensível."
            )
            self.change_affinity(-10)
        elif choice == "agua":
            self.display_text(
                "Você coloca um copo d'água silenciosamente na mesa dela. "
                "Lucy olha para o copo, depois para você, e depois de um momento "
                "bebe um gole.\n\n"
                "Lucy: 'Obrigada.' É tudo que ela diz, mas sua voz está menos áspera.\n\n"
                "Depois de alguns minutos, ela pergunta: 'Você sabe algo sobre "
                "algoritmos de ordenação?'"
            )
            self.change_affinity(8)
        else:
            self.display_text(
                "Você decide não se envolver e continua trabalhando. "
                "Depois de um tempo, Lucy resolve seu problema e sai do laboratório. "
                "Ao passar por você, ela parece um pouco decepcionada por você não "
                "ter dito nada."
            )
            self.change_affinity(-3)
        self.add_option("Continuar", self.next_day)

    def scene_sexo(self):
        self.display_text(
            f"Dia {self.day} - Festa na Casa do Mike\n\n"
            "Você chega à festa e logo encontra Lucy, que parece estar se divertindo. "
            "Ela está cercada por amigos, mas quando te vê, seu rosto se ilumina.\n\n"
            "'Ei! Você veio!', ela exclamou, puxando você para mais perto.\n\n"
            "A música está alta e a atmosfera é animada. O que você faz?"
        )
        self.add_option("Oferecer uma bebida", 
                       lambda: self.choice_sexo("bebida"))
        self.add_option("Perguntar se ela quer dançar", 
                       lambda: self.choice_sexo("dançar"))
        self.add_option("Tentar beija-la", 
                       lambda: self.choice_sexo("beijar"))
        self.add_option("Ignorar e continuar bebendo", 
                       lambda: self.choice_sexo("ignorar"))
        
    def choice_sexo(self, choice):
        if choice == "bebida":
            if self.affinity < 10:
                self.display_text(
                    "Lucy olha para você com um sorriso irônico.\n\n"
                    "Lucy: 'Você realmente acha que eu aceitaria uma bebida de alguém que mal conheço?'\n\n"
                    "Ela recusa educadamente, mas você percebe que ela aprecia sua iniciativa, mesmo que não demonstre."
                )
                self.change_affinity(-5)
            else:
                self.display_text(
                    "Lucy aceita a bebida com um sorriso genuíno.\n\n"
                    "Lucy: 'Obrigada. Você sabe como animar uma festa.'\n\n"
                    "Vocês brindam juntas e, entre risadas e conversas, a conexão entre vocês fica ainda mais forte. "
                    "Lucy se aproxima, tocando levemente sua mão, e você sente que ela está realmente confortável ao seu lado."
                )
                self.change_affinity(15)
        elif choice == "dançar":
            if self.affinity > 20:
                self.display_text(
                    "Lucy hesita por um momento, depois sorri de forma inesperada.\n\n"
                    "Lucy: 'Você quer dançar comigo? Não esperava por isso.'\n\n"
                    "Ela aceita seu convite e vocês vão para a pista de dança. "
                    "No começo, Lucy parece um pouco tímida, mas logo se solta e vocês se divertem juntas.\n\n"
                    "Durante a dança, Lucy se aproxima e sussurra:\n\n"
                    "'Você está me surpreendendo hoje.'\n\n"
                    "A conexão entre vocês fica mais intensa, e o clima entre vocês esquenta."
                )
                self.change_affinity(12)
            else:
                self.display_text(
                    "Lucy olha para você com uma expressão confusa.\n\n"
                    "Lucy: 'Dançar? Com você? Acho que você está se enganando.'\n\n"
                    "Ela recusa educadamente, mas você percebe que ela não está interessada em se aproximar mais."
                )
                self.change_affinity(-5)
        elif choice == "beijar":
            if self.affinity > 30:
                self.display_text(
                    "Lucy olha para você surpresa, mas não recua.\n\n"
                    "Lucy: 'Você é realmente ousada, hein?'\n\n"
                    "Ela sorri e se inclina para te beijar. O beijo é intenso e cheio de emoção, "
                    "e você sente que finalmente conquistou o coração dela.\n\n"
                    "Depois do beijo, Lucy segura sua mão e diz:\n\n"
                    "'Eu acho que podemos tentar algo mais sério.'\n\n"
                    "Vocês passam o resto da noite juntas, aproveitando a companhia uma da outra."
                    "\n\nMais tarde, vocês vão para um lugar mais reservado. Lucy te olha nos olhos, "
                    "com um sorriso tímido, e se aproxima ainda mais. O clima entre vocês esquenta, "
                    "e a paixão toma conta do momento. Vocês se entregam uma à outra, compartilhando "
                    "carícias e beijos intensos, em uma noite inesquecível de amor e conexão."
                )
                self.change_affinity(20)
            else:
                self.display_text(
                    "Lucy recua rapidamente, olhando para você com olhos furiosos.\n\n"
                    "Lucy: 'Isso é inapropriado! Você está se passando dos limites.'\n\n"
                    "Ela se afasta de você e não quer mais falar. Parece que você estragou suas chances."
                )
                self.change_affinity(-15)
        elif choice == "ignorar":
            if self.affinity > 30:
                self.display_text(
                    "Você decide ignorar Lucy e continua aproveitando a festa por conta própria. "
                    "Enquanto conversa com outras pessoas, percebe que Lucy observa você de longe, "
                    "com uma expressão indecifrável. Ela parece hesitar, dá alguns passos em sua direção, "
                    "mas acaba desistindo e retorna para o grupo de amigos, claramente desapontada. "
                    "Talvez ela esperasse que você se aproximasse, mas agora parece distante e desinteressada."
                )
                self.change_affinity(-8)
            else:
                self.display_text(
                    "Você decide ignorar Lucy e continua aproveitando a festa por conta própria. "
                    "Enquanto conversa com outras pessoas, percebe que Lucy observa você de longe, "
                    "com uma expressão indecifrável. Talvez ela esperasse que você se aproximasse, "
                    "mas agora parece distante e desinteressada."
                )
                self.change_affinity(0)
        else:
            self.display_text(
                "Sua escolha não foi reconhecida. Tente novamente."
            )
            self.change_affinity(0)
        self.add_option("Continuar", self.next_day)
    
    def scene_final(self):
        if self.affinity >= 50:
            self.display_text(
                f"Dia {self.day} - Fim do Semestre\n\n"
                "Com o semestre terminando, você convida Lucy para sair e, para sua surpresa, "
                "ela aceita. Vocês vão para um café fora do campus e passam horas conversando.\n\n"
                "No final da noite, Lucy pega sua mão e diz:\n\n"
                "'Eu nunca pensei que diria isso, mas... você é a única pessoa que "
                "realmente me entende nesse lugar.'\n\n"
                "Ela se inclina e te dá um beijo suave. Parece que seus esforços valeram a pena!\n\n"
                "FINAL ROMÂNTICO: VOCÊ CONQUISTOU LUCY WILLIAMS!"
            )
        elif self.affinity >= 30:
            self.display_text(
                f"Dia {self.day} - Fim do Semestre\n\n"
                "No último dia de aula, Lucy se aproxima de você.\n\n"
                "'Olha, eu não sou boa com despedidas', ela diz, evitando seu olhar. "
                "'Mas você não é tão ruim quanto a maioria das pessoas aqui.'\n\n"
                "Ela te dá um abraço rápido e sai antes que você possa responder. "
                "Talvez no próximo semestre vocês possam se aproximar mais.\n\n"
                "FINAL BOM: LUCY CONSIDERA VOCÊ UMA AMIGA"
            )
        elif self.affinity >= 10:
            self.display_text(
                f"Dia {self.day} - Fim do Semestre\n\n"
                "O semestre termina sem grandes acontecimentos entre você e Lucy. "
                "Vocês trocam um aceno casual no último dia, mas nada mais.\n\n"
                "Talvez com mais tempo e esforço você pudesse ter se aproximado dela, "
                "mas pelo menos ela não te odeia.\n\n"
                "FINAL NEUTRO: VOCÊS PERMANECEM COLEGAS"
            )
        else:
            self.display_text(
                f"Dia {self.day} - Fim do Semestre\n\n"
                "No último dia, Lucy passa por você no corredor e faz uma careta.\n\n"
                "'Finalmente não vou mais ter que te ver todo dia', ela murmura, "
                "suficientemente alto para você ouvir.\n\n"
                "Parece que suas tentativas de se aproximar só a afastaram mais. "
                "Melhor sorte na próxima vida acadêmica!\n\n"
                "FINAL RUIM: LUCY NÃO SUPORTA VOCÊ"
            )
        self.add_option("Jogar novamente", self.restart_game)
        self.add_option("Sair", self.root.quit)
    
    def restart_game(self):
        self.affinity = 0
        self.day = 1
        self.visited_locations = set()
        self.choices_made = {}
        self.lucy_mood = "neutra"
        self.show_scene("inicio")
    
    def display_text(self, text):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        self.text_display.config(state=tk.DISABLED)

    def default_scene(self):
        self.display_text("Cena não implementada ainda.")
        self.add_option("Voltar", lambda: self.show_scene("novo_dia"))

if __name__ == "__main__":
    root = tk.Tk()
    game = RomanceRPG(root)
    root.mainloop()
