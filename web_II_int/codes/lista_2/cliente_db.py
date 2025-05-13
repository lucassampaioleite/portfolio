import sqlite3


class ClienteDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(100),
                cidade VARCHAR(100)
            );
        """)
        self.conn.commit()

    def inserir_cliente(self, nome, cidade):
        self.cursor.execute("""
            INSERT INTO clientes (nome, cidade)
            VALUES (?, ?)
        """, (nome, cidade))
        self.conn.commit()

    def inserir_clientes(self, lista_de_clientes):
        self.cursor.executemany("""
            INSERT INTO clientes (nome, cidade)
            VALUES (?, ?)
        """, lista_de_clientes)
        self.conn.commit()

    def atualizar_cliente(self, id, nome, cidade):
        self.cursor.execute("""
            UPDATE clientes
            SET nome = ?, cidade = ?
            WHERE id = ?
        """, (nome, cidade, id))
        self.conn.commit()

    def deletar_cliente(self, id):
        self.cursor.execute("""
            DELETE FROM clientes
            WHERE id = ?
        """, (id,))
        self.conn.commit()

    def consultar_cliente(self, id):
        self.cursor.execute("""
            SELECT * FROM clientes
            WHERE id = ?
        """, (id,))
        return self.cursor.fetchone()

    def consultar_todos_clientes(self):
        self.cursor.execute("""
            SELECT * FROM clientes
        """)
        return self.cursor.fetchall()

    def fechar_conexao(self):
        self.cursor.close()
        self.conn.close()

    # def inserir_cliente(self, nome, cidade, commit=True):
    #     self.cursor.execute("""
    #         INSERT INTO clientes (nome, cidade)
    #         VALUES (?, ?)
    #     """, (nome, cidade))
    #     if commit:
    #         self.conn.commit()

    # def inserir_cliente(self, nome, cidade):
    #     try:
    #         self.cursor.execute("""
    #             INSERT INTO clientes (nome, cidade)
    #             VALUES (?, ?)
    #         """, (nome, cidade))
    #         self.conn.commit()
    #     except sqlite3.Error as e:
    #         print(f"Erro ao inserir cliente: {e}")
    #         self.conn.rollback()


if __name__ == "__main__":
    db = ClienteDB("my_database.db")

    db.inserir_cliente("Lucas", "Recife - PE")
    db.inserir_cliente("Maria", "Senhor do Bonfim - BA")

    dados = [
        ("Lucas", "Recife - PE"),
        ("Maria", "Senhor do Bonfim - BA"),
        ("Jaiminho", "Tangamandápio - Michoacán")
    ]

    db.inserir_clientes(dados)

    db.atualizar_cliente(1, "Lucas", "Salvador - BA")

    cliente = db.consultar_cliente(1)
    print(cliente)

    clientes = db.consultar_todos_clientes()
    print(clientes)

    # db.inserir_cliente("João", "Natal", commit=False)
    # db.inserir_cliente("Ana", "Fortaleza", commit=False)
    # db.conn.commit()

    db.deletar_cliente(2)
    db.fechar_conexao()
