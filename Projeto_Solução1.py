import json
from time import sleep


# Função para carregar os cadastros, tenta abrir o arquivo, se não existir, cria uma lista.
def carregar_cadastros():
    try:
        with open('cadastros.json', 'r') as arquivo:
            cadastros = json.load(arquivo)
    except FileNotFoundError:
        cadastros = []

    return cadastros


# Função que salva o cadastro passado como parâmetro.
def salvar_cadastros(cadastros):
    with open('cadastros.json', 'w') as arquivo:
        json.dump(cadastros, arquivo, indent=2)


# Função que vai consultar os usuários cadastrados e mostrar.
def consultar_cadastros():
    cadastros = carregar_cadastros()
    if not cadastros:
        print('\033[31mNão há cadastros disponíveis.\033[0;0m')
    else:
        for cadastro in cadastros:
            print(f"ID: {cadastro['id']}")
            print(f"Nome: {cadastro['nome']}")
            print(f"Formação: {cadastro['formacao']}")
            print("Conhecimentos:")
            for conhecimento, nivel in cadastro['conhecimentos'].items():
                print(f"- {conhecimento}: {nivel}")
            print(30 * '=')


# Função que vai cadastrar novo usuário.
def cadastrar_usuario():
    nome = input('Nome: ').upper()
    formacao = input('Formação: ').upper()

    conhecimentos = {}

    r = int(input(f'Quantos conhecimentos deseja adicionar para {nome}? '))

    for c in range(r):
        conhecimento = input('Conhecimento: ').upper()

        print('\033[33mNíveis: 1 - Aprendiz; 2 - Ciente; 3 - Generalista; 4 - Especialista\033[0;0m')

        while True:
            nivel = input('Nível do conhecimento: ')

            if nivel == '1':
                nivel = 'APRENDIZ'
                break
            elif nivel == '2':
                nivel = 'CIENTE'
                break
            elif nivel == '3':
                nivel = 'GENERALISTA'
                break
            elif nivel == '4':
                nivel = 'ESPECIALISTA'
                break
            else:
                print('\033[31mNível não é válido.\033[0;0m')

        conhecimentos[conhecimento] = nivel

    # Vai chamar a função "carregar_cadastros()".
    cadastros = carregar_cadastros()
    # Criar o id do usuário.
    id_usuario = len(cadastros) + 1

    # Criar um dicionário com as informações recebidas.
    novo_usuario = {
        'id': id_usuario,
        'nome': nome,
        'formacao': formacao,
        'conhecimentos': conhecimentos
    }

    # Append do novo cadastro para a lista "cadastros".
    cadastros.append(novo_usuario)
    # Chama a função "salvar_cadastros".
    salvar_cadastros(cadastros)
    print("\033[32mUsuário cadastrado com sucesso.\033[0;0m")


