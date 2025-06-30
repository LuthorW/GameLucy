import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
import pygame
import os

# Inicializar mixer para som
pygame.mixer.init()

# --- Funções de áudio ---
def tocar_musica():
    caminho = "musica.mp3"  # Certifique-se de ter esse arquivo
    if os.path.exists(caminho):
        pygame.mixer.music.load(caminho)
        pygame.mixer.music.play(-1)  # Loop infinito

def parar_musica():
    pygame.mixer.music.stop()

# --- Dados iniciais ---
afinidade = 0
cena_atual = 0
save_file = "save.txt"

# --- Cenas do jogo ---
cenas = [
    {
        "texto": "Você vê Lucy do outro lado do campus. Ela parece concentrada, lendo algo no celular.",
        "opcoes": [
            {"texto": "Ir até ela com confiança", "pontos": 10, "resposta": "Lucy levanta os olhos e sorri de lado: 'Sempre tão ousada, hein?'"},
            {"texto": "Observar de longe", "pontos": 0, "resposta": "Você hesita, e Lucy vai embora antes que você possa decidir."},
            {"texto": "Gritar o nome dela de longe", "pontos": -10, "resposta": "Lucy olha assustada, depois sorri com um pouco de vergonha: 'Letícia, você me assustou!'"},
        ]
    },
    {
        "texto": "Lucy está sentada no café da faculdade. Você se aproxima e ela sorri levemente. O que você faz?",
        "opcoes": [
            {"texto": "Elogiar o sorriso dela", "pontos": 20, "resposta": "Lucy cora, mas disfarça com um gole de café."},
            {"texto": "Fazer piada sobre café amargo como ela", "pontos": 10, "resposta": "Ela ri de leve: 'Pelo menos alguém entende meu drama.'"},
            {"texto": "Dizer que ela parece cansada", "pontos": -10, "resposta": "Lucy revira os olhos: 'Obrigada por me lembrar, Letícia.'"},
        ]
    },
    {
        "texto": "Vocês estão na biblioteca. Lucy está focada estudando. Como você interrompe?",
        "opcoes": [
            {"texto": "Deixar um bilhete divertido no livro dela", "pontos": 15, "resposta": "Ela lê, morde o lábio pra não rir, e te encara com um olhar curioso."},
            {"texto": "Oferecer ajuda com a matéria", "pontos": 10, "resposta": "'Você sabe mesmo isso tudo?' Lucy pergunta, surpresa."},
            {"texto": "Tocar no ombro dela abruptamente", "pontos": -15, "resposta": "Ela se assusta: 'Letícia! Que susto! Não faça isso!'"},
        ]
    },
    {
        "texto": "No jardim da faculdade, Lucy está lendo um livro de romance. Você se senta ao lado dela.",
        "opcoes": [
            {"texto": "Perguntar sobre o livro com interesse genuíno", "pontos": 20, "resposta": "Ela sorri, animada: 'Você quer mesmo saber? É raro alguém perguntar isso.'"},
            {"texto": "Brincar dizendo que aquilo é 'coisa de gente sensível demais'", "pontos": -10, "resposta": "Lucy fecha o livro lentamente: 'Você leu algum ou só está tirando sarro?'"},
            {"texto": "Dizer que ela combina com aquele tipo de história", "pontos": 15, "resposta": "Lucy sorri, tocada: 'Você acha? Nunca pensei nisso.'"},
        ]
    }
]

# --- Funções principais ---
def escolher_opcao(pontos, resposta):
    global afinidade, cena_atual
    afinidade += pontos
    texto_resposta.set(resposta)
    barra_afinidade['value'] = afinidade
    salvar_progresso()

    if afinidade >= 100:
        messagebox.showinfo("Final Feliz ❤️", "Lucy toca a mão de Letícia: 'Acho que finalmente estou pronta pra isso... com você.'")
        root.quit()
    elif afinidade <= -50:
        messagebox.showinfo("Rejeição 💔", "Lucy cruza os braços, decepcionada: 'Não sei o que você quer, Letícia... mas não é comigo.'")
        root.quit()
    else:
        cena_atual += 1
        if cena_atual < len(cenas):
            carregar_cena()
        else:
            if afinidade >= 50:
                messagebox.showinfo("Final Amizade 💙", "Lucy sorri: 'Talvez não seja amor... ainda. Mas eu gosto de estar com você, Letícia.'")
            else:
                messagebox.showinfo("Final Inconclusivo 🤷‍♀️", "Lucy: 'Talvez em outra vida...'")
            root.quit()

def carregar_cena():
    cena = cenas[cena_atual]
    texto.set(cena["texto"])
    opcoes = cena["opcoes"]
    botao1.config(text=opcoes[0]["texto"], command=lambda: escolher_opcao(opcoes[0]["pontos"], opcoes[0]["resposta"]))
    botao2.config(text=opcoes[1]["texto"], command=lambda: escolher_opcao(opcoes[1]["pontos"], opcoes[1]["resposta"]))
    botao3.config(text=opcoes[2]["texto"], command=lambda: escolher_opcao(opcoes[2]["pontos"], opcoes[2]["resposta"]))
    texto_resposta.set("")

def salvar_progresso():
    with open(save_file, "w") as f:
        f.write(f"{cena_atual}\n{afinidade}")

def carregar_progresso():
    global cena_atual, afinidade
    if os.path.exists(save_file):
        with open(save_file, "r") as f:
            linhas = f.readlines()
            if len(linhas) >= 2:
                cena_atual = int(linhas[0])
                afinidade = int(linhas[1])

# --- Interface ---
root = tk.Tk()
root.title("Conquistando Lucy")
root.geometry("600x600")
carregar_progresso()
tocar_musica()

texto = tk.StringVar()
texto.set("")
texto_resposta = tk.StringVar()
texto_resposta.set("")

frame_texto = tk.Frame(root)
frame_texto.pack(pady=20)

label_texto = tk.Label(frame_texto, textvariable=texto, wraplength=550, font=("Helvetica", 12))
label_texto.pack()

frame_resposta = tk.Frame(root)
frame_resposta.pack(pady=10)

label_resposta = tk.Label(frame_resposta, textvariable=texto_resposta, fg="blue", wraplength=500, font=("Helvetica", 11, "italic"))
label_resposta.pack()

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=20)

botao1 = tk.Button(frame_botoes, text="Opção 1", width=50)
botao1.grid(row=0, column=0, padx=5, pady=5)

botao2 = tk.Button(frame_botoes, text="Opção 2", width=50)
botao2.grid(row=1, column=0, padx=5, pady=5)

botao3 = tk.Button(frame_botoes, text="Opção 3", width=50)
botao3.grid(row=2, column=0, padx=5, pady=5)

barra_afinidade = Progressbar(root, length=300, maximum=100)
barra_afinidade.pack(pady=10)

# Menu
menu_bar = tk.Menu(root)
opcoes_menu = tk.Menu(menu_bar, tearoff=0)
opcoes_menu.add_command(label="Salvar", command=salvar_progresso)
opcoes_menu.add_command(label="Sair", command=root.quit)
menu_bar.add_cascade(label="Menu", menu=opcoes_menu)
root.config(menu=menu_bar)

# Iniciar jogo
carregar_cena()
root.mainloop()
