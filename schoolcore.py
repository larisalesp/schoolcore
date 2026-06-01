from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime
import random

class Banco:
    def __init__(self):
        self.alunos = None
        self.professores = None
        self.turmas = None
        self.matriculas = None
        self.disciplinas = None
        self.notas = None

banco_dados = Banco()

def conectar_banco():
    try:
        cliente = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        cliente.server_info()
        banco = cliente["schoolcore"]
        banco_dados.alunos = banco["alunos"]
        banco_dados.professores = banco["professores"]
        banco_dados.turmas = banco["turmas"]
        banco_dados.matriculas = banco["matriculas"]
        banco_dados.disciplinas = banco["disciplinas"]
        banco_dados.notas = banco["notas"]
        print("\n [OK] Conectado ao MongoDB com sucesso.")
        return True
    except ServerSelectionTimeoutError:
        print("\n[ERRO] Não foi possível conectar ao MongoDB.")
        print("Verifique se o MongoDB está em execução em mongodb://localhost:27017")
        return False

class Usuario:
    def __init__(self, nome, cpf):
        self.set_nome(nome)
        self._cpf = cpf

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        if nome.strip() != "":
            self._nome = nome.strip()
        else:
            self._nome = "Nome não informado"
            print("Nome inválido.")

    def get_cpf(self):
        return self._cpf

class Aluno(Usuario):
    def __init__(self, nome, cpf, aniversario, curso, periodo, status, matricula=""):
        super().__init__(nome, cpf)
        self._aniversario = aniversario
        self.set_curso(curso)
        self._periodo = periodo
        self._status = status
        self._matricula = matricula

    def get_matricula(self):
        return self._matricula

    def get_aniversario(self):
        return self._aniversario

    def get_curso(self):
        return self._curso

    def set_curso(self, valor):
        if valor.strip() != "":
            self._curso = valor.strip()
        else:
            print("Curso inválido.")
            self._curso = "Não informado"

    def get_periodo(self):
        return self._periodo

    def set_periodo(self, valor):
        self._periodo = valor.strip()

    def get_status(self):
        return self._status

    def set_status(self, valor):
        self._status = valor.strip()

    def exibir_perfil(self):
        print("\n" + "=" * 36)
        print(" PERFIL DO ALUNO".center(36))
        print("=" * 36)
        print(f" Matrícula: {self._matricula}")
        print(f" Nome: {self._nome}")
        print(f" CPF: {self._cpf}")
        print(f" Nascimento: {self._aniversario}")
        print(f" Curso: {self._curso}")
        print(f" Período: {self._periodo}")
        print(f" Status: {self._status}")
        print("─" * 36)

class Professor(Usuario):
    def __init__(self, nome, titulacao, area, disciplinas, codigo=""):
        super().__init__(nome, "")
        self._titulacao = titulacao
        self._area = area
        self._disciplinas = disciplinas
        self._codigo = codigo

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, valor):
        self._codigo = valor

    def get_titulacao(self):
        return self._titulacao

    def get_area(self):
        return self._area

    def get_disciplinas(self):
        return self._disciplinas

    def exibir_perfil(self):
        print("\n" + "=" * 36)
        print("  PERFIL DO PROFESSOR".center(36))
        print("=" * 36)
        print(f" Código : {self._codigo}")
        print(f" Nome : {self._nome}")
        print(f" Titulação : {self._titulacao}")
        print(f" Área : {self._area}")
        discs = ", ".join(self._disciplinas) if self._disciplinas else "Nenhuma"
        print(f" Disciplinas: {discs}")
        print("─" * 36)

class Disciplina:
    def __init__(self, nome, carga_horaria, codigo=""):
        self.set_nome(nome)
        self.set_carga_horaria(carga_horaria)
        self._codigo = codigo

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        if nome.strip() != "":
            self._nome = nome.strip()
        else:
            print("Nome da disciplina inválido.")
            self._nome = "Não informado"

    def get_carga_horaria(self):
        return self._carga_horaria

    def set_carga_horaria(self, valor):
        if valor > 0:
            self._carga_horaria = valor
        else:
            print("Carga horária deve ser positiva.")
            self._carga_horaria = 0

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, valor):
        self._codigo = valor

    def __str__(self):
        return f"[{self._codigo}] {self._nome} — {self._carga_horaria}h"

