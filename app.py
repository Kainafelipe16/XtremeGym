from flask import Flask, render_template, flash, url_for, redirect
from flask import request
from sqlalchemy import select

from models import Funcionario, Categoria, db_session, Produto, Movimentacao

app = Flask(__name__)
app.secret_key = 'Chave Secreta'


@app.route('/')
def index():
    return render_template("landpage.html")


@app.route('/movimentacoes')
def movimentacoes():
    lista_movimentacoes = select(Movimentacao).select_from(Movimentacao)
    lista_movimentacoes = db_session.execute(lista_movimentacoes).scalars()
    listaMovimentacoes = []
    for movimentacao in lista_movimentacoes:
        listaMovimentacoes.append(movimentacao.serialize_movimentacao())
    print(listaMovimentacoes)

    return render_template('movimentacoes.html', var_movimentacao=listaMovimentacoes)


@app.route('/catalogo')
def catalogo():
    lista_produtos = select(Produto).select_from(Produto)
    lista_produtos = db_session.execute(lista_produtos).scalars()
    listaProdutos = []
    for produto in lista_produtos:
        listaProdutos.append(produto.serialize_produto())
    print(listaProdutos)
    return render_template('catalogo.html', var_produto=listaProdutos)


@app.route('/listarFuncionarios', methods=['GET'])
def listarFuncionarios():
    lista_funcionarios = select(Funcionario).select_from(Funcionario)
    lista_funcionarios = db_session.execute(lista_funcionarios).scalars()
    listaFuncionarios = []
    for funcionario in lista_funcionarios:
        listaFuncionarios.append(funcionario.serialize_func())
    print(listaFuncionarios)
    return render_template('listarFuncionario.html', var_funcionario=listaFuncionarios)


@app.route('/listarCategorias', methods=['GET'])
def listarCategorias():
    lista_categorias = select(Categoria).select_from(Categoria)
    lista_categorias = db_session.execute(lista_categorias).scalars()
    listaCategorias = []
    for categoria in lista_categorias:
        listaCategorias.append(categoria.serialize_categoria())
    print(listaCategorias)
    return render_template('listarCategoria.html', var_categoria=listaCategorias)


@app.route('/movimentacaoProduto', methods=['POST', "GET"])
def movimentacaoProduto():
    if request.method == 'POST':
        if not request.form['id_produto']:
            flash("Escolha um produto para cadastrar uma entrada no estoque!", "error")
        if not request.form['id_funcionario']:
            flash("Informe o funcionário que está movimentando!", "error")
        if not request.form['quantidade_movimentacao']:
            flash("Informe quantos produtos foram inseridos no estoque!", "error")
        if not request.form['data_movimentacao']:
            flash("Informe a data da movimentação!", "error")
        if not request.form['tipo_movimentacao']:
            flash("Informe o tipo de movimentacao!", "error")

        else:
            tipo_mov = bool(int(request.form['tipo_movimentacao']))
            form_evento = Movimentacao(id_produto=int(request.form['id_produto']),
                                       id_funcionario=int(request.form['id_funcionario']),
                                       quantidade_movimentacao=int(request.form['quantidade_movimentacao']),
                                       data_movimentacao=request.form['data_movimentacao'],
                                       tipo_movimentacao=bool(int(request.form['tipo_movimentacao'])))
            atuliza_estoque = db_session.execute(select(Produto).where(int(request.form['id_produto']) == Produto.id_produto)).scalar()

            if tipo_mov:
                atuliza_estoque.quantidade_produto = int(request.form['quantidade_movimentacao']) + atuliza_estoque.quantidade_produto
            else:
                if atuliza_estoque.quantidade_produto >= int(request.form['quantidade_movimentacao']):
                    atuliza_estoque.quantidade_produto = atuliza_estoque.quantidade_produto - int(request.form['quantidade_movimentacao'])
                else:
                    flash("Quantidade no estoque insuficiente!", "error")

            print(atuliza_estoque.quantidade_produto)
            print(form_evento)
            form_evento.save()
            # db_session.close()
            flash("Movimentação de Produto Cadastrada!", "success")
            return redirect(url_for('movimentacoes'))

    # Recupera a lista de funcionários
    lista_funcionarios = select(Funcionario).select_from(Funcionario)
    lista_funcionarios = db_session.execute(lista_funcionarios).scalars()
    listaFuncionarios = []
    for funcionario in lista_funcionarios:
        listaFuncionarios.append(funcionario.serialize_func())

    # Recupera a lista de produtos
    lista_produtos = select(Produto).select_from(Produto)
    lista_produtos = db_session.execute(lista_produtos).scalars()
    listaProdutos = []
    for produto in lista_produtos:
        listaProdutos.append(produto.serialize_produto())

    # Recupera a lista de categorias
    lista_categorias = select(Categoria).select_from(Categoria)
    lista_categorias = db_session.execute(lista_categorias).scalars()
    listaCategorias = []
    for categoria in lista_categorias:
        listaCategorias.append(categoria.serialize_categoria())

        # Renderiza o template com as listas de funcionários e produtos
    return render_template('movimentacaoProduto.html', var_funcionario=listaFuncionarios, var_produto=listaProdutos,
                           var_categoria=listaCategorias)


