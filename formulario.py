import tkinter as tk
from tkinter import messagebox
from informacoes import obter_candidatos
from processamento import salvar_informacoes
from datetime import datetime
import tkinter.font as tkFont

#tela de entrada
def criar_tela_entrada():
    root = tk.Tk()
    root.title("IAUPE Curricular")
    root.geometry("600x400")  # Define o tamanho da janela
    
    # Centralizar os elementos na tela
    canvas = tk.Canvas(root, width=600, height=4000, bg="#f0f0f0")
    canvas.pack()

    # Configurar a tela para sempre abrir em tela cheia
    root.state('zoomed')

    # Adicionar o logo (substitua o caminho pelo caminho real do seu arquivo de imagem)
    logo = tk.PhotoImage(file="Logos/IAUPE25-x3.png")
    canvas.create_image(300, 150, image=logo)
    
    # Adicionar o nome da empresa
    canvas.create_text(300, 300, text="IAUPE CONCURSOS", font=("Arial", 24, "bold"), fill="blue")

    # Adicionar o nome do processo
    canvas.create_text(300, 350, text="Análise Curricular - UPE 2025", font=("Arial", 24, "bold"), fill="red")


    # Definindo o ícone da janela
    root.iconbitmap("Icones/Upe.ico") 

    # Agendar a troca de tela após 5 segundos
    root.after(1000, lambda: abrir_proxima_tela(root))
    root.mainloop()

# Função para fechar a tela de entrada e abrir a próxima
def abrir_proxima_tela(root):
    root.destroy()  # Fecha a tela de entrada


# Chama a função para criar a tela de entrada
criar_tela_entrada()

# Variáveis globais e inicialização dos candidatos
candidatos = obter_candidatos() 
indice_atual = 0
pontuacoes = {"Especializacao": 40, "Mestrado": 60, "Doutorado": 10, "Nao possui": 0}
total_candidatos = len(candidatos)
data_hoje = datetime.now().strftime("%d/%m/%Y")

# Função para atualizar o formulário com os dados do candidato atual
def atualizar_formulario():
    global indice_atual
    if 0 <= indice_atual < total_candidatos:
        candidato = candidatos[indice_atual]
        
        # Dados pessoais do candidato
        nome_var.set(candidato.get("nome", ""))
        numero_var.set(candidato.get("inscricao", ""))
        cargo_var.set(candidato.get("cargo", ""))
        
        # Dados a serem analisados
        requisito_var.set(candidato.get("requisito", ""))
        avaliacao_var.set(candidato.get("avaliacao", ""))
        observacoes_text.delete("1.0", tk.END)
        observacoes_text.insert(tk.END, candidato.get("observacao", ""))
        
        justificar_frame.grid_remove()
        rodape_var.set(f"Candidato {indice_atual + 1} de {total_candidatos} | Data: {data_hoje}")
        
        if candidato.get("avaliacao") == "Nao possui":
            exibir_justificativa("Nao possui")
            justificativa_var.set(candidato.get("justificativa", ""))
    else:
        messagebox.showinfo("Fim", "Todos os candidatos foram analisados.")
        root.quit()



# Função para salvar as informações dos candidatos
def submit():
    global indice_atual
    candidato_id = indice_atual + 1
 # Dados pessoais do candidato
    nome = nome_entry.cget("text")
    numero = numero_entry.cget("text")
    cargo = cargo_entry.cget("text")
        
 # Dados a serem analisados
    requisito = requisito_var.get()
    avaliacao = avaliacao_var.get()
    observacoes = observacoes_text.get("1.0", tk.END).strip()
    pontuacao = pontuacoes.get(avaliacao, 0)
       
    justificativa = justificativa_var.get() if avaliacao == "Nao possui" else ""

    salvar_informacoes(candidato_id, nome, numero, cargo, requisito, avaliacao, justificativa, observacoes, pontuacao)

    messagebox.showinfo("Informações", f"Nome do candidato: {nome}\nNúmero de inscrição: {numero}\nCargo: {cargo}\nPossui requisito? {requisito}\nAvaliação curricular: {avaliacao}\nJustificativa: {justificativa}\nObservações: {observacoes}\nPontuação: {pontuacao}")
 
# Função para avançar para o próximo candidato
def proximo():
    global indice_atual
    resposta = messagebox.askquestion("Confirmação", "Deseja enviar o atual?")
    if resposta == 'yes':
        submit()
        submit_button.config(state="normal")
        if indice_atual < len(candidatos) - 1:
            indice_atual += 1
            atualizar_formulario()
    elif resposta == 'no':
        if indice_atual < len(candidatos) - 1:
            indice_atual += 1
            atualizar_formulario()