class Turma:
    def __init__(self, disciplina, codigo_professor, professor_nome, horario, turma_id="", alunos=None):
        self._disciplina = disciplina
        self._codigo_professor = codigo_professor
        self._professor_nome = professor_nome
        self._horario = horario
        self._turma_id = turma_id
        self._alunos = alunos if alunos is not None else []

    def get_turma_id(self):
        return self._turma_id

    def get_disciplina(self):
        return self._disciplina

    def get_codigo_professor(self):
        return self._codigo_professor

    def get_professor_nome(self):
        return self._professor_nome

    def get_horario(self):
        return self._horario

    def get_alunos(self):
        return self._alunos

    def adicionar_aluno(self, matricula):
        if matricula not in self._alunos:
            self._alunos.append(matricula)

    def remover_aluno(self, matricula):
        if matricula in self._alunos:
            self._alunos.remove(matricula)

def gerar_codigo_aluno():
    ano = datetime.now().year
    while True:
        numero = random.randint(1, 9999)
        codigo = f"ALU{ano}-{numero:04d}"
        if not banco_dados.alunos.find_one({"matricula": codigo}):
            return codigo

def gerar_codigo_professor():
    ano = datetime.now().year
    while True:
        numero = random.randint(1, 9999)
        codigo = f"PRO{ano}-{numero:04d}"
        if not banco_dados.professores.find_one({"codigo": codigo}):
            return codigo

def gerar_codigo_disciplina():
    while True:
        numero = random.randint(1, 999)
        codigo = f"DIS-{numero:03d}"
        if not banco_dados.disciplinas.find_one({"codigo": codigo}):
            return codigo

def gerar_turma_id():
    while True:
        numero = random.randint(1, 999)
        tid = f"TUR-{numero:03d}"
        if not banco_dados.turmas.find_one({"turma_id": tid}):
            return tid

def buscar_aluno_por_matricula(matricula):
    d = banco_dados.alunos.find_one({"matricula": matricula}, {"_id": 0})
    if d:
        return Aluno(
            nome=d["nome"],
            cpf=d["cpf"],
            aniversario=d["aniversario"],
            curso=d["curso"],
            periodo=d["periodo"],
            status=d["status"],
            matricula=d["matricula"]
        )
    return None

def buscar_professor_por_codigo(codigo):
    d = banco_dados.professores.find_one({"codigo": codigo}, {"_id": 0})
    if d:
        return Professor(
            nome=d["nome"],
            titulacao=d["titulacao"],
            area=d["area"],
            disciplinas=d["disciplinas"],
            codigo=d["codigo"]
        )
    return None

def buscar_turmas_do_aluno(matricula):
    resultado = []
    for d in banco_dados.turmas.find({"alunos": matricula}, {"_id": 0}):
        resultado.append(Turma(
            disciplina=d["disciplina"],
            codigo_professor=d["codigo_professor"],
            professor_nome=d["professor_nome"],
            horario=d["horario"],
            turma_id=d["turma_id"],
            alunos=d.get("alunos", [])
        ))
    return resultado

def buscar_turmas_do_professor(codigo_prof):
    resultado = []
    for d in banco_dados.turmas.find({"codigo_professor": codigo_prof}, {"_id": 0}):
        resultado.append(Turma(
            disciplina=d["disciplina"],
            codigo_professor=d["codigo_professor"],
            professor_nome=d["professor_nome"],
            horario=d["horario"],
            turma_id=d["turma_id"],
            alunos=d.get("alunos", [])
        ))
    return resultado

def buscar_nota(turma_id, matricula):
    d = banco_dados.notas.find_one({"turma_id": turma_id, "matricula": matricula}, {"_id": 0})
    if d:
        return {
            "NP1": d.get("NP1"),
            "NP2": d.get("NP2"),
            "faltas": d.get("faltas", 0),
            "total_aulas": d.get("total_aulas", 0),
        }
    return {"NP1": None, "NP2": None, "faltas": 0, "total_aulas": 0}

def salvar_nota(turma_id, matricula, np1=None, np2=None, faltas=None, total_aulas=None):
    nota_atual = buscar_nota(turma_id, matricula)
    np1_final = np1 if np1 is not None else nota_atual["NP1"]
    np2_final = np2 if np2 is not None else nota_atual["NP2"]
    faltas_final = faltas if faltas is not None else nota_atual["faltas"]
    total_final = total_aulas if total_aulas is not None else nota_atual["total_aulas"]
    novo_doc = {
        "turma_id": turma_id,
        "matricula": matricula,
        "NP1": np1_final,
        "NP2": np2_final,
        "faltas": faltas_final,
        "total_aulas": total_final,
    }
    banco_dados.notas.update_one(
        {"turma_id": turma_id, "matricula": matricula},
        {"$set": novo_doc},
        upsert=True
    )

