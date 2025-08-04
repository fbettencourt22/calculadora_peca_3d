import pandas as pd
import matplotlib.pyplot as plt

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

    df_pecas.index = range(1, len(df_pecas) + 1)

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


def exportar_excel():
    global df_pecas
    if df_pecas.empty:
        print("\n Nenhuma peça registada. ")
        return

    print("\nLinhas disponíveis para exportar:")
    print(df_pecas)

    linhas_str = input(
        "Indique os números das linhas que quer exportar (separados por vírgula), ou ENTER para todas: "
    ).strip()

    if linhas_str == "":
        df_exportar = df_pecas.copy()
    else:
        try:

            linhas = [int(x) for x in linhas_str.split(",")]

            df_exportar = df_pecas.loc[linhas]
        except Exception as e:
            print(f"Entrada inválida ou linhas não encontradas: {e}")
            return

    nome_ficheiro = input("Introduza o nome do ficheiro a guardar: ").strip()

    if not nome_ficheiro.endswith(".xlsx"):
        nome_ficheiro += ".xlsx"

    try:
        df_exportar.to_excel(nome_ficheiro, index=False)
        print(f"Dados exportados com sucesso para: {nome_ficheiro}")
    except Exception as e:
        print(f"Erro ao gerar ficheiro: {e}")
    print()


def importar_excel():
    global df_pecas

    nome_ficheiro = input("Introduza o nome do ficheiro a importar: ")

    if not nome_ficheiro.endswith(".xlsx"):
        nome_ficheiro += ".xlsx"

    try:
        novo_df = pd.read_excel(nome_ficheiro)

        if df_pecas.empty:
            df_pecas = novo_df.copy()
            df_pecas.index = range(1, len(df_pecas) + 1)
        else:
            novo_df = novo_df.reindex(columns=df_pecas.columns)

            max_index = df_pecas.index.max()
            if pd.isna(max_index):
                max_index = 0
            else:
                max_index = int(max_index)

            novo_df.index = range(max_index + 1, max_index + 1 + len(novo_df))

            df_pecas = pd.concat([df_pecas, novo_df])

        print(f"{nome_ficheiro} importado e adicionado com sucesso!")
    except FileNotFoundError:
        print(f"Erro! {nome_ficheiro} não encontrado! ")
    except Exception as e:
        print(f"Erro ao importar ficheiro: {e}")
    print()


def filtro_dataframe():
    global df_pecas
    if df_pecas.empty:
        print("\n Nenhuma peça registada. ")
        return

    print("\nColunas disponíveis:")
    for i, col in enumerate(df_pecas.columns):
        print(f"{i} - {col}")

    idx_col = input("Escolha o número da coluna a filtrar: ")

    if not idx_col.isdigit() or int(idx_col) not in range(len(df_pecas.columns)):
        print(" Índice de coluna inválido!")
        return

    nome_coluna = df_pecas.columns[int(idx_col)]
    tipo_dado = df_pecas[nome_coluna].dtype

    filtro = None

    try:
        if pd.api.types.is_numeric_dtype(tipo_dado):
            critério = float(
                input(f"Indique o valor a filtrar na coluna '{nome_coluna}': ").replace(
                    ",", "."
                )
            )
            filtro = df_pecas[df_pecas[nome_coluna] == critério]

        elif pd.api.types.is_datetime64_any_dtype(tipo_dado):
            critério = pd.to_datetime(
                input(f"Indique a data (DD/MM/AAAA) para filtrar '{nome_coluna}': "),
                dayfirst=True,
            )
            filtro = df_pecas[df_pecas[nome_coluna] == critério]

        else:
            critério = input(
                f"Indique o texto a procurar na coluna '{nome_coluna}': "
            ).lower()
            filtro = df_pecas[df_pecas[nome_coluna].str.lower() == critério]

    except ValueError:
        print("Erro no valor introduzido.")
        return

    if filtro is None:
        print("Erro inesperado: filtro não definido.")
        return

    print(f"\nResultados encontrados para '{critério}' na coluna '{nome_coluna}':")
    if filtro.empty:
        print(" Nenhum resultado encontrado.")
    else:
        print(filtro)
    print()


def grafico_preco_final():
    global df_pecas

    if df_pecas.empty:
        print("O DataFrame está vazio, nada para mostrar.")
        return

    coluna = "Preço Final (€)"
    if coluna not in df_pecas.columns:
        print(f"A coluna '{coluna}' não existe no DataFrame.")
        return

    df_pecas[coluna].plot(kind="bar", figsize=(10, 6), color="skyblue")
    plt.title("Preço Final das Peças")
    plt.xlabel("Índice da Peça")
    plt.ylabel("Preço Final (€)")
    plt.grid(axis="y")
    plt.show()


while True:
    print("Bem-Vindo(a)")
    print("1 - Inserir Peça")
    print("2 - Consultar Peças ")
    print("3 - Editar valor ")
    print("4 - Editar valores pre definidos")
    print("5 - Exportar Excel")
    print("6 - Importar Excel")
    print("7 - Filtro")
    print("8 - Grafico preço final")
    print("9 - Sair do Programa ")

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
        exportar_excel()
    elif escolha == "6":
        importar_excel()
    elif escolha == "7":
        filtro_dataframe()
    elif escolha == "8":
        grafico_preco_final()
    elif escolha == "9":
        print("Obrigado!")
        break
    else:
        print("Erro Opção Inválida! ")
