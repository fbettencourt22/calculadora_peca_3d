import io
from flask import Flask, render_template, request, redirect, send_file, url_for, flash
import pandas as pd

app = Flask(__name__)
app.secret_key = "minha_chave_secreta"


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

VALOR_KWH = 0.158
CONSUMO_W = 140
CUSTO_MAO_OBRA = 20


def recalcular_pecas():
    global df_pecas
    for index, row in df_pecas.iterrows():
        try:
            preco_filamento_kg = float(row["Filamento (€/kg)"])
            quantidade_filamento_g = float(row["Filamento (g)"])
            tempo_horas = float(row["Tempo (h)"])
            tempo_mao_obra_min = float(row["Mão de Obra (min)"])
            margem = float(row["Margem (%)"])

            custo_filamento = (
                (preco_filamento_kg / 1000) * quantidade_filamento_g
            ) * 1.10
            consumo_kwh = (CONSUMO_W * tempo_horas) / 1000
            custo_energia = consumo_kwh * VALOR_KWH
            custo_mao_obra = (tempo_mao_obra_min / 60) * CUSTO_MAO_OBRA
            custo_total = (
                custo_filamento + custo_energia + custo_mao_obra + (0.15 * tempo_horas)
            )
            preco_final = custo_total / (1 - (margem / 100))

            df_pecas.at[index, "Custo Filamento (€)"] = round(custo_filamento, 2)
            df_pecas.at[index, "Custo Energia (€)"] = round(custo_energia, 2)
            df_pecas.at[index, "Custo Mão de Obra (€)"] = round(custo_mao_obra, 2)
            df_pecas.at[index, "Custo Total (€)"] = round(custo_total, 2)
            df_pecas.at[index, "Preço Final (€)"] = round(preco_final, 2)
            df_pecas.at[index, "Energia (€/kWh)"] = VALOR_KWH
            df_pecas.at[index, "Consumo (W)"] = CONSUMO_W
        except Exception as e:
            print(f"Erro no cálculo da peça {index}: {e}")


@app.route("/")
def listar():
    global df_pecas
    return render_template("listar.html", pecas=df_pecas)


