import flet as ft

def main(page: ft.Page):
    page.title = "Gestão de Notas - Larissa 💻🎓"
    materias = []

    # Campos da primeira tela
    campo_nome = ft.TextField(label="Seu nome", width=300)
    campo_curso = ft.TextField(label="Curso", width=300)
    campo_semestre = ft.TextField(label="Semestre", width=150)
    resultado = ft.Text()

    # --- Terceira tela: Gráfico e tabela ---
    def terceira_tela(nome, curso, semestre, materias):
        page.controls.clear()

        page.add(
            ft.Text("Resumo Final 📊", size=24, weight="bold"),
            ft.Text(f"Aluno(a): {nome} | Curso: {curso} | Semestre: {semestre}", size=16)
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
            ft.Text("Status", weight="bold", width=100)
        ])

        linhas = []
        for m in materias:
            cor = ft.colors.GREEN_400 if m["media"] >= 6 else ft.colors.RED_400
            linhas.append(
                ft.Row([
                    ft.Text(m["nome"], width=150),
                    ft.Text(f"{m['media']:.2f}", width=100),
                    ft.Text(m["status"], width=100, color=cor)
                ])
            )

        page.add(
            pie_chart,
            ft.Divider(),
            ft.Text("Tabela de Resultados", size=20, weight="w600"),
            header,
            *linhas
        )

        page.update()

    # --- Segunda tela: cadastro de matérias ---
    def segunda_tela(nome, curso, semestre):
        page.controls.clear()

        campo_materia = ft.TextField(label="Nome da Matéria", width=300)
        campo_nota = ft.TextField(label="Adicionar Nota", width=150, keyboard_type=ft.KeyboardType.NUMBER)
        notas_materia = []
        notas_texto = ft.Text()
        resultado_media = ft.Text()
        lista_materias_salvas = ft.Column()

        def adicionar_nota(e):
            try:
                nota = float(campo_nota.value)
                notas_materia.append(nota)
                campo_nota.value = ""
                notas_texto.value = f"Notas: {notas_materia}"
            except:
                notas_texto.value = "Digite apenas números"
            page.update()

        def adicionar_materia(e):
            nome_materia = campo_materia.value.strip()
            if not nome_materia or not notas_materia:
                resultado_media.value = "Preencha o nome e adicione ao menos uma nota."
                return

            media = sum(notas_materia) / len(notas_materia)
            status = "✅ Aprovada" if media >= 6 else "❌ Reprovada"

            materias.append({
                "nome": nome_materia,
                "notas": list(notas_materia),
                "media": media,
                "status": status
            })

            lista_materias_salvas.controls.append(
                ft.Text(f"{nome_materia} - Média: {media:.2f} - {status}")
            )

            campo_materia.value = ""
            notas_materia.clear()
            notas_texto.value = ""
            resultado_media.value = ""

            page.update()

        def ir_para_graficos(e):
            terceira_tela(nome, curso, semestre, materias)

        page.add(
            ft.Text("Cadastro de Matérias 📚", size=24, weight="bold"),
            campo_materia,
            campo_nota,
            ft.Row([
                ft.ElevatedButton(text="Adicionar Nota", on_click=adicionar_nota, color=ft.colors.PINK_300),
                ft.ElevatedButton(text="Salvar Matéria", on_click=adicionar_materia, color=ft.colors.PINK_300)
            ]),
            notas_texto,
            resultado_media,
            ft.Divider(),
            ft.Text("Matérias adicionadas:"),
            lista_materias_salvas,
            ft.ElevatedButton(text="Terminar", on_click=ir_para_graficos, color=ft.colors.GREEN)
        )
        page.update()

    # Primeira tela - cadastro inicial
    def avancar(e):
        nome = campo_nome.value.strip()
        curso = campo_curso.value.strip()
        semestre = campo_semestre.value.strip()

        if not nome or not curso or not semestre:
            resultado.value = "Preencha todos os campos!"
        else:
            segunda_tela(nome, curso, semestre)

        page.update()

    page.add(
        ft.Text("Cadastro Inicial 📋", size=24, weight="bold"),
        campo_nome,
        campo_curso,
        campo_semestre,
        ft.ElevatedButton(text="Avançar", on_click=avancar, color=ft.colors.PINK_300),
        resultado
    )

ft.app(target=main)
