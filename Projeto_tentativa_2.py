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

        try:
            nivel = int(input('Nível do conhecimento: '))

            if nivel == 1:
                nivel = 'APRENDIZ'
            elif nivel == 2:
                nivel = 'CIENTE'
            elif nivel == 3:
                nivel = 'GENERALISTA'
            elif nivel == 4:
                nivel = 'ESPECIALISTA'

        except:
            print('\033[31mNível não é válido.\033[0;0m')
        else:
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
            opcao = int(input('O que deseja editar: '))

            if opcao == 1:
                novo_nome = input("Digite o novo nome: ")
                cadastro['nome'] = novo_nome
                salvar_cadastros(cadastros)
                print('\033[32mNome atualizado com sucesso.\033[0;0m')

            elif opcao == 2:
                nova_graduacao = input("Digite a nova formação: ")
                cadastro['formacao'] = nova_graduacao
                salvar_cadastros(cadastros)
                print('\033[32mFormação atualizada com sucesso.\033[0;0m')

            elif opcao == 3:
                print('Conhecimentos atuais:')
                for conhecimento, nivel in cadastro['competencias'].items():
                    print(f"- {conhecimento}: {nivel}")

                while True:
                    acao = int(input(
                        'Digite 1 - Para Adicionar um Conhecimento, 2 - Para Remover um Conhecimento, ou 3 - Cancelar: '))

                    if acao == 1:
                        novo_conhecimento = input('Digite o novo conhecimento: ')

                        novo_nivel = int(input('Digite o nível desse conhecimento: '))

                        if novo_nivel == 1:
                            novo_nivel = 'APRENDIZ'
                        elif novo_nivel == 2:
                            novo_nivel = 'CIENTE'
                        elif novo_nivel == 3:
                            novo_nivel = 'GENERALISTA'
                        elif novo_nivel == 4:
                            novo_nivel = 'ESPECIALISTA'

                        cadastro['conhecimentos'][novo_conhecimento] = novo_nivel
                        salvar_cadastros(cadastros)

                        print('\033[32mCompetência adicionada com sucesso.\033[0;0m')

                    elif acao == 2:
                        conhecimento_remover = input("Digite o conhecimento que deseja remover: ")

                        if conhecimento_remover in cadastro['conhecimentos']:
                            del cadastro['conhecimentos'][conhecimento_remover]
                            salvar_cadastros(cadastros)

                            print('\033[32mCompetência removida com sucesso.\033[0;0m')

                        else:
                            print('Competência não encontrada.')

                    elif acao == 3:
                        break

                    else:
                        print('\033[31mOpção inválida. Digite novamente.\033[0;0m')

            elif opcao == 4:
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

            elif opcao == 5:
                print('Edição cancelada.')
            else:
                print('\033[31mOpção inválida.\033[0;0m')

            break
    else:
        print('ID não encontrado.')


# Função que vai mostrar o menu.
def exibir_menu():
    print(30 * '=')
    print('MENU'.center(30))
    print('PROJETOS EDUCACIONAIS'.center(30))
    print(30 * '=')
    print('1. CONSULTAR CADASTROS')
    print('2. CADASTRAR NOVO USUÁRIO')
    print('3. EDITAR USUÁRIOS')
    print('4. SAIR')
    print(30 * '=')


# Programa Principal:
while True:

    exibir_menu()
    opcao = int(input('Digite a opção desejada: '))

    if opcao == 1:
        consultar_cadastros()
    elif opcao == 2:
        cadastrar_usuario()
    elif opcao == 3:
        editar_usuario()
    elif opcao == 4:
        print('Programa encerrado.')
        break
    else:
        print('\033[31mOpção inválida. Digite novamente.\033[0;0m')

    sleep(1.5)