def atualizar_turma_no_banco(turma_atualizada):
    doc_turma = {
        "turma_id": turma_atualizada.get_turma_id(),
        "disciplina": turma_atualizada.get_disciplina(),
        "codigo_professor": turma_atualizada.get_codigo_professor(),
        "professor_nome": turma_atualizada.get_professor_nome(),
        "horario": turma_atualizada.get_horario(),
        "alunos": turma_atualizada.get_alunos(),
    }
    banco_dados.turmas.update_one(
        {"turma_id": turma_atualizada.get_turma_id()},
        {"$set": doc_turma}
    )

def cadastrar_aluno():
    print("\n" + "=" * 36)
    print(" CADASTRO DE ALUNO".center(36))
    print("=" * 36)
    print(" (pressione Enter para cancelar em qualquer campo)\n")
    nome = input(" Nome completo: ").strip()
    if not nome:
        print("\n Cadastro cancelado.")
        return None
    cpf = input(" CPF: ").strip()
    if not cpf:
        print("\n Cadastro cancelado.")
        return None
    if banco_dados.alunos.find_one({"cpf": cpf}):
        print("\n [ERRO] Já existe um aluno com esse CPF.")
        return None
    aniversario = input(" Data de nascimento (dd/mm/aaaa): ").strip()
    curso = input(" Curso: ").strip()
    periodo = input(" Período (ex: 2º): ").strip()
    status = input(" Status acadêmico (ex: Ativo): ").strip()
    if not aniversario or not curso or not periodo or not status:
        print("\n [ERRO] Todos os campos são obrigatórios.")
        return None
    matricula = gerar_codigo_aluno()
    aluno = Aluno(nome, cpf, aniversario, curso, periodo, status, matricula)
    doc_aluno = {
        "matricula": aluno.get_matricula(),
        "nome": aluno.get_nome(),
        "cpf": aluno.get_cpf(),
        "aniversario": aluno.get_aniversario(),
        "curso": aluno.get_curso(),
        "periodo": aluno.get_periodo(),
        "status": aluno.get_status()
    }
    banco_dados.alunos.insert_one(doc_aluno)
    print("\n" + "=" * 36)
    print(" CADASTRO REALIZADO COM SUCESSO!  ".center(36))
    print("=" * 36)
    print(f"\n Sua matrícula (código de acesso): {matricula}")
    return matricula

def cadastrar_professor():
    print("\n" + "=" * 36)
    print(" CADASTRO DE PROFESSOR".center(36))
    print("=" * 36)
    nome = input(" Nome completo: ").strip()
    if not nome:
        print("\n Cadastro cancelado.")
        return None
    titulacao = input(" Titulação (ex: Mestre): ").strip()
    area = input(" Área de atuação: ").strip()
    disc_input = input(" Disciplinas (separadas por vírgula): ").strip()
    if not titulacao or not area or not disc_input:
        print("\n [ERRO] Todos os campos são obrigatórios.")
        return None
    disciplinas = []
    for d in disc_input.split(","):
        if d.strip():
            disciplinas.append(d.strip())
    codigo = gerar_codigo_professor()
    professor = Professor(nome, titulacao, area, disciplinas, codigo)
    doc_professor = {
        "codigo": professor.get_codigo(),
        "nome": professor.get_nome(),
        "titulacao": professor.get_titulacao(),
        "area": professor.get_area(),
        "disciplinas": professor.get_disciplinas()
    }
    banco_dados.professores.insert_one(doc_professor)
    print("\n" + "=" * 36)
    print(" CADASTRO REALIZADO COM SUCESSO!  ".center(36))
    print("=" * 36)
    print(f"\n  Seu código de acesso: {codigo}")
    return codigo

def menu_aluno(aluno):
    while True:
        print("\n" + "=" * 36)
        print(f" Olá, {aluno.get_nome().split()[0]}!")
        print(f" Matrícula: {aluno.get_matricula()}")
        print("=" * 36)
        print(" 1. Meu perfil")
        print(" 2. Horário de aulas")
        print(" 3. Notas e faltas")
        print(" 4. Boletim")
        print(" 5. Sair")
        opcao = input("\n  Opção: ").strip()
        if opcao == "1":
            aluno.exibir_perfil()
        elif opcao == "2":
            ver_horario_aluno(aluno.get_matricula())
        elif opcao == "3":
            ver_notas_aluno(aluno.get_matricula())
        elif opcao == "4":
            ver_boletim_aluno(aluno)
        elif opcao == "5":
            print("\n  Até logo!")
            break
        else:
            print("\n  [ERRO] Opção inválida.")

