import flet as ft
from datetime import datetime
from bd import criar_tabelas, inserir_aluno, buscar_aluno_por_cpf, inserir_materia, buscar_materias_por_cpf, atualizar_materia

def main(page: ft.Page):
    page.title = "Gestão de Notas - Larissa 💻🎓"
    criar_tabelas()

    aluno_logado = None  # Vai guardar o CPF do aluno logado
    materias = []        # Lista de matérias do aluno

    # Campos cadastro/login
    campo_cpf = ft.TextField(label="CPF", width=300, hint_text="Ex: 123.456.789-00")
    campo_nome = ft.TextField(label="Nome completo", width=300)
    campo_curso = ft.TextField(label="Curso", width=300)
    campo_semestre = ft.TextField(label="Semestre", width=150)
    resultado = ft.Text(color=ft.colors.RED)

    # Campos matérias
    campo_materia = ft.TextField(label="Nome da Matéria", width=300)
    campo_nota = ft.TextField(label="Adicionar Nota", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    notas_materia = []
    notas_texto = ft.Text()
    resultado_media = ft.Text()
    lista_materias_salvas = ft.Column()

    # --- Funções de navegação ---
    def mostrar_tela_cadastro():
        resultado.value = ""
        campo_cpf.value = ""
        campo_nome.value = ""
        campo_curso.value = ""
        campo_semestre.value = ""
        page.controls.clear()
        page.add(
            ft.Text("Cadastro 📋", size=25, weight="bold"),
            campo_cpf,
            campo_nome,
            campo_curso,
            campo_semestre,
            ft.Row([
                ft.ElevatedButton(text="Cadastrar", on_click=cadastrar_aluno, color=ft.colors.GREEN),
                ft.ElevatedButton(text="Já tenho cadastro", on_click=mostrar_tela_login, color=ft.colors.BLUE)
            ]),
            resultado
        )
        page.update()

    def mostrar_tela_login(e=None):
        resultado.value = ""
        campo_cpf.value = ""
        page.controls.clear()
        page.add(
            ft.Text("Login 📲", size=24, weight="bold"),
            campo_cpf,
            ft.Row([
                ft.ElevatedButton(text="Entrar", on_click=logar_aluno, color=ft.colors.GREEN),
                ft.ElevatedButton(text="Voltar", on_click=lambda e: mostrar_tela_cadastro(), color=ft.colors.RED)
            ]),
            resultado
        )
        page.update()

    def mostrar_tela_materias():
        nonlocal notas_materia
        notas_materia = []
        campo_materia.value = ""
        campo_nota.value = ""
        notas_texto.value = ""
        resultado_media.value = ""
        lista_materias_salvas.controls.clear()

        # Recarregar matérias do banco para o aluno logado
        nonlocal materias
        materias = buscar_materias_por_cpf(aluno_logado)

        for m in materias:
            notas_str = ", ".join([str(n) for n in m["notas"]])
            lista_materias_salvas.controls.append(
                ft.Row([
                    ft.Text(f"{m['nome']} - Notas: [{notas_str}] - Média: {m['media']:.2f} - {m['status']} - Data: {m['data_adicionado']}"),
                    ft.ElevatedButton("Editar", on_click=lambda e, mat=m: mostrar_tela_editar_materia(mat), color=ft.colors.ORANGE_300)
                ])
            )
        page.controls.clear()
        page.add(
            ft.Text(f"Matérias de {campo_nome.value} 📚", size=24, weight="bold"),
            campo_materia,
            campo_nota,
            ft.Row([
                ft.ElevatedButton(text="Adicionar Nota", on_click=adicionar_nota, color=ft.colors.PINK_300),
                ft.ElevatedButton(text="Salvar Matéria", on_click=salvar_materia, color=ft.colors.PINK_300),
                ft.ElevatedButton(text="Logout", on_click=logout, color=ft.colors.RED)
            ]),
            notas_texto,
            resultado_media,
            ft.Divider(),
            ft.Text("Matérias adicionadas:"),
            lista_materias_salvas,
            ft.ElevatedButton(text="Ver Resumo", on_click=mostrar_tela_resumo, color=ft.colors.GREEN),
            ft.ElevatedButton(text="Voltar", on_click=mostrar_tela_login, color=ft.colors.RED)
        )
        page.update()

    def mostrar_tela_editar_materia(materia):
        campo_materia.value = materia["nome"]
        nonlocal notas_materia
        notas_materia = list(materia["notas"])  # copia para editar
        campo_nota.value = ""
        notas_texto.value = f"Notas atuais: {notas_materia}"
        resultado_media.value = ""
        page.controls.clear()
        page.add(
            ft.Text(f"Editar Matéria: {materia['nome']}", size=24, weight="bold"),
            campo_materia,
            campo_nota,
            ft.Row([
                ft.ElevatedButton(text="Adicionar Nota", on_click=adicionar_nota, color=ft.colors.PINK_300),
                ft.ElevatedButton(text="Salvar Alterações", on_click=lambda e: salvar_alteracoes_materia(materia), color=ft.colors.ORANGE_700),
                ft.ElevatedButton(text="Cancelar", on_click=mostrar_tela_materias, color=ft.colors.RED)
            ]),
            notas_texto,
            resultado_media,
        )
        page.update()

    def mostrar_tela_resumo(e=None):
        page.controls.clear()
        page.add(
            ft.Text("Resumo Final 📊", size=24, weight="bold"),
            ft.Text(f"Aluno(a): {campo_nome.value} | Curso: {campo_curso.value} | Semestre: {campo_semestre.value}", size=16)
        )
        pie_chart = ft.PieChart(
            sections=[
                ft.PieChartSection(
                    value=m["media"],
                    title=m["nome"],
                    color=ft.colors.GREEN if m["media"] >= 6 else ft.colors.RED,
                    radius=80,
                ) for m in materias
            ],
            sections_space=2,
            center_space_radius=40,
            height=250,
        )
        header = ft.Row([
            ft.Text("Matéria", weight="bold", width=150),
            ft.Text("Média", weight="bold", width=100),
            ft.Text("Status", weight="bold", width=100),
            ft.Text("Data", weight="bold", width=150)
        ])
        linhas = []
        for m in materias:
            cor = ft.colors.GREEN_400 if m["media"] >= 6 else ft.colors.RED_400
            linhas.append(
                ft.Row([
                    ft.Text(m["nome"], width=150),
                    ft.Text(f"{m['media']:.2f}", width=100),
                    ft.Text(m["status"], width=100, color=cor),
                    ft.Text(m["data_adicionado"], width=150)
                ])
            )
        page.add(
            pie_chart,
            ft.Divider(),
            ft.Text("Tabela de Resultados", size=20, weight="w600"),
            header,
            *linhas,
            ft.ElevatedButton(text="Voltar", on_click=mostrar_tela_materias, color=ft.colors.RED)
        )
        page.update()

    # --- Funções lógica ---
    def cadastrar_aluno(e):
        cpf = campo_cpf.value.strip()
        nome = campo_nome.value.strip()
        curso = campo_curso.value.strip()
        semestre = campo_semestre.value.strip()

        if not cpf or not nome or not curso or not semestre:
            resultado.value = "⚠️ Preencha todos os campos!"
            page.update()
            return

        sucesso = inserir_aluno(cpf, nome, curso, semestre)
        if sucesso:
            resultado.value = f"✅ Aluno {nome} cadastrado com sucesso!"
            page.update()
        else:
            resultado.value = "⚠️ CPF já cadastrado."
            page.update()

    def logar_aluno(e):
        cpf = campo_cpf.value.strip()
        aluno = buscar_aluno_por_cpf(cpf)
        if aluno:
            nonlocal aluno_logado
            aluno_logado = cpf
            # Preencher dados para mostrar no resumo e matérias
            campo_nome.value = aluno[1]
            campo_curso.value = aluno[2]
            campo_semestre.value = aluno[3]
            mostrar_tela_materias()
        else:
            resultado.value = "⚠️ Aluno não encontrado. Cadastre-se primeiro."
            page.update()

    def adicionar_nota(e):
        try:
            nota = float(campo_nota.value)
            if nota < 0 or nota > 10:
                resultado_media.value = "Nota deve ser entre 0 e 10."
                page.update()
                return
            notas_materia.append(nota)
            campo_nota.value = ""
            notas_texto.value = f"Notas: {notas_materia}"
            resultado_media.value = ""
            page.update()
        except:
            resultado_media.value = "Digite apenas números válidos."
            page.update()

    def salvar_materia(e):
        nome_materia = campo_materia.value.strip()
        if not nome_materia or not notas_materia:
            resultado_media.value = "Preencha o nome e adicione ao menos uma nota."
            page.update()
            return

        media = sum(notas_materia) / len(notas_materia)
        status = "✅ Aprovada" if media >= 6 else "❌ Reprovada"
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        inserir_materia(aluno_logado, nome_materia, notas_materia, media, status, data_hoje)

        # Atualizar lista local e tela
        mostrar_tela_materias()

    def salvar_alteracoes_materia(materia_original):
        nome_novo = campo_materia.value.strip()
        if not nome_novo or not notas_materia:
            resultado_media.value = "Preencha o nome e adicione ao menos uma nota."
            page.update()
            return

        media = sum(notas_materia) / len(notas_materia)
        status = "✅ Aprovada" if media >= 6 else "❌ Reprovada"
        # Mantém a data original
        atualizar_materia(materia_original["id"], nome_novo, notas_materia, media, status)

        mostrar_tela_materias()

    def logout(e):
        nonlocal aluno_logado
        aluno_logado = None
        mostrar_tela_login()

    # Inicia na tela de cadastro
    mostrar_tela_cadastro()

ft.app(target=main)
