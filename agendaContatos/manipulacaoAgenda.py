import json


contatosSuportados = ("Telefone", "E-mail", "Endereço")
#tupla

agenda = {
    "Leticia":{
        "telefone":["11 1234-5678"],
        "email":["pessoa@email.com", "email@profissional.com"],
        "endereco":["Rua 123"]
    },
    "Davi":{
        "telefone":["11 9874-5678"],
        "email":["pessoa2@email.com", "pessoa2@profissional.com"],
        "endereco":["Rua 345"]
    }
}

def agenda_para_txt(nomeArquivo:str, agenda):
    if "txt" not in nomeArquivo:
        nomeArquivo = f"{nomeArquivo}.txt"
    with open(nomeArquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(agenda_para_texto(**agenda))
        print("Agenda exportada com sucesso!")

def json_para_agenda(nomeArquivo:str):
    with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    print("Agenda carregada com sucesso!")
    return json.loads(conteudo)

def agenda_para_json(nomeArquivo:str, agenda):
    if ".json" not in nomeArquivo:
        nomeArquivo = f"{nomeArquivo}.json"
    with open(nomeArquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(agenda, indent=4, ensure_ascii=False))
        print("Agenda exportada com sucesso!")
    

def contato_para_texto(nomeContato:str, **formasContato):
    """Recebe um nome de contato com string e um dicionário
     com as formas de contato.
     Retorna uma string com os dados recebidos"""
    formatoTexto = f"{nomeContato}"
    for meioContato, contato in formasContato.items():
        formatoTexto = f"{formatoTexto}\n{meioContato.upper()}"
        contadorFormas = 1
        for valor in contato:
            formatoTexto = f"{formatoTexto}\n\t{contadorFormas} - {valor.upper()}"
            contadorFormas = contadorFormas + 1

    return formatoTexto

def agenda_para_texto(**agendaCompleta):
    """Recebe um dicionário de dicionários com a agenda que será exibida e 
    retorna uma string com este dicionário formatado"""
    formatoTexto = ""
    for nomeContato, formasContato in agendaCompleta.items():
        formatoTexto = f"{formatoTexto}{contato_para_texto(nomeContato, **formasContato)}\n"
        formatoTexto = f"{formatoTexto}---------------------------\n"
    return formatoTexto


def altera_nome_contato(agendaOriginal:dict, nomeOriginal:str, nomeAtualizado:str):
    """Recebe a agenda original em forma de dicionário, o nome_original e o nome_atualizado em forma
    de string. 
    Busca o nome original no dicionário e retorna False se não encontrar.
    Retorna True se encontrar o nome original no dicionário e fizer a exclusão do contato antigo e inclusão do novo"""
    if nomeOriginal in agendaOriginal.keys():
        copiaContatos = agendaOriginal[nomeOriginal].copy()
        agendaOriginal.pop(nomeOriginal)
        agendaOriginal[nomeAtualizado] = copiaContatos
        return True
    return False


def altera_forma_contato(listaContatos:list, valorAntigo:str, novoValor:str):
    """Recebe uma list lista_contatos, o valor antigo que será substituído e o novo valor
    Caso o valor antigo não esteja na lista, retornará False.
    Caso o valor antigo esteja na lista, será removido, o novo valor será incluido e retornará True
    """
    if valorAntigo in listaContatos:
        posicaoValorAntigo = listaContatos.index(valorAntigo)
        listaContatos.pop(posicaoValorAntigo)
        listaContatos.insert(posicaoValorAntigo, novoValor)
        return True
    return False

def exclui_contato(agenda: dict, nomeContato: str):
    """Recebe uma agenda completa como dicionário e o nome do contato como string.
    Caso o nome do contato não esteja nas chaves do dicionário, retornará False.
    Caso o nome do contato esteja nas chaves, o registro correspondente será removido 
    depois de uma confirmação e retornará True, ou False se a confirmação for negativa."""
    
    if nomeContato in agenda.keys():
        # Perguntando ao usuário se ele tem certeza da exclusão
        confirmacao = input(f"Você tem certeza que deseja excluir o contato '{nomeContato}'? (s/n): ")
        if confirmacao.lower() == 's':  # Se a resposta for 's', exclui o contato
            agenda.pop(nomeContato)
            print(f"Contato '{nomeContato}' foi excluído com sucesso.")
            return True
        else:
            print(f"Exclusão do contato '{nomeContato}' cancelada.")
            return False
    else:
        return False

def inclui_contato(agenda:dict, nomeContato:str, **formasContato):
    """Recebe uma agenda completa como dicionário, o nome do novo contato como string e as formas de contato
    em um dicionário como **kwargs.
    Não é feita nenhuma verifição, portanto se já existir um contato com o mesmo nome, será sobrescrito"""
    #print(formas_contato)
    agenda[nomeContato] = formasContato

def inclui_forma_contato(formasContato:dict, formaIncluida:str, valorIncluido:str):
    """Recebe um dicionário com as formas de contato, a forma de contato que será incluida ou 
    alterada e o valor que será incluído.
    Caso a forma de contato já possua valores, o novo valor será adicionado na lista e retornará True.
    Caso a forma de contato ainda não exista e estiver presente na tupla de formas de contatos suportados
     será incluída e o novo valor será incluído em uma lista, retornando True.
     Caso a forma de contato ainda não exista e não estiver presente na tupla de formas de contato suportados,
     retornará False"""
    if formaIncluida in formasContato.keys():
        formasContato[formaIncluida].append(valorIncluido)
        return True
    elif formaIncluida in contatosSuportados:
        formasContato[formaIncluida] = [valorIncluido]
        return True
    return False

def usuario_inclui_contato(agenda:dict):
    nome = input("Informe o nome do novo contato que será inserido na agenda: ")
    dicionarioFormas = {}
    for forma in contatosSuportados:
        resposta = input(f"Deseja inserir um {forma} para {nome.upper()}? \nSIM ou NÃO -> ")
        listaContatos = []
        while "S" in resposta.upper():
            listaContatos.append(input(f"Informe um {forma}: "))
            resposta = input(f"Deseja inserir outro {forma} para {nome.upper()}?\nSIM ou NÃO -> ")
        if len(listaContatos) > 0:
            dicionarioFormas[forma] = listaContatos.copy()
            listaContatos.clear()
    if len(dicionarioFormas.keys()) > 0:
        inclui_contato(agenda, nome, **dicionarioFormas)
        print("Inclusão bem sucedida!")
    else:
        print("É necessário incluir pelo menos uma forma de contato!\nA agenda não foi alterada.")

def usuario_inclui_forma_contato(agenda:dict):
    #inclui_forma_contato(formas_contato:dict, forma_incluida:str, valor_incluido:str):
    nome = input("Informe o nome do contato para o qual deseja incluir formas de contato ")
    if nome in agenda.keys():
        print(f"As formas de contato suportadas pelo sistema são: {contatosSuportados}")
        formaIncluida = input("Qual forma de contato deseja incluir? ")
        if formaIncluida in contatosSuportados:
            valorIncluido = input(f"Informe o {formaIncluida} que deseja incluir: ")
            if inclui_forma_contato(agenda[nome], formaIncluida, valorIncluido):
                print("Operação bem sucedida! A nova forma de contato foi incluida! ")
            else:
                print("Ocorreu um erro durante a inserção. A agenda não foi alterada.")
        else:
            print("A forma de contato indicada não é suportada pelo sistema. A agenda não foi alterada.")
    else:
        print("O contato informado não existe na agenda. Não foram feitas alterações. ")

def usuario_exclui_contato(agenda:dict):
    nome = input("Informe o nome do contato que deseja excluir: ")
    if exclui_contato(agenda, nome):
        print("Usuário excluido com sucesso!")
    else:
        print("Nome do usuário não localizado na agenda. Não foram feitas alterações.")

def usuario_altera_forma_contato(agenda:dict):
    nome = input("Informe o nome do contato que deseja alterar: ")
    if nome in agenda.keys():
        print(f"As formas de contato suportadas pelo sistema são: {contatosSuportados}")
        formaIncluida = input("Qual forma de contato deseja incluir? ")
        if formaIncluida in contatosSuportados:
            print(contato_para_texto(nome, **agenda[nome]))
            valorAntigo = input(f"Informe o {formaIncluida} que deseja alterar " )
            novaValor = input(f"Informe o novo {formaIncluida} ")
            if altera_forma_contato(agenda[nome][formaIncluida], valorAntigo, novaValor):
                print("Contato alterado com sucesso!")
            else:
                print("Ocorreu um erro durante a alteração do contato. A agenda não foi alterada.")
        else:
            print(f"{formaIncluida} nõa é uma forma de contato suportada pelo sistema. A agenda não foi alterada.")
    else:
        print(f"O contato {nome} não está na agenda. A agenda não foi alterada.")

def usuario_altera_nome_contato(agenda:dict):
    #altera_nome_contato(agenda_original:dict, nome_original:str, nome_atualizado:str):
    nomeOriginal = input("Informe o nome do contato que deseja alterar: ")
    nomeAtualizado = input("Informe o nome do novo contato: ")
    if altera_nome_contato(agenda, nomeOriginal, nomeAtualizado):
        print(f"O contato foi atualizado e agora se chama {nomeAtualizado}")
    else:
        print(f"O contato original não foi localizado. A agenda não foi alterada.")

def usuario_contato_para_texto(agenda:dict):
    nome = input("Informe o nome do contato que deseja exibir: ")
    if nome in agenda.keys():
        print(contato_para_texto(nome, **agenda[nome]))
    else:
        print("O contato informado não está na agenda.")


def exibe_menu():
    print("\n\n")
    print("1 - Incluir contato na agenda")
    print("2 - Incluir uma forma de contato")
    print("3 - Alterar o nome de um contato")
    print("4 - Alterar uma forma de contato")
    print("5 - Exibir um contato")
    print("6 - Exibir toda a agenda")
    print("7 - Excluir um contato")
    print("8 - Exportar agenda para txt")
    print("9 - Exportar agenda para JSON")
    print("10 - Importar agenda de JSON")
    print("11 - Sair")
    print("\n")

def manipulador_agenda():
    agenda = {}
    op = 1
    while op != 11:
        exibe_menu()
        op = int(input("Informe a opção desejada: "))
        if op == 1:
            usuario_inclui_contato(agenda)
        elif op == 2:
            usuario_inclui_forma_contato(agenda)
        elif op == 3:
            usuario_altera_nome_contato(agenda)
        elif op == 4:
            usuario_altera_forma_contato(agenda)
        elif op == 5:
            usuario_contato_para_texto(agenda)
        elif op == 6:
            print(agenda_para_texto(**agenda))
        elif op == 7:
            usuario_exclui_contato(agenda)
        elif op == 8:
            nomeArquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda_para_txt(nomeArquivo, agenda)
        elif op == 9:
            nomeArquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda_para_json(nomeArquivo, agenda)
        elif op == 10:
            nomeArquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda = json_para_agenda(nomeArquivo)
        elif op == 11:
            print("Saindo do sistema")
            break
        else:
            print("Opção inválida! Informe uma opção existente.")


manipulador_agenda()