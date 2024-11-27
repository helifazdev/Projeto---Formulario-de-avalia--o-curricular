import tkinter as tk
from tkinter import messagebox
from informacoes import obter_candidatos
from processamento import salvar_informacoes

candidatos = obter_candidatos()
indice_atual = 0
pontuacoes = {"Especializacao": 40, "Mestrado": 60, "Doutorado": 10, "Nao possui": 0}


def atualizar_formulario():
    global indice_atual
    if indice_atual < len(candidatos):
        candidato = candidatos[indice_atual]
        nome_var.set(candidato["nome"])
        numero_var.set(candidato["inscricao"])
        avaliacao_var.set("")  # Limpa a seleção da avaliação
        observacoes_text.delete("1.0", tk.END)  # Limpa o texto das observações
        justificar_frame.grid_remove()
    else:
        messagebox.showinfo("Fim", "Todos os candidatos foram analisados.")
        root.quit()

def submit():
    global indice_atual
    candidato_id = indice_atual + 1
    nome = nome_entry.cget("text")
    numero = numero_entry.cget("text")
    avaliacao = avaliacao_var.get()
    observacoes = observacoes_text.get("1.0", tk.END).strip()
    pontuacao = pontuacoes.get(avaliacao, 0)

    # Verificação para garantir que o campo "Avaliação" esteja preenchido
    if not avaliacao:
        messagebox.showwarning("Aviso", "Por favor, selecione uma avaliação antes de passar para o próximo candidato.")
        return

    if avaliacao == "Nao possui" and not justificativa_var.get():
        messagebox.showwarning("Erro", "Por favor, selecione uma justificativa.")
        return

    justificativa = justificativa_var.get() if avaliacao == "Nao possui" else ""
    salvar_informacoes(candidato_id, nome, numero, avaliacao, justificativa, observacoes, pontuacao)
    messagebox.showinfo("Informações", f"Nome do candidato: {nome}\nNúmero de inscrição: {numero}\nAvaliação curricular: {avaliacao}\nJustificativa: {justificativa}\nObservações: {observacoes}\nPontuação: {pontuacao}")
    indice_atual += 1
    atualizar_formulario()

  


# Criando a janela principal
root = tk.Tk()
root.title("Formulário")

# Definindo o ícone da janela 
root.iconbitmap("Upe.ico") # Substitua "caminho/para/seu/icone.ico" pelo caminho real do seu ícone

# Criando e posicionando os widgets
tk.Label(root, text="Nome do candidato:").grid(row=0, column=0, padx=10, pady=5)
nome_var = tk.StringVar()
nome_entry = tk.Label(root, textvariable=nome_var, relief="solid")
nome_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Número de inscrição:").grid(row=1, column=0, padx=10, pady=5)
numero_var = tk.StringVar()
numero_entry = tk.Label(root, textvariable=numero_var, relief="solid")
numero_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Avaliação curricular:").grid(row=2, column=0, padx=10, pady=5)
avaliacao_var = tk.StringVar()  # Variável sem valor padrão
avaliacoes = ["Especializacao", "Mestrado", "Doutorado", "Nao possui"]
for idx, val in enumerate(avaliacoes):
    tk.Radiobutton(root, text=val, variable=avaliacao_var, value=val, command=lambda: exibir_justificativa(avaliacao_var.get())).grid(row=2+idx, column=1, padx=10, pady=5, sticky="w")

justificativa_var = tk.StringVar()
justificar_frame = tk.Frame(root)
justificar_frame.grid(row=6, column=1, padx=10, pady=5, sticky="w")
tk.Label(root, text="Justificativa:").grid(row=6, column=0, padx=10, pady=5)

def exibir_justificativa(avaliacao):
    if avaliacao == "Nao possui":
        justificar_frame.grid()
        justificativas = ["Nao enviou documentacao", "Documentacao ilegivel", "Documentacao invalida"]
        for widget in justificar_frame.winfo_children():
            widget.destroy()
        for idx, val in enumerate(justificativas):
            tk.Radiobutton(justificar_frame, text=val, variable=justificativa_var, value=val).pack(anchor='w')
    else:
        justificativa_var.set("")
        justificar_frame.grid_remove()

tk.Label(root, text="Observacoes:").grid(row=9, column=0, padx=10, pady=5)
observacoes_text = tk.Text(root, height=5, width=40)
observacoes_text.grid(row=9, column=1, padx=10, pady=5)

submit_button = tk.Button(root, text="Enviar", command=submit)
submit_button.grid(row=10, columnspan=2, pady=10)

# Inicializando o formulário com o primeiro candidato
atualizar_formulario()

# Iniciando o loop principal
root.mainloop()