def ver_horario_aluno(matricula):
    print("\n" + "=" * 36)
    print(" HORÁRIO DE AULAS".center(36))
    print("=" * 36)
    turmas = buscar_turmas_do_aluno(matricula)
    if not turmas:
        print(" Você ainda não está matriculado em nenhuma turma.")
        return
    for t in turmas:
        print(f"\n Disciplina: {t.get_disciplina()}")
        print(f" Professor: {t.get_professor_nome() or 'N/A'}")
        print(f" Horário: {t.get_horario() or 'Não definido'}")
        print("  ─────────────────────────────")

def ver_notas_aluno(matricula):
    print("\n" + "=" * 36)
    print(" NOTAS E FALTAS".center(36))
    print("=" * 36)
    turmas = buscar_turmas_do_aluno(matricula)
    if not turmas:
        print(" Nenhuma disciplina encontrada.")
        return
    for t in turmas:
        nota = buscar_nota(t.get_turma_id(), matricula)
        np1 = nota["NP1"] if nota["NP1"] is not None else "—"
        np2 = nota["NP2"] if nota["NP2"] is not None else "—"
        faltas = nota["faltas"]
        total = nota["total_aulas"]
        print(f"\n  Disciplina: {t.get_disciplina()}")
        print(f" NP1: {np1}")
        print(f" NP2 : {np2}")
        print(f" Faltas: {faltas} / {total} aulas")
        print("  ─────────────────────────────")

def ver_boletim_aluno(aluno):
    print("\n" + "=" * 36)
    print("BOLETIM".center(36))
    print("=" * 36)
    print(f" Aluno: {aluno.get_nome()}")
    print(f" Matrícula: {aluno.get_matricula()}")
    print(f" Curso: {aluno.get_curso()}")
    print(f" Período: {aluno.get_periodo()}")
    print("─" * 36)
    turmas = buscar_turmas_do_aluno(aluno.get_matricula())
    if not turmas:
        print(" Nenhuma disciplina registrada.")
        return
    print(f"  {'Disciplina':<25} {'NP1':>5} {'NP2':>5} {'Média':>6} {'Faltas':>7} {'Sit.':>9}")
    print("  " + "─" * 61)
    for t in turmas:
        nota = buscar_nota(t.get_turma_id(), aluno.get_matricula())
        np1 = nota["NP1"]
        np2 = nota["NP2"]
        faltas = nota["faltas"]
        disc = t.get_disciplina()
        if np1 is not None and np2 is not None:
            media = (float(np1) + float(np2)) / 2
            sit = "APROVADO" if media >= 7.0 else "REPROVADO"
            print(f" {disc:<25} {float(np1):>5.1f} {float(np2):>5.1f} {media:>6.1f} {faltas:>7} {sit:>9}")
        else:
            print(f" {disc:<25} {'—':>5} {'—':>5} {'—':>6} {faltas:>7} {'—':>9}")
    print("─" * 36)

def menu_professor(professor):
    codigo = professor.get_codigo()
    while True:
        print("\n" + "=" * 36)
        print(f" Prof. {professor.get_nome().split()[0]}")
        print(f" Código: {codigo}")
        print("=" * 36)
        print(" 1. Meu perfil")
        print(" 2. Minhas disciplinas e horários")
        print(" 3. Listagem de turma")
        print(" 4. Controle de frequência e notas")
        print(" 5. Emitir boletim da turma")
        print(" 6. Sair")
        opcao = input("\n  Opção: ").strip()
        if opcao == "1":
            professor.exibir_perfil()
        elif opcao == "2":
            ver_disciplinas_professor(codigo)
        elif opcao == "3":
            ver_turma_professor(codigo)
        elif opcao == "4":
            lancar_frequencia_notas(codigo)
        elif opcao == "5":
            emitir_boletim_turma(codigo)
        elif opcao == "6":
            print("\n  Até logo!")
            break
        else:
            print("\n  [ERRO] Opção inválida.")

