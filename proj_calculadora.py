import pandas as pd

df_pecas = pd.DataFrame(
    columns=[
        "Peça",
        "Material",
        "Filamento (g)",
        "Filamento (€/kg)",
        "Custo Filamento (€)",
        "Tempo (h)",
        "Energia (€/kWh)",
        "Consumo (W)",
        "Custo Energia (€)",
        "Mão de Obra (min)",
        "Custo Mão de Obra (€)",
        "Margem (%)",
        "Custo Total (€)",
        "Preço Final (€)",
    ]
)


def inserir_peca():

    print("\n   Inserir nova peça")
    nome = input("Nome peça: ")
    material = input("Material (ex: PLA): ")
    preco_filamento_kg = float(input("Preço do Filamento (€/kg): ").replace(",", "."))
    quantidade_filamento_g = int(input("Filamento usado (g): "))
    tempo_horas = float(input("Tempo de impressao (h): ").replace(",", "."))
    tempo_mao_obra_min = float(input("Tempo de trabalho (min): ").replace(",", "."))
    preco_kwh = float(input("Preço da eletricidade (€/kWh): ").replace(",", "."))
    consumo_w = float(input("Consumo da impressora (W): ").replace(",", "."))
    custo_mao_obra_hora = float(input("Custo mao de obra (€/hora): ").replace(",", "."))
    margem = float(input("Margem de lucro (%): ").replace(",", "."))

    # Cálculos
    custo_filamento = ((preco_filamento_kg / 1000) * quantidade_filamento_g) * 1.10
    consumo_kwh = (consumo_w * tempo_horas) / 1000
    custo_energia = consumo_kwh * preco_kwh
    custo_mao_obra = (tempo_mao_obra_min / 60) * custo_mao_obra_hora
    custo_total = (
        custo_filamento + custo_energia + custo_mao_obra + (0.15 * tempo_horas)
    )
    preco_final = custo_total / (1 - (margem / 100))

    df_pecas.loc[len(df_pecas)] = [
        nome,
        material,
        quantidade_filamento_g,
        preco_filamento_kg,
        round(custo_filamento, 2),
        tempo_horas,
        preco_kwh,
        consumo_w,
        round(custo_energia, 2),
        tempo_mao_obra_min,
        round(custo_mao_obra, 2),
        margem,
        round(custo_total, 2),
        round(preco_final, 2),
    ]

    print(f"\n Peça '{nome}' adicionada com sucesso!\n")


def mostra_pecas():

    global df_pecas
    if df_pecas.empty:
        print("\n Nenhuma peça registada. ")
    else:
        print("\n      LISTA DE PEÇAS      ")
        print(df_pecas)
        print()


def editar_valor():
    global df
    if df_pecas.empty:
        print("Data Frame vazio! ")
        return
    mostra_pecas()
    try:
        linha = int(input("Indique o id da linha a alterar: "))
        nome_coluna = input("Indique em qual coluna pretende alterar o dado: ")

        if linha not in df_pecas.index:
            print(f"Erro! O índice '{linha}' é inválido! ")
            return None

        if nome_coluna not in df_pecas.columns:
            print(f"Erro! A coluna '{nome_coluna}' não está registada! ")
            return None

        novo_dado = input(
            f"Indique o novo dado para o índice {linha}, na coluna {nome_coluna}: "
        )
        df_pecas.at[linha, nome_coluna] = novo_dado
        print("Dados atualizados com sucesso! ")
    except ValueError:
        print("Erro! O id da linha deve ser um nº inteiro! ")
    print()


while True:
    print("Bem-Vindo(a)")
    print("1 Inserir Peça")
    print("2 Consultar Peças ")
    print("3 Editar valor ")
    ##print("4 Remover Coluna no Data Frame ")
    print("4 Sair do Programa ")

    escolha = input("Indique a opção a executar: ")

    if escolha == "1":
        inserir_peca()
    elif escolha == "2":
        mostra_pecas()
    elif escolha == "3":
        editar_valor()
    ##elif escolha == "4":
    ##eliminar_coluna()
    elif escolha == "4":
        print("Obrigado!")
        break
    else:
        print("Erro Opção Inválida! ")
