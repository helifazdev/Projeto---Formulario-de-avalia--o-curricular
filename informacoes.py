# informacoes.py

def obter_candidatos():
    candidatos = []
    try:
        with open("Dados.txt", "r") as arquivo:
            for linha in arquivo:
                dados = linha.strip().split(";")
                candidato = {
                    "nome": dados[1].replace('"', ''),  # Remove aspas
                    "inscricao": dados[3].replace('"', ''),  # Remove aspas
                    "cargo": dados[5].replace('"', '')  # Remove aspas
                }
                candidatos.append(candidato)
    except FileNotFoundError:
        print("Arquivo Dados.txt não encontrado. Certifique-se de que o arquivo existe e tente novamente.")
    return candidatos