@app.route('/cadastrarProduto', methods=['POST', "GET"])
def cadastrarProduto():
    if request.method == 'POST':
        if not request.form['nome_produto']:
            flash("Preencha o nome do produto para realizar o cadastro!", "error")
        if not request.form['quantidade_produto']:
            flash("Preencha a quantidade de produtos para realizar o cadastro!", "error")
        if not request.form['preco_custo']:
            flash("Preencha o valor do produto para realizar o cadastro!", "error")
        if not request.form['preco_venda']:
            flash("Preencha o valor que o produto será vendido!", "error")
        if not request.form['id_categoria']:
            flash('Preencha a categoria do produto para realizar o cadastro!', 'error')
        else:
            form_evento = Produto(nome_produto=request.form['nome_produto'],
                                  quantidade_produto=int(request.form['quantidade_produto']),
                                  preco_custo=int(request.form['preco_custo']),
                                  preco_venda=int(request.form['preco_venda']),
                                  id_categoria=int(request.form['id_categoria']))
            print(form_evento)
            form_evento.save()
            #db_session.close()
            flash("Produto Cadastrado com Sucesso!", "success")
            return redirect(url_for('catalogo'))
    lista_categorias = select(Categoria).select_from(Categoria)
    lista_categorias = db_session.execute(lista_categorias).scalars()
    listaCategorias = []
    for categoria in lista_categorias:
        listaCategorias.append(categoria.serialize_categoria())
    print(listaCategorias)
    return render_template('cadastroProduto.html', var_categoria=listaCategorias)


@app.route('/cadastrarFuncionario', methods=['POST', "GET"])
def cadastrarFuncionario():
    if request.method == 'POST':
        cpf = request.form['cpf_funcionario']
        sql_cpf = select(Funcionario).where(cpf == Funcionario.cpf_funcionario)
        sql_cpf = db_session.execute(sql_cpf).scalar()
        email = request.form['email_funcionario']
        sql_email = select(Funcionario).where(email == Funcionario.email_funcionario)
        sql_email = db_session.execute(sql_email).scalar()
        tel = request.form['telefone_funcionario']
        sql_tel = select(Funcionario).where(tel == Funcionario.telefone_funcionario)
        sql_tel = db_session.execute(sql_tel).scalar()

        if not request.form['nome_funcionario']:
            flash("Preencha o nome do funcionário para realizar o cadastro!", "error")
        elif sql_cpf:
            flash("O CPF informado pertence a outra pessoa!", "error")
        elif sql_email:
            flash("O E-mail informado pertence a outra pessoa!", "error")
        elif sql_tel:
            flash("O telefone informado pertence a outra pessoa!", "error")
        elif not request.form['cpf_funcionario']:
            flash("Preencha o cpf do funcionário para realizar o cadastro!", "error")
        elif not request.form['email_funcionario']:
            flash("Preencha o email do funcionário para realizar o cadastro!", "error")
        elif not request.form['telefone_funcionario']:
            flash("Preencha o telefone do funcionário para realizar o cadastro!", "error")
        elif not request.form['cargo_funcionario']:
            flash("Preencha o cargo do funcionário para realizar o cadastro!", "error")

        else:
            form_evento = Funcionario(nome_funcionario=request.form['nome_funcionario'],
                                      cpf_funcionario=int(request.form['cpf_funcionario']),
                                      email_funcionario=request.form['email_funcionario'],
                                      telefone_funcionario=int(request.form['telefone_funcionario']),
                                      cargo_funcionario=request.form['cargo_funcionario'])
            print(form_evento)
            form_evento.save()
            #db_session.close()
            flash("Funcionário Cadastrado com Sucesso!!", "sucess")
            return redirect(url_for('listarFuncionarios'))

    return render_template('cadastroFuncionario.html')