@app.route("/inserir", methods=["GET", "POST"])
def inserir():
    global df_pecas
    if request.method == "POST":
        try:
            nome = request.form["nome"]
            material = request.form["material"]
            preco_filamento_kg = float(
                request.form["preco_filamento_kg"].replace(",", ".")
            )
            quantidade_filamento_g = float(request.form["quantidade_filamento_g"])
            tempo_horas = float(request.form["tempo_horas"].replace(",", "."))
            tempo_mao_obra_min = float(
                request.form["tempo_mao_obra_min"].replace(",", ".")
            )
            margem = float(request.form["margem"].replace(",", "."))

            custo_filamento = (
                (preco_filamento_kg / 1000) * quantidade_filamento_g
            ) * 1.10
            consumo_kwh = (CONSUMO_W * tempo_horas) / 1000
            custo_energia = consumo_kwh * VALOR_KWH
            custo_mao_obra = (tempo_mao_obra_min / 60) * CUSTO_MAO_OBRA
            custo_total = (
                custo_filamento + custo_energia + custo_mao_obra + (0.15 * tempo_horas)
            )
            preco_final = custo_total / (1 - (margem / 100))

            nova_peca = {
                "Peça": nome,
                "Material": material,
                "Filamento (g)": quantidade_filamento_g,
                "Filamento (€/kg)": preco_filamento_kg,
                "Custo Filamento (€)": round(custo_filamento, 2),
                "Tempo (h)": tempo_horas,
                "Energia (€/kWh)": VALOR_KWH,
                "Consumo (W)": CONSUMO_W,
                "Custo Energia (€)": round(custo_energia, 2),
                "Mão de Obra (min)": tempo_mao_obra_min,
                "Custo Mão de Obra (€)": round(custo_mao_obra, 2),
                "Margem (%)": margem,
                "Custo Total (€)": round(custo_total, 2),
                "Preço Final (€)": round(preco_final, 2),
            }

            df_pecas = pd.concat(
                [df_pecas, pd.DataFrame([nova_peca])], ignore_index=True
            )

            flash(f"Peça '{nome}' adicionada com sucesso!", "success")
            return redirect(url_for("listar"))
        except Exception as e:
            flash(f"Erro ao inserir peça: {e}", "danger")
            return redirect(url_for("inserir"))
    else:
        return render_template("inserir.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    global df_pecas
    if id < 0 or id >= len(df_pecas):
        flash("Peça não encontrada.", "danger")
        return redirect(url_for("listar"))

    if request.method == "POST":
        try:
            nome = request.form["nome"]
            material = request.form["material"]
            preco_filamento_kg = float(
                request.form["preco_filamento_kg"].replace(",", ".")
            )
            quantidade_filamento_g = float(request.form["quantidade_filamento_g"])
            tempo_horas = float(request.form["tempo_horas"].replace(",", "."))
            tempo_mao_obra_min = float(
                request.form["tempo_mao_obra_min"].replace(",", ".")
            )
            margem = float(request.form["margem"].replace(",", "."))

            df_pecas.at[id, "Peça"] = nome
            df_pecas.at[id, "Material"] = material
            df_pecas.at[id, "Filamento (g)"] = quantidade_filamento_g
            df_pecas.at[id, "Filamento (€/kg)"] = preco_filamento_kg
            df_pecas.at[id, "Tempo (h)"] = tempo_horas
            df_pecas.at[id, "Mão de Obra (min)"] = tempo_mao_obra_min
            df_pecas.at[id, "Margem (%)"] = margem

            # Recalcular custos
            recalcular_pecas()

            flash(f"Peça '{nome}' atualizada com sucesso!", "success")
            return redirect(url_for("listar"))
        except Exception as e:
            flash(f"Erro ao editar peça: {e}", "danger")
            return redirect(url_for("editar", id=id))
    else:
        peca = df_pecas.iloc[id].to_dict()
        return render_template("editar.html", peca=peca, id=id)


@app.route("/apagar/<int:id>")
def apagar(id):
    global df_pecas
    if id < 0 or id >= len(df_pecas):
        flash("Peça não encontrada.", "danger")
    else:
        df_pecas = df_pecas.drop(df_pecas.index[id]).reset_index(drop=True)
        flash("Peça removida com sucesso.", "success")
    return redirect(url_for("listar"))


@app.route("/exportar", methods=["GET", "POST"])
def exportar():
    global df_pecas
    if request.method == "POST":
        try:
            linhas_selecionadas = request.form.getlist("linhas")
            if not linhas_selecionadas:
                return "Nenhuma linha selecionada para exportar.", 400

            df_selecionadas = df_pecas.loc[
                df_pecas.index.isin(map(int, linhas_selecionadas))
            ]

            nome_base = request.form.get("filename", "exportacao").strip()
            if not nome_base:
                nome_base = "exportacao"
            nome_ficheiro = f"{nome_base}.xlsx"

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df_selecionadas.to_excel(writer, index=False, sheet_name="Peças")
            output.seek(0)

            return send_file(
                output,
                download_name=nome_ficheiro,
                as_attachment=True,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        except Exception as e:
            return f"Erro ao exportar: {e}"
    else:

        return render_template("exportar.html", pecas=df_pecas)


@app.route("/importar", methods=["GET", "POST"])
def importar():
    global df_pecas
    if request.method == "POST":
        try:
            arquivo = request.files.get("file")
            if not arquivo:
                return "Nenhum arquivo enviado.", 400

            df_novo = pd.read_excel(arquivo)

            if df_pecas is None or df_pecas.empty:
                df_pecas = df_novo
            else:

                df_pecas = pd.concat([df_pecas, df_novo], ignore_index=True)

            flash("Importação realizada com sucesso!", "success")
            return redirect(url_for("listar"))
        except Exception as e:
            flash(f"Erro ao importar ficheiro: {e}", "danger")
            return redirect(url_for("importar"))
    else:
        return render_template("importar.html")


if __name__ == "__main__":
    app.run(debug=True)
