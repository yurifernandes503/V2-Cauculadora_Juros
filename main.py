from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# Funções de cálculo de juros
def calcular_juros_simples(principal, taxa_de_juros, tempo):
    return principal * (1 + (taxa_de_juros / 100) * tempo)

def calcular_juros_compostos(principal, taxa_de_juros, tempo):
    return principal * ((1 + (taxa_de_juros / 100)) ** tempo)

# Rota principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            p = float(request.form['principal'])
            r = float(request.form['taxa_de_juros'])
            t = int(request.form['tempo'])

            if p < 0 or r < 0 or t < 0:
                raise ValueError("Os valores devem ser positivos.")

            tempos = np.arange(t + 1)
            montantes_simples = [calcular_juros_simples(p, r, ano) for ano in tempos]
            montantes_compostos = [calcular_juros_compostos(p, r, ano) for ano in tempos]

            # Criar gráfico
            fig, ax = plt.subplots()
            ax.plot(tempos, montantes_simples, label='Juros Simples')
            ax.plot(tempos, montantes_compostos, label='Juros Compostos')
            ax.set_title('Crescimento do Investimento ao Longo do Tempo')
            ax.set_xlabel('Tempo (anos)')
            ax.set_ylabel('Montante')
            ax.legend()

            # Salvar gráfico em um objeto de bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)

            return render_template('index.html', image_base64=image_base64)
        except ValueError as e:
            return render_template('index.html', error=str(e))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