@app.route('/cadastrarCategoria', methods=['POST', "GET"])
def cadastrarCategoria():
    if request.method == 'POST':
        cat = request.form['nome_categoria']
        sql_cat = select(Categoria).where(cat == Categoria.nome_categoria)
        sql_cat = db_session.execute(sql_cat).scalar()

        if not request.form['nome_categoria']:
            flash("Preencha o nome da categoria para realizar o cadastro!", "error")
        elif sql_cat:
            flash("A Categoria já existe!", "error")
        else:
            form_evento = Categoria(nome_categoria=request.form['nome_categoria'])
            print(form_evento)
            form_evento.save()
            #db_session.close()
            flash("Categoria Cadastrada com Sucesso!", "success")
            return redirect(url_for('listarCategorias'))

    return render_template('cadastroCategoria.html')


@app.route('/editarFuncionario/<int:id>', methods=['POST', 'GET'])
def editarFuncionario(id):
    funcionario = Funcionario.query.get(id)
    if funcionario is None:
        flash('Funcionário não encontrado', 'error')
        return redirect(url_for('listarFuncionarios'))

    if request.method == 'POST':
        form_data = request.form
        funcionario.nome_funcionario = form_data['nome_funcionario']
        funcionario.cpf_funcionario = form_data['cpf_funcionario']
        funcionario.email_funcionario = form_data['email_funcionario']
        funcionario.telefone_funcionario = form_data['telefone_funcionario']
        funcionario.cargo_funcionario = form_data['cargo_funcionario']

        try:
            db_session.commit()
            flash('Funcionário atualizado com sucesso', 'success')
        except Exception as e:
            db_session.rollback()
            flash('Erro ao atualizar funcionário: {}'.format(e), 'error')

        return redirect(url_for('listarFuncionarios'))
    else:
        return render_template('editarFuncionario.html', funcionario=funcionario)


@app.route('/editarCategoria/<int:id>', methods=['POST', 'GET'])
def editarCategoria(id):
    categoria = Categoria.query.get(id)
    if categoria is None:
        flash('Categoria inexistente', 'error')
        return redirect(url_for('listarCategorias'))

    if request.method == 'POST':
        form_data = request.form
        categoria.nome_categoria = form_data['nome_categoria']

        try:
            db_session.commit()
            flash('Categoria atualizada com sucesso!', 'success')
        except Exception as e:
            db_session.rollback()
            flash('Erro ao atualizar categoria: {}'.format(e), 'error')

        return redirect(url_for('listarCategorias'))
    else:
        return render_template('editarCategoria.html', categoria=categoria)


@app.route('/editarProduto/<int:id>', methods=['POST', 'GET'])
def editarProduto(id):
    produto = Produto.query.get(id)
    if produto is None:
        flash('Produto inexistente', 'error')
        return redirect(url_for('catalogo'))

    if request.method == 'POST':
        form_data = request.form
        produto.nome_produto = form_data['nome_produto']
        produto.id_categoria = form_data['id_categoria']
        produto.quantidade_produto = form_data['quantidade_produto']
        produto.preco_custo = form_data['preco_custo']
        produto.preco_venda = form_data['preco_venda']

        try:
            db_session.commit()
            flash('Produto atualizado com sucesso!', 'success')
        except Exception as e:
            db_session.rollback()
            flash('Erro ao atualizar produto: {}'.format(e), 'error')

        return redirect(url_for('catalogo'))

    # O código a seguir deve ser executado quando o método for GET
    lista_categorias = select(Categoria).select_from(Categoria)
    lista_categorias = db_session.execute(lista_categorias).scalars()
    listaCategorias = []
    for categoria in lista_categorias:
        listaCategorias.append(categoria.serialize_categoria())

    return render_template('editarProduto.html', produto=produto, var_categoria=listaCategorias)


@app.route('/deletarFuncionario/<int:id>', methods=['POST', 'GET'])
def deletarFuncionario(id):
    funcionario = select(Funcionario).where(Funcionario.id_funcionario == id)
    print(funcionario)
    funcionario_del = db_session.execute(funcionario).scalar()
    funcionario_del.delete()
    flash('Funcionário deletado com sucesso!', 'success')
    return redirect(url_for('listarFuncionarios'))


@app.route('/deletarCategoria/<int:id>', methods=['POST', 'GET'])
def deletarCategoria(id):
    categoria = select(Categoria).where(Categoria.id_categoria == id)
    print(categoria)
    categoria_del = db_session.execute(categoria).scalar()
    categoria_del.delete()
    flash('Categoria deletado com sucesso!', 'success')
    return redirect(url_for('listarCategorias'))


@app.route('/deletarProduto/<int:id>', methods=['POST', 'GET'])
def deletarProduto(id):
    produto = select(Produto).where(Produto.id_produto == id)
    print(produto)
    produto_del = db_session.execute(produto).scalar()
    produto_del.delete()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('catalogo'))


if __name__ == '__main__':
    app.run(debug=True)
