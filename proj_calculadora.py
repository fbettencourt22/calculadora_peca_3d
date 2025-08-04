import pandas as pd

VALOR_KWH = 0.158
CONSUMO_W = 140
CUSTO_MAO_OBRA = 20

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
    margem = float(input("Margem de lucro (%): ").replace(",", "."))

    preco_kwh = VALOR_KWH
    consumo_w = CONSUMO_W
    custo_mao_obra_hora = CUSTO_MAO_OBRA

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
    global df_pecas

    if df_pecas.empty:
        print("\n Nenhuma peça registada. ")
        return

    mostra_pecas()

    try:
        linha = int(input("Indique o id da linha a alterar: "))
        print("\nColunas disponíveis:")
        for i, col in enumerate(df_pecas.columns):
            print(f"{i} - {col}")
        idx_col = input("Escolha o número da coluna a editar: ")

        if not idx_col.isdigit() or int(idx_col) not in range(len(df_pecas.columns)):
            print(" Índice de coluna inválido!")
            return

        nome_coluna = df_pecas.columns[int(idx_col)]

        if linha not in df_pecas.index:
            print(f" Erro! O índice '{linha}' é inválido!")
            return

        if nome_coluna not in df_pecas.columns:
            print(f" Erro! A coluna '{nome_coluna}' não está registada!")
            return

        novo_dado = input(
            f"Indique o novo dado para o índice {linha}, na coluna {nome_coluna}: "
        )

        try:
            if nome_coluna in [
                "Filamento (g)",
                "Filamento (€/kg)",
                "Tempo (h)",
                "Mão de Obra (min)",
                "Margem (%)",
            ]:
                novo_dado = float(novo_dado.replace(",", "."))

        except ValueError:
            print(" Valor inválido para campo numérico!")
            return

        df_pecas.at[linha, nome_coluna] = novo_dado
        print(" Valor atualizado.")

        if nome_coluna in [
            "Filamento (g)",
            "Filamento (€/kg)",
            "Tempo (h)",
            "Mão de Obra (min)",
            "Margem (%)",
        ]:
            recalcular_pecas(linha)

    except ValueError:
        print(" Erro! O id da linha deve ser um número inteiro.")

    print()


def editar_configuracoes_fixas():
    global VALOR_KWH, CONSUMO_W, CUSTO_MAO_OBRA

    while True:
        print("\n  Editar valores fixos:")
        print(f"1 - Preço da energia (€/kWh): {VALOR_KWH}")
        print(f"2 - Consumo da impressora (W): {CONSUMO_W}")
        print(f"3 - Custo de mão de obra (€/hora): {CUSTO_MAO_OBRA}")
        print("4 - Voltar ao menu\n")

        escolha = input("Escolha o número da opção que deseja alterar: ")

        if escolha == "1":
            try:
                novo = float(input("Novo preço da energia (€/kWh): ").replace(",", "."))
                VALOR_KWH = novo
                print(" Valor atualizado.")
            except ValueError:
                print(" Entrada inválida.")
        elif escolha == "2":
            try:
                novo = float(
                    input("Novo consumo da impressora (W): ").replace(",", ".")
                )
                CONSUMO_W = novo
                print(" Valor atualizado.")
            except ValueError:
                print(" Entrada inválida.")
        elif escolha == "3":
            try:
                novo = float(
                    input("Novo custo de mão de obra (€/hora): ").replace(",", ".")
                )
                CUSTO_MAO_OBRA = novo
                print(" Valor atualizado.")
            except ValueError:
                print(" Entrada inválida.")
        elif escolha == "4":
            break
        else:
            print(" Opção inválida.")

        recalcular_pecas()


def recalcular_pecas(linha=None, usar_valores_globais=True):
    global df_pecas, VALOR_KWH, CONSUMO_W, CUSTO_MAO_OBRA

    linhas = [linha] if linha is not None else df_pecas.index

    for index in linhas:
        try:
            row = df_pecas.loc[index]

            preco_filamento_kg = float(row["Filamento (€/kg)"])
            quantidade_filamento_g = float(row["Filamento (g)"])
            tempo_horas = float(row["Tempo (h)"])
            tempo_mao_obra_min = float(row["Mão de Obra (min)"])
            margem = float(row["Margem (%)"])

            consumo_w = CONSUMO_W if usar_valores_globais else float(row["Consumo (W)"])
            valor_kwh = (
                VALOR_KWH if usar_valores_globais else float(row["Energia (€/kWh)"])
            )
            custo_mao_obra_hora = CUSTO_MAO_OBRA

            custo_filamento = (
                (preco_filamento_kg / 1000) * quantidade_filamento_g
            ) * 1.10
            consumo_kwh = (consumo_w * tempo_horas) / 1000
            custo_energia = consumo_kwh * valor_kwh
            custo_mao_obra = (tempo_mao_obra_min / 60) * custo_mao_obra_hora
            custo_total = (
                custo_filamento + custo_energia + custo_mao_obra + (0.15 * tempo_horas)
            )
            preco_final = custo_total / (1 - (margem / 100))

            df_pecas.at[index, "Custo Mão de Obra (€)"] = round(custo_mao_obra, 2)
            df_pecas.at[index, "Custo Energia (€)"] = round(custo_energia, 2)
            df_pecas.at[index, "Custo Filamento (€)"] = round(custo_filamento, 2)
            df_pecas.at[index, "Custo Total (€)"] = round(custo_total, 2)
            df_pecas.at[index, "Preço Final (€)"] = round(preco_final, 2)

            if usar_valores_globais:
                df_pecas.at[index, "Energia (€/kWh)"] = round(VALOR_KWH, 3)
                df_pecas.at[index, "Consumo (W)"] = round(CONSUMO_W, 2)

        except Exception as e:
            print(f"Erro ao recalcular linha {index}: {e}")


while True:
    print("Bem-Vindo(a)")
    print("1 - Inserir Peça")
    print("2 - Consultar Peças ")
    print("3 - Editar valor ")
    print("4 - Editar valores pre definidos")
    print("5 - Sair do Programa ")

    escolha = input("Indique a opção a executar: ")

    if escolha == "1":
        inserir_peca()
    elif escolha == "2":
        mostra_pecas()
    elif escolha == "3":
        editar_valor()
    elif escolha == "4":
        editar_configuracoes_fixas()
    elif escolha == "5":
        print("Obrigado!")
        break
    else:
        print("Erro Opção Inválida! ")