def ver_disciplinas_professor(codigo_prof):
    print("\n" + "=" * 36)
    print(" DISCIPLINAS E HORÁRIOS".center(36))
    print("=" * 36)
    turmas = buscar_turmas_do_professor(codigo_prof)
    if not turmas:
        print(" Nenhuma disciplina atribuída.")
        return
    for t in turmas:
        print(f"\n  Disciplina: {t.get_disciplina()}")
        print(f"  Horário: {t.get_horario() or 'Não definido'}")
        print("  ─────────────────────────────")

def ver_turma_professor(codigo_prof):
    print("\n" + "=" * 36)
    print(" LISTAGEM DE TURMA".center(36))
    print("=" * 36)
    turmas = buscar_turmas_do_professor(codigo_prof)
    if not turmas:
        print(" Nenhuma turma encontrada.")
        return
    for i, t in enumerate(turmas, 1):
        print(f"  {i}. {t.get_disciplina()} — {t.get_turma_id()}  ({len(t.get_alunos())} aluno(s))")
    try:
        idx = int(input("\n  Selecione a turma (número): ").strip()) - 1
        if idx < 0 or idx >= len(turmas):
            raise IndexError
    except (ValueError, IndexError):
        print("\n  [ERRO] Seleção inválida.")
        return
    turma = turmas[idx]
    print(f"\n  Disciplina: {turma.get_disciplina()}")
    print(f"  Turma ID  : {turma.get_turma_id()}")
    if not turma.get_alunos():
        print(" Nenhum aluno matriculado nesta turma.")
        return
    print(f"\n  {'#':<4} {'Matrícula':<16} {'Nome':<30}")
    print("  " + "─" * 52)
    for i, mat in enumerate(turma.get_alunos(), 1):
        aluno = buscar_aluno_por_matricula(mat)
        nome = aluno.get_nome() if aluno else "(não encontrado)"
        print(f"  {i:<4} {mat:<16} {nome:<30}")

def lancar_frequencia_notas(codigo_prof):
    print("\n" + "=" * 36)
    print(" CONTROLE DE FREQUÊNCIA/NOTAS".center(36))
    print("=" * 36)
    turmas = buscar_turmas_do_professor(codigo_prof)
    if not turmas:
        print(" Nenhuma turma encontrada.")
        return
    for i, t in enumerate(turmas, 1):
        print(f"  {i}. {t.get_disciplina()} — {t.get_turma_id()}")
    try:
        idx = int(input("\n  Selecione a turma: ").strip()) - 1
        if idx < 0 or idx >= len(turmas):
            raise IndexError
    except (ValueError, IndexError):
        print("\n [ERRO] Seleção inválida.")
        return
    turma = turmas[idx]
    if not turma.get_alunos():
        print("Nenhum aluno nesta turma.")
        return
    for i, mat in enumerate(turma.get_alunos(), 1):
        aluno = buscar_aluno_por_matricula(mat)
        nome = aluno.get_nome() if aluno else "(não encontrado)"
        print(f"  {i}. {mat} — {nome}")
    try:
        idx_aluno = int(input("\n Selecione o aluno: ").strip()) - 1
        if idx_aluno < 0 or idx_aluno >= len(turma.get_alunos()):
            raise IndexError
    except (ValueError, IndexError):
        print("\n [ERRO] Seleção inválida.")
        return
    matricula_aluno = turma.get_alunos()[idx_aluno]
    print(f"\n  Aluno: {matricula_aluno}")
    print("  O que deseja registrar?")
    print("  1. Lançar NP1")
    print("  2. Lançar NP2")
    print("  3. Registrar faltas")
    acao = input("\n  Opção: ").strip()
    try:
        if acao == "1":
            nota = float(input(" Nota NP1 (0 a 10): ").strip())
            if not (0 <= nota <= 10):
                raise ValueError("Nota fora do intervalo 0–10.")
            salvar_nota(turma.get_turma_id(), matricula_aluno, np1=nota)
            print("\n NP1 registrada com sucesso!")
        elif acao == "2":
            nota = float(input(" Nota NP2 (0 a 10): ").strip())
            if not (0 <= nota <= 10):
                raise ValueError("Nota fora do intervalo 0–10.")
            salvar_nota(turma.get_turma_id(), matricula_aluno, np2=nota)
            print("\n NP2 registrada com sucesso!")
        elif acao == "3":
            faltas = int(input(" Número de faltas: ").strip())
            total = int(input(" Total de aulas: ").strip())
            salvar_nota(turma.get_turma_id(), matricula_aluno, faltas=faltas, total_aulas=total)
            print("\n Frequência registrada com sucesso!")
        else:
            print("\n [ERRO] Opção inválida.")
    except ValueError as e:
        print(f"\n [ERRO] {e}")

