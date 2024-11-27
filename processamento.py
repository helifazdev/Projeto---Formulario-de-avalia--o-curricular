# processamento.py

import unicodedata

def remover_acentos(texto):
    return ''.join((c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn'))

def salvar_informacoes(id, nome, numero, cargo, requisito, avaliacao, justificativa, observacoes, pontuacao):
    nome = remover_acentos(nome)
    justificativa = remover_acentos(justificativa)
    observacoes = remover_acentos(observacoes)
    
    with open("retorno.txt", "a") as arquivo:
        arquivo.write(f"{id};{nome};{numero};{cargo};{requisito};{avaliacao};{justificativa};{observacoes};{pontuacao}\n")
