from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from informacoes import obter_candidatos
from processamento import salvar_informacoes

app = Flask(__name__)

candidatos = obter_candidatos()
indice_atual = 0
total_candidatos = len(candidatos)
data_hoje = datetime.now().strftime("%d/%m/%Y")
pontuacoes = {"Especializacao": 40, "Mestrado": 60, "Doutorado": 10, "Nao possui": 0}

@app.route('/')
def index():
    global indice_atual, candidatos, total_candidatos, data_hoje
    if indice_atual < total_candidatos:
        candidato = candidatos[indice_atual]
        return render_template('index.html', candidato=candidato, total=total_candidatos, atual=indice_atual + 1, data=data_hoje)
    else:
        return "Todos os candidatos foram analisados."

@app.route('/submit', methods=['POST'])
def submit():
    global indice_atual
    nome = request.form['nome']
    numero = request.form['numero']
    avaliacao = request.form['avaliacao']
    observacoes = request.form['observacoes']
    pontuacao = pontuacoes.get(avaliacao, 0)

    if not avaliacao:
        return "Por favor, selecione uma avaliação.", 400

    justificativa = request.form.get('justificativa', '')
    if avaliacao == "Nao possui" and not justificativa:
        return "Por favor, selecione uma justificativa.", 400

    candidato_id = indice_atual + 1
    salvar_informacoes(candidato_id, nome, numero, avaliacao, justificativa, observacoes, pontuacao)
    candidatos[indice_atual].update({"avaliacao": avaliacao, "justificativa": justificativa, "observacao": observacoes, "pontuacao": pontuacao})
    indice_atual += 1

    return redirect(url_for('index'))

@app.route('/anterior', methods=['POST'])
def anterior():
    global indice_atual
    if indice_atual > 0:
        indice_atual -= 1
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