def emitir_boletim_turma(codigo_prof):
    print("\n" + "=" * 36)
    print(" BOLETIM DA TURMA".center(36))
    print("=" * 36)
    turmas = buscar_turmas_do_professor(codigo_prof)
    if not turmas:
        print("Nenhuma turma encontrada.")
        return
    for i, t in enumerate(turmas, 1):
        print(f"  {i}. {t.get_disciplina()} — {t.get_turma_id()}")
    try:
        idx = int(input("\n  Selecione a turma: ").strip()) - 1
        if idx < 0 or idx >= len(turmas):
            raise IndexError
    except (ValueError, IndexError):
        print("\n [ERRO] Seleção inválida.")
        return
    turma = turmas[idx]
    print(f"\n Disciplina: {turma.get_disciplina()}")
    print(f"  Turma: {turma.get_turma_id()}")
    print(f"\n  {'Nome':<28} {'NP1':>5} {'NP2':>5} {'Média':>6} {'Faltas':>7} {'Sit.':>10}")
    print("  " + "─" * 65)
    for mat in turma.get_alunos():
        aluno = buscar_aluno_por_matricula(mat)
        nome = aluno.get_nome() if aluno else mat
        nota = buscar_nota(turma.get_turma_id(), mat)
        np1 = nota["NP1"]
        np2 = nota["NP2"]
        faltas = nota["faltas"]
        if np1 is not None and np2 is not None:
            media = (float(np1) + float(np2)) / 2
            sit = "APROVADO" if media >= 7.0 else "REPROVADO"
            print(f" {nome:<28} {float(np1):>5.1f} {float(np2):>5.1f} {media:>6.1f} {faltas:>7} {sit:>10}")
        else:
            print(f" {nome:<28} {'—':>5} {'—':>5} {'—':>6} {faltas:>7} {'—':>10}")
    print("─" * 36)

def tela_entrada():
    while True:
        print("\n" + "=" * 36)
        print(" SCHOOLCORE".center(36))
        print("=" * 36)
        print(" 1. Já tenho cadastro")
        print(" 2. Não tenho cadastro")
        print(" 3. Sair")
        opcao = input("\n  Opção: ").strip()
        if opcao == "1":
            fazer_login()
        elif opcao == "2":
            fazer_cadastro()
        elif opcao == "3":
            print("\n Sistema encerrado.\n")
            break
        else:
            print("\n [ERRO] Opção inválida. Escolha 1, 2 ou 3.")

def fazer_login():
    print("\n" + "=" * 36)
    print(" LOGIN".center(36))
    print("=" * 36)
    print(" Códigos de aluno começam com ALU")
    print(" Códigos de professor começam com PRO")
    codigo = input("\n Digite seu código de acesso: ").strip().upper()
    if codigo.startswith("ALU"):
        aluno = buscar_aluno_por_matricula(codigo)
        if not aluno:
            print("\n  [ERRO] Matrícula não encontrada.")
            return
        print(f"\n  ✔ Bem-vindo(a), {aluno.get_nome()}!")
        menu_aluno(aluno)
    elif codigo.startswith("PRO"):
        professor = buscar_professor_por_codigo(codigo)
        if not professor:
            print("\n  [ERRO] Código funcional não encontrado.")
            return
        print(f"\n  ✔ Bem-vindo(a), Prof. {professor.get_nome()}!")
        menu_professor(professor)
    else:
        print("\n [ERRO] Código inválido.")

def fazer_cadastro():
    print("\n" + "=" * 36)
    print(" NOVO CADASTRO".center(36))
    print("=" * 36)
    print(" Quem vai se cadastrar?")
    print(" 1. Aluno")
    print(" 2. Professor")
    tipo = input("\n  Opção: ").strip()
    if tipo == "1":
        codigo = cadastrar_aluno()
        if codigo:
            aluno = buscar_aluno_por_matricula(codigo)
            if aluno:
                print("\n Redirecionando para seu menu...")
                menu_aluno(aluno)
    elif tipo == "2":
        codigo = cadastrar_professor()
        if codigo:
            professor = buscar_professor_por_codigo(codigo)
            if professor:
                print("\nRedirecionando para seu menu...")
                menu_professor(professor)
    else:
        print("\n [ERRO] Opção inválida.")

def main():
    if not conectar_banco():
        return
    tela_entrada()

if __name__ == "__main__":
    main()