# Função para voltar para o candidato anterior
def anterior():
    global indice_atual
    if indice_atual > 0:
        indice_atual -= 1
        atualizar_formulario()


# Criando a janela principal
root = tk.Tk()
root.title("IAUPE CONCURSOS - Análise curricular UPE 2025")

# Ajustar o tamanho da letra
root.option_add("*Font", "Helvetica")

# Configurar a tela para sempre abrir em tela cheia
root.state('zoomed')

# Criando o rodapé
rodape_var = tk.StringVar()
rodape_label = tk.Label(root, textvariable=rodape_var)
rodape_label.grid(row=20, columnspan=2, padx=10, pady=5)

# Definindo o ícone da janela
root.iconbitmap("Icones/Upe.ico")

#Dados pessoais do candidato

# Criando e posicionando os widgets
tk.Label(root, text="Nome do candidato:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
nome_var = tk.StringVar()
nome_entry = tk.Label(root, textvariable=nome_var)
nome_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Número de inscrição:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
numero_var = tk.StringVar()
numero_entry = tk.Label(root, textvariable=numero_var)
numero_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="Cargo/Função:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
cargo_var = tk.StringVar()
cargo_entry = tk.Label(root, textvariable=cargo_var)
cargo_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

#Dados a serem analisado do candidato

tk.Label(root, text="Possui Requisitos para o cargo:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
requisito_var = tk.StringVar()  # Variável sem valor padrão
requisito = ["Sim", "Nao"]
for idx, val in enumerate(requisito):
   tk.Radiobutton(root, text=val, variable=requisito_var, value=val, command=lambda:
                   exibir_justificativa(requisito_var.get())).grid(row=3+idx, column=1, padx=10, pady=5, sticky="w")    

tk.Label(root, text="Avaliação curricular:").grid(row=8, column=0, padx=10, pady=10, sticky="w")
avaliacao_var = tk.StringVar()  # Variável sem valor padrão
avaliacoes = ["Especializacao", "Mestrado", "Doutorado", "Nao possui"]
for idx, val in enumerate(avaliacoes):
    tk.Radiobutton(root, text=val, variable=avaliacao_var, value=val, command=lambda:
                   exibir_justificativa(avaliacao_var.get())).grid(row=8+idx, column=1, padx=10, pady=5, sticky="w")


justificativa_var = tk.StringVar()
justificar_frame = tk.Frame(root)
justificar_frame.grid(row=9, column=1, padx=10, pady=5, sticky="w")

tk.Label(root, text="").grid(row=9, column=0, padx=10, pady=5)

# Função para exibir justificativas se necessário
def exibir_justificativa(avaliacao):
    if avaliacao == "Nao possui":
        justificar_frame.grid(row=12, column=1, padx=10, pady=5, sticky="w")
        justificativas = ["Nao enviou documentacao", "Documentacao ilegivel", "Documentacao invalida"]
        for widget in justificar_frame.winfo_children():
            widget.destroy()
        for idx, val in enumerate(justificativas):
            tk.Radiobutton(justificar_frame, text=val, variable=justificativa_var, value=val).pack(anchor='w')
    else:
        justificativa_var.set("")
        justificar_frame.grid_remove()

tk.Label(root, text="Observações:").grid(row=14, column=0, padx=10, pady=5)
observacoes_text = tk.Text(root, height=5, width=40)
observacoes_text.grid(row=14, column=1, padx=10, pady=5)

justificar_frame = tk.Frame(root)
justificar_frame.grid(row=10, column=1, padx=10, pady=5, sticky="w")
tk.Label(root, text="").grid(row=10, column=0, padx=10, pady=5)



# Botões de navegação
anterior_button = tk.Button(root, text="Anterior", command=anterior)
anterior_button.grid(row=15, column=0, padx=0, pady=0)

proximo_button = tk.Button(root, text="Próximo", command=proximo)
proximo_button.grid(row=15, column=1, padx=0, pady=0)

# Botão para enviar os dados
submit_button = tk.Button(root, text="Enviar", command=submit)
submit_button.grid(row=16, column=3, padx=10, pady=10)

# Inicializando o formulário com o primeiro candidato
atualizar_formulario()

# Iniciando o loop principal
root.mainloop()
