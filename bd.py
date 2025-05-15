import sqlite3
import json


def criar_tabelas():
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        cpf TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        curso TEXT NOT NULL,
        semestre TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS materias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cpf_aluno TEXT,
        nome TEXT NOT NULL,
        notas TEXT NOT NULL,
        media REAL,
        status TEXT,
        data_adicionado TEXT,
        FOREIGN KEY (cpf_aluno) REFERENCES alunos(cpf)
    )
    """)

    conn.commit()
    conn.close()

def inserir_aluno(cpf, nome, curso, semestre):
    try:
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO alunos (cpf, nome, curso, semestre)
            VALUES (?, ?, ?, ?)
        """, (cpf, nome, curso, semestre))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # CPF já cadastrado

def buscar_aluno_por_cpf(cpf):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alunos WHERE cpf = ?", (cpf,))
    aluno = cursor.fetchone()
    conn.close()
    return aluno

def inserir_materia(cpf_aluno, nome, notas, media, status, data_adicionado):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    notas_json = json.dumps(notas)  # Salva as notas como JSON
    cursor.execute("""
        INSERT INTO materias (cpf_aluno, nome, notas, media, status, data_adicionado)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cpf_aluno, nome, notas_json, media, status, data_adicionado))
    conn.commit()
    conn.close()

def buscar_materias_por_cpf(cpf_aluno):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, notas, media, status, data_adicionado FROM materias WHERE cpf_aluno = ?", (cpf_aluno,))
    rows = cursor.fetchall()
    conn.close()

    materias = []
    for row in rows:
        materias.append({
            "id": row[0],
            "nome": row[1],
            "notas": json.loads(row[2]),
            "media": row[3],
            "status": row[4],
            "data_adicionado": row[5]
        })
    return materias

def atualizar_materia(id_materia, nome, notas, media, status):
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    notas_json = json.dumps(notas)
    cursor.execute("""
        UPDATE materias
        SET nome = ?, notas = ?, media = ?, status = ?
        WHERE id = ?
    """, (nome, notas_json, media, status, id_materia))
    conn.commit()
    conn.close()