# Função que vai editar usuários cadastrados.
def editar_usuario():
    cadastros = carregar_cadastros()
    if not cadastros:
        print('\033[31mNão há cadastros disponíveis.\033[0;0m')
        return

    print('Usuários disponíveis para edição:')

    # Vai mostrar o id e o nome dos usuários que estão no arquivo.
    for cadastro in cadastros:
        print(f"{cadastro['id']} - {cadastro['nome']}")

    id_usuario = input('Digite o ID do usuário que deseja editar: ')

    for cadastro in cadastros:
        if str(cadastro['id']) == id_usuario:
            print(f"Editar usuário ID: {cadastro['id']}")
            print(f"Nome atual: {cadastro['nome']}")
            print(f"Formação atual: {cadastro['formacao']}")
            print('Conhecimentos atuais:')
            for conhecimento, nivel in cadastro['conhecimentos'].items():
                print(f"- {conhecimento}: {nivel}")
            print("=" * 30)

            print(30 * '=')
            print('EDIÇÃO DE USUÁRIO'.center(30))
            print(30 * '=')
            print('1 - Editar Nome, 2 - Editar Formação, 3 - Editar Conhecimentos, 4 - Excluir Usuário, 5 - Cancelar')
            opcao = input('O que deseja editar: ')

            if opcao == '1':
                novo_nome = input("Digite o novo nome: ").upper()
                cadastro['nome'] = novo_nome
                salvar_cadastros(cadastros)
                print('\033[32mNome atualizado com sucesso.\033[0;0m')

            elif opcao == '2':
                nova_graduacao = input("Digite a nova formação: ").upper()
                cadastro['formacao'] = nova_graduacao
                salvar_cadastros(cadastros)
                print('\033[32mFormação atualizada com sucesso.\033[0;0m')

            elif opcao == '3':
                print('Conhecimentos atuais:')
                for conhecimento, nivel in cadastro['conhecimentos'].items():
                    print(f"- {conhecimento}: {nivel}")

                while True:
                    acao = input(
                        'Digite 1 - Para Adicionar um Conhecimento, 2 - Para Remover um Conhecimento, ou 3 - Cancelar: ')

                    if acao == '1':
                        novo_conhecimento = input('Digite o novo conhecimento: ').upper()

                        while True:
                            print(f'\033[33mNíveis: 1 - Aprendiz; 2 - Ciente; 3 - Generalista; 4 - '
                                  f'Especialista\033[0;0m')
                            novo_nivel = input('Digite o nível desse conhecimento: ')

                            if novo_nivel == '1':
                                novo_nivel = 'APRENDIZ'
                                break
                            elif novo_nivel == '2':
                                novo_nivel = 'CIENTE'
                                break
                            elif novo_nivel == '3':
                                novo_nivel = 'GENERALISTA'
                                break
                            elif novo_nivel == '4':
                                novo_nivel = 'ESPECIALISTA'
                                break
                            else:
                                print('\033[31mOpção inválida.\033[0;0m')

                        cadastro['conhecimentos'][novo_conhecimento] = novo_nivel
                        salvar_cadastros(cadastros)

                        print('\033[32mCompetência adicionada com sucesso.\033[0;0m')

                    elif acao == '2':
                        conhecimento_remover = input("Digite o conhecimento que deseja remover: ").upper()

                        if conhecimento_remover in cadastro['conhecimentos']:
                            del cadastro['conhecimentos'][conhecimento_remover]
                            salvar_cadastros(cadastros)

                            print('\033[32mCompetência removida com sucesso.\033[0;0m')

                        else:
                            print('Competência não encontrada.')

                    elif acao == '3':
                        break

                    else:
                        print('\033[31mOpção inválida. Digite novamente.\033[0;0m')

            elif opcao == '4':
                id_excluir = int(input('Confirme o ID do usuário que deseja excluir: '))
                if int(id_usuario) == id_excluir:
                    for i in range(len(cadastros)):
                        if cadastros[i]['id'] == id_excluir:
                            del cadastros[i]
                            salvar_cadastros(cadastros)
                            break
                    print('Usuário excluído.')

                else:
                    print('\033[31mID não confirmado. Operação cancelada.\033[0;0m')

            elif opcao == '5':
                print('Edição cancelada.')
            else:
                print('\033[31mOpção inválida.\033[0;0m')

            break
    else:
        print('ID não encontrado.')


# Função que vai buscar usuários pelo conhecimento que possuem.
def buscar_conhecimento():
    cadastros = carregar_cadastros()
    if not cadastros:
        print('\033[31mNão há cadastros disponíveis.\033[0;0m')

    resp = input('Insira o conhecimento que deseja buscar: ').upper()
    print(f'Opção escolhida: \033[33m{resp}\033[0;0m')

    for cadastro in cadastros:
        for conhecimento, nivel in cadastro['conhecimentos'].items():
            if conhecimento == resp:
                print(30 * '=')

                print(f"{cadastro['id']} - {cadastro['nome']}")
                print(f"Formação: {cadastro['formacao']}")
                print("Conhecimentos:")
                print(f"- {conhecimento}: {nivel}")

    if resp not in cadastro['conhecimentos']:
        print(f'\033[31mNão há cadastrados com conhecimento em {resp}.\033[0;0m')


# Função que vai mostrar o menu.
def exibir_menu():
    print(30 * '=')
    print('MENU'.center(30))
    print('PROJETOS EDUCACIONAIS'.center(30))
    print(30 * '=')
    print("""
    1. CONSULTAR CADASTROS
    2. CADASTRAR NOVO USUÁRIO
    3. EDITAR USUÁRIOS
    4. BUSCAR CONHECIMENTO
    5. SAIR
    """)
    print(30 * '=')


# Programa Principal:
while True:

    exibir_menu()
    opcao = input('Digite a opção desejada: ')

    if opcao == '1':
        consultar_cadastros()
    elif opcao == '2':
        cadastrar_usuario()
    elif opcao == '3':
        editar_usuario()
    elif opcao == '4':
        buscar_conhecimento()
    elif opcao == '5':
        print('Programa encerrado.')
        break
    else:
        print('\033[31mOpção inválida. Digite novamente.\033[0;0m')

    sleep(1.5)
