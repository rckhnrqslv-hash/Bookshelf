from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'bookshelf_secret_key'

# Banco de dados simulado (Mock) baseado na estrutura Bookshelf
USUARIOS = {
    "autor@bookshelf.com": {
        "nome": "Rodrigo Turini",
        "username": "rodrigo_turini",
        "cpf": "000.000.000-00",
        "senha": "123",
        "bio": "Escrevendo histórias, conectando mundos. Desenvolvedor e Escritor na Bookshelf Co."
    }
}

LIVROS_MOCK = [
    {
        "id": 1,
        "titulo": "Desbravando Java e Orientação a Objetos",
        "autor": "Rodrigo Turini",
        "formato": "PDF",
        "tamanho": "4.8 MB",
        "progresso": 35,
        "paginas": "032 - 323 PÁG."
    },
    {
        "id": 2,
        "titulo": "Java - Como Programar",
        "autor": "Paul Deitel, Harvey Deitel",
        "formato": "PDF",
        "tamanho": "22 MB",
        "progresso": 12,
        "paginas": "050 - 960 PÁG."
    },
    {
        "id": 3,
        "titulo": "Box HP Lovecraft: Os melhores contos",
        "autor": "Lovecraft H.P.",
        "formato": "EPUB",
        "tamanho": "3,9 MB",
        "progresso": 85,
        "paginas": "210 - 245 PÁG."
    }
]

RASCUNHOS_MOCK = [
    {
        "id": 1,
        "titulo": "Crônicas de Bordeaux: O Início",
        "updated_at": "14/09/2026",
        "previa": "O sol se punha atrás das colinas avermelhadas quando o primeiro mensageiro do rei cruzou os portões de pedra..."
    },
    {
        "id": 2,
        "titulo": "Arquitetura Limpa no Mundo Real",
        "updated_at": "10/09/2026",
        "previa": "Capítulo 3: Entidades não devem conhecer os detalhes dos frameworks de entrega. Isso inclui o Flask..."
    }
]

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if email in USUARIOS and USUARIOS[email]['senha'] == senha:
            return redirect(url_for('perfil'))
        else:
            flash("Usuário ou senha incorretos.", "error")
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        cpf = request.form.get('cpf')
        
        username = nome.lower().replace(" ", "_")
        
        if email in USUARIOS:
            flash("E-mail já cadastrado.", "error")
        else:
            USUARIOS[email] = {
                'nome': nome, 
                'username': username,
                'senha': senha, 
                'cpf': cpf,
                'bio': 'Novo escritor na comunidade Bookshelf!'
            }
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/biblioteca')
def biblioteca():
    busca = request.args.get('q', '')
    livros_filtrados = LIVROS_MOCK
    if busca:
        livros_filtrados = [l for l in LIVROS_MOCK if busca.lower() in l['titulo'].lower() or busca.lower() in l['autor'].lower()]
    return render_template('biblioteca.html', livros=livros_filtrados, busca=busca)

# ====================================================================
# CORRIGIDO: Rota alterada para renderizar o arquivo 'usuario.html'
# ====================================================================
@app.route('/perfil')
def perfil():
    busca = request.args.get('q', '')
    
    usuario_atual = list(USUARIOS.values())[0] if USUARIOS else None
    
    livros_prateleira = LIVROS_MOCK
    if busca:
        livros_prateleira = [l for l in LIVROS_MOCK if busca.lower() in l['titulo'].lower() or busca.lower() in l['autor'].lower()]

    # Mudança aqui: Renderizando usuario.html conforme solicitado
    return render_template(
        'usuario.html', 
        usuario=usuario_atual, 
        livros_prateleira=livros_prateleira,
        rascunhos=RASCUNHOS_MOCK,
        publicados=[],
        busca=busca
    )

@app.route('/perfil/publicar', methods=['POST'])
def publicar_livro():
    titulo = request.form.get('titulo')
    arquivo = request.files.get('arquivo')
    
    if arquivo and arquivo.filename != '':
        extensao = os.path.splitext(arquivo.filename).upper().replace('.', '')
        
        novo_livro = {
            "id": len(LIVROS_MOCK) + 1,
            "titulo": titulo,
            "autor": "Você (Autor Bookshelf)",
            "formato": extensao,
            "tamanho": "Upload Virtual",
            "progresso": 100,
            "paginas": "Completo"
        }
        
        LIVROS_MOCK.append(novo_livro)
        flash(f"Obra '{titulo}' publicada com sucesso no ecossistema Bookshelf!", "success")
        return redirect(url_for('perfil'))
        
    flash("Erro ao enviar o arquivo do manuscrito.", "error")
    return redirect(url_for('perfil'))

if __name__ == '__main__':
    app.run(debug=True)
