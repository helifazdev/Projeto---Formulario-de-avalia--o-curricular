import tkinter as tk
from tkinter import messagebox


def gerar_relatorios():
    # Abrir o arquivo e ler as linhas
    try:
        with open("retorno.txt", "r") as arquivo:
            linhas = arquivo.readlines()
    except FileNotFoundError:
        messagebox.showerror("Erro", "O arquivo retorno.txt não foi encontrado!")
        return

    # Processar cada linha e gerar os relatórios
    relatorios = []
    for linha in linhas:
        dados = linha.strip().split(";")
        if len(dados) != 9:
            messagebox.showwarning("Aviso", f"Dados inválidos na linha: {linha}")
            continue

        # Extrair os dados
        _, nome, inscricao, Cargo, requisito , analise_curricular,justificativa, observacao, nota = dados
        situacao = "Eliminado" if requisito == "Nao" else "Analisado"
        relatorio = (
            # Dados pessoais do candidato
            f"Nome: {nome}\n"
            f"Inscrição: {inscricao}\n"
            f"Cargo: {Cargo}\n"

            # Dados a serem analisados
            f"Possui requisito? {requisito}\n"
            f"Análise Curricular: {analise_curricular}\n"
            f"Justificativa: {justificativa}\n"
            f"Observação: {observacao}\n"
            f"Nota: {nota}\n"
            f"Situação: {situacao}\n"
            "-----------------------------"
        )
        relatorios.append(relatorio)

    # Exibir os relatórios na área de texto
    text_area.delete("1.0", tk.END)
    if relatorios:
        text_area.insert(tk.END, "\n".join(relatorios))
    else:
        text_area.insert(tk.END, "Nenhum relatório válido encontrado!")



# Criar a janela principal
root = tk.Tk()
root.title("Gerador de Relatórios")

# Definindo o ícone da janela 
root.iconbitmap("Icones/Upe.ico") 

# Layout da interface
frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Clique no botão para gerar relatórios do arquivo retorno.txt:")
label.grid(row=0, column=0, pady=(0, 10))

btn_gerar = tk.Button(frame, text="Gerar Relatórios", command=gerar_relatorios)
btn_gerar.grid(row=1, column=0, pady=(0, 10))

text_area = tk.Text(frame, height=20, width=80)
text_area.grid(row=2, column=0, pady=(10, 0))

# Iniciar o loop da interface
root.mainloop()
