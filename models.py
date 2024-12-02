from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, declarative_base

engine = create_engine('sqlite:///xtremegym.sqlite3')
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Funcionario(Base):
    __tablename__ = 'funcionarios'
    id_funcionario = Column(Integer, primary_key=True, unique=True)
    nome_funcionario = Column(String(40), nullable=True)
    cpf_funcionario = Column(Integer, nullable=True, unique=True)
    email_funcionario = Column(String(60), nullable=True, unique=True)
    telefone_funcionario = Column(Integer, nullable=True, unique=True)
    cargo_funcionario = Column(String(20), nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_func(self):
        dados_funcionario = {
            'id_funcionario': self.id_funcionario,
            'nome_funcionario': self.nome_funcionario,
            'cpf_funcionario': self.cpf_funcionario,
            'email_funcionario': self.email_funcionario,
            'telefone_funcionario': self.telefone_funcionario,
            'cargo_funcionario': self.cargo_funcionario
        }
        return dados_funcionario

    def __repr__(self):
        return '<Funcionarios: {} {} {} {} {} {}>'.format(self.id_funcionario,
                                                          self.nome_funcionario,
                                                          self.cpf_funcionario,
                                                          self.email_funcionario,
                                                          self.telefone_funcionario,
                                                          self.cargo_funcionario)


class Categoria(Base):
    __tablename__ = 'categorias'
    id_categoria = Column(Integer, primary_key=True, unique=True)
    nome_categoria = Column(String(40), nullable=True, unique=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_categoria(self):
        dados_categoria = {
            'id_categoria': self.id_categoria,
            'nome_categoria': self.nome_categoria,
        }
        return dados_categoria

    def __repr__(self):
        return '<Categorias: {} {}>'.format(self.id_categoria,
                                            self.nome_categoria)


class Produto(Base):
    __tablename__ = 'produtos'
    id_produto = Column(Integer, primary_key=True, unique=True)
    nome_produto = Column(String(40), nullable=True)
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    categorias = relationship(Categoria)
    quantidade_produto = Column(Integer, nullable=True)
    preco_custo = Column(Integer, nullable=True)
    preco_venda = Column(Integer, nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_produto(self):
        dados_produto = {
            'id_produto': self.id_produto,
            'nome_produto': self.nome_produto,
            'id_categoria': self.id_categoria,
            'quantidade_produto': self.quantidade_produto,
            'preco_custo': self.preco_custo,
            'preco_venda': self.preco_venda
        }
        return dados_produto

    def __repr__(self):
        return '<Produto: {} {} {} {} {} {}>'.format(self.id_produto,
                                                     self.nome_produto,
                                                     self.id_categoria,
                                                     self.quantidade_produto,
                                                     self.preco_custo,
                                                     self.preco_venda)


class Movimentacao(Base):
    __tablename__ = 'movimentacoes'
    id_movimentacao = Column(Integer, primary_key=True, unique=True)
    id_produto = Column(Integer, ForeignKey('produtos.id_produto'))
    produtos = relationship(Produto)
    quantidade_movimentacao = Column(Integer, nullable=True)
    data_movimentacao = Column(String(10), nullable=True)
    id_funcionario = Column(Integer, ForeignKey('funcionarios.id_funcionario'))
    funcionarios = relationship(Funcionario)
    tipo_movimentacao = Column(Boolean, nullable=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    def serialize_movimentacao(self):
        dados_movimentacao = {
            'id_movimentacao': self.id_movimentacao,
            'id_produto': self.id_produto,
            'quantidade_movimentacao': self.quantidade_movimentacao,
            'data_movimentacao': self.data_movimentacao,
            'id_funcionario': self.id_funcionario,
            'tipo_movimentacao': self.tipo_movimentacao,
        }
        return dados_movimentacao

    def __repr__(self):
        return '<Movimentacao: {} {} {} {} {} {}>'.format(self.id_movimentacao,
                                                          self.id_produto,
                                                          self.quantidade_movimentacao,
                                                          self.data_movimentacao,
                                                          self.id_funcionario,
                                                          self.tipo_movimentacao)


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
