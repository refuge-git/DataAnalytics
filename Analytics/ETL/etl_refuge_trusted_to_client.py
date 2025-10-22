# # -*- coding: utf-8 -*-
# """
# Combina Atendimentos.csv + condicao_saude_tratado.csv por beneficiário
# Leitura:  Analytics/s3-refuge-analysis-trusted/base-refuge/
# Saída:    Analytics/s3-refuge-analysis-client/base-refuge/beneficiarios_atendimento_saude.csv
# """

# import os
# import glob
# import unicodedata
# import pandas as pd

# # ---------------- paths ----------------
# def data_analytics_root(script_dir: str) -> str:
#     if "DataAnalytics" in script_dir:
#         base = script_dir.split("DataAnalytics")[0]
#         return os.path.join(base, "DataAnalytics")
#     cur = script_dir
#     while True:
#         cand = os.path.join(cur, "DataAnalytics")
#         if os.path.isdir(cand):
#             return cand
#         parent = os.path.dirname(cur)
#         if parent == cur:
#             return script_dir
#         cur = parent

# HERE = os.path.dirname(os.path.abspath(__file__))
# DA_ROOT = data_analytics_root(HERE)
# ANALYTICS = os.path.join(DA_ROOT, "Analytics")

# TRUSTED_DIR = os.path.join(ANALYTICS, "s3-refuge-analysis-trusted", "base-refuge")
# CLIENT_DIR  = os.path.join(ANALYTICS, "s3-refuge-analysis-client",  "base-refuge")
# os.makedirs(CLIENT_DIR, exist_ok=True)

# ATEND_FILE = "Atendimentos.csv"
# SAUDE_FILE = "condicao_saude_tratado.csv"
# OUT_FILE   = os.path.join(CLIENT_DIR, "beneficiarios_atendimento_saude.csv")

# # ---------------- helpers ----------------
# def norm_str(s: str) -> str:
#     s = unicodedata.normalize("NFKD", s)
#     s = "".join(c for c in s if not unicodedata.combining(c))
#     return s.strip().lower()

# def load_from_trusted(filename: str) -> pd.DataFrame:
#     path = os.path.join(TRUSTED_DIR, filename)
#     if os.path.exists(path):
#         df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
#         df.columns = [norm_str(c) for c in df.columns]
#         df = df.dropna(axis=1, how="all")
#         print(f"✓ Carregado: {path}  ({len(df):,} linhas)")
#         return df

#     hits = glob.glob(os.path.join(TRUSTED_DIR, "**", filename), recursive=True)
#     if hits:
#         path = hits[0]
#         df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
#         df.columns = [norm_str(c) for c in df.columns]
#         print(f"✓ Carregado (busca recursiva): {path}  ({len(df):,} linhas)")
#         return df

#     raise FileNotFoundError(f"Arquivo não encontrado em TRUSTED: {filename}")

# def find_beneficiary_key(cols) -> str | None:
#     candidates = [
#         "id_beneficiario", "fk_beneficiario", "fkbeneficiario",
#         "beneficiario_id", "idbeneficiario"
#     ]
#     for k in candidates:
#         if k in cols:
#             return k
#     for c in cols:
#         if ("benef" in c and "id" in c) or c.startswith("fkbenef"):
#             return c
#     return None

# # ---------------- main ----------------
# def main():
#     att   = load_from_trusted(ATEND_FILE)
#     saude = load_from_trusted(SAUDE_FILE)

#     att_key = find_beneficiary_key(att.columns)
#     sd_key  = find_beneficiary_key(saude.columns)
#     if att_key is None or sd_key is None:
#         raise KeyError("Coluna de beneficiário não encontrada.")

#     att = att.rename(columns={att_key: "id_beneficiario"}).copy()
#     saude = saude.rename(columns={sd_key: "id_beneficiario"}).copy()

#     att["id_beneficiario"] = att["id_beneficiario"].astype(str).str.strip().str.replace('"', "", regex=False)
#     saude["id_beneficiario"] = saude["id_beneficiario"].astype(str).str.strip().str.replace('"', "", regex=False)

#     # Prefixos
#     att_pref = att.add_prefix("att_").rename(columns={"att_id_beneficiario": "id_beneficiario"})
#     saude_pref = saude.add_prefix("saude_").rename(columns={"saude_id_beneficiario": "id_beneficiario"})

#     # ✅ Mapeia valores da coluna ATENDIMENTO
#     if "att_atendimento" in att_pref.columns:
#         def map_atendimento(val):
#             if pd.isna(val):
#                 return pd.NA
#             val = str(val).strip()
#             return {
#                 "1": "Refeicao",
#                 "2": "Banho"
#             }.get(val, "Outros")

#         att_pref["att_atendimento"] = att_pref["att_atendimento"].apply(map_atendimento)

#     # Deduplicar saúde por beneficiário
#     saude_dedup = saude_pref.drop_duplicates(subset=["id_beneficiario"])

#     # LEFT JOIN
#     merged = pd.merge(att_pref, saude_dedup, on="id_beneficiario", how="left", sort=True)

#     # Substituir campos vazios por null
#     merged = merged.replace(r"^\s*$", pd.NA, regex=True)

#     # Adicionar coluna de categoria com base em fkcategoria
#     cat_col = next((c for c in merged.columns if "fkcategoria" in c.lower()), None)
#     if cat_col:
#         merged["categoria"] = merged[cat_col].map({
#             "1": "deficiencia",
#             "2": "doenca",
#             "3": "transtorno"
#         }).fillna(pd.NA)
#     else:
#         print("⚠️ Coluna 'fkcategoria' não encontrada. A coluna 'categoria' não será criada.")

#     # Garantir que dados de saúde e categoria apareçam só na primeira linha por beneficiário
#     saude_cols = [c for c in merged.columns if c.startswith("saude_") or c == "categoria"]
#     merged[saude_cols] = merged.groupby("id_beneficiario")[saude_cols].transform(
#         lambda x: x.where(x.index == x.first_valid_index())
#     )

#     # Ordenar
#     sort_cols = [c for c in ("id_beneficiario", "att_data", "att_hora") if c in merged.columns]
#     if sort_cols:
#         merged = merged.sort_values(by=sort_cols, kind="stable")

#     # Salvar
#     merged.to_csv(OUT_FILE, index=False, sep=";", encoding="utf-8-sig", na_rep="null")
#     print(f"\n✅ Arquivo final salvo em:\n{OUT_FILE}\nLinhas: {len(merged):,}")

# if __name__ == "__main__":
#     main()

# -*- coding: utf-8 -*-
"""
Combina Atendimentos.csv + condicao_saude_tratado.csv + Local_status_transformado.csv por beneficiário
Leitura:  Analytics/s3-refuge-analysis-trusted/base-refuge/
Saída:    Analytics/s3-refuge-analysis-client/base-refuge/beneficiarios_atendimento_saude.csv
"""

import os
import glob
import unicodedata
import pandas as pd

# ---------------- paths ----------------
def data_analytics_root(script_dir: str) -> str:
    if "DataAnalytics" in script_dir:
        base = script_dir.split("DataAnalytics")[0]
        return os.path.join(base, "DataAnalytics")
    cur = script_dir
    while True:
        cand = os.path.join(cur, "DataAnalytics")
        if os.path.isdir(cand):
            return cand
        parent = os.path.dirname(cur)
        if parent == cur:
            return script_dir
        cur = parent

HERE = os.path.dirname(os.path.abspath(__file__))
DA_ROOT = data_analytics_root(HERE)
ANALYTICS = os.path.join(DA_ROOT, "Analytics")

TRUSTED_DIR = os.path.join(ANALYTICS, "s3-refuge-analysis-trusted", "base-refuge")
CLIENT_DIR  = os.path.join(ANALYTICS, "s3-refuge-analysis-client",  "base-refuge")
os.makedirs(CLIENT_DIR, exist_ok=True)

ATEND_FILE = "Atendimentos.csv"
SAUDE_FILE = "condicao_saude_tratado.csv"
LOCAL_FILE = "Local_status_transformado.csv"
OUT_FILE   = os.path.join(CLIENT_DIR, "beneficiarios_atendimento_saude.csv")

# ---------------- helpers ----------------
def norm_str(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip().lower()

def load_from_trusted(filename: str) -> pd.DataFrame:
    path = os.path.join(TRUSTED_DIR, filename)
    if os.path.exists(path):
        df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
        df.columns = [norm_str(c) for c in df.columns]
        df = df.dropna(axis=1, how="all")
        print(f"✓ Carregado: {path}  ({len(df):,} linhas)")
        return df

    hits = glob.glob(os.path.join(TRUSTED_DIR, "**", filename), recursive=True)
    if hits:
        path = hits[0]
        df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
        df.columns = [norm_str(c) for c in df.columns]
        print(f"✓ Carregado (busca recursiva): {path}  ({len(df):,} linhas)")
        return df

    raise FileNotFoundError(f"Arquivo não encontrado em TRUSTED: {filename}")

def find_beneficiary_key(cols) -> str | None:
    candidates = [
        "id_beneficiario", "fk_beneficiario", "fkbeneficiario",
        "beneficiario_id", "idbeneficiario"
    ]
    for k in candidates:
        if k in cols:
            return k
    for c in cols:
        if ("benef" in c and "id" in c) or c.startswith("fkbenef"):
            return c
    return None

# ---------------- main ----------------
def main():
    att   = load_from_trusted(ATEND_FILE)
    saude = load_from_trusted(SAUDE_FILE)
    local = load_from_trusted(LOCAL_FILE)

    att_key = find_beneficiary_key(att.columns)
    sd_key  = find_beneficiary_key(saude.columns)
    lc_key  = find_beneficiary_key(local.columns)
    if att_key is None or sd_key is None or lc_key is None:
        raise KeyError("Coluna de beneficiário não encontrada em um dos arquivos.")

    att = att.rename(columns={att_key: "id_beneficiario"}).copy()
    saude = saude.rename(columns={sd_key: "id_beneficiario"}).copy()
    local = local.rename(columns={lc_key: "id_beneficiario"}).copy()

    for df in [att, saude, local]:
        df["id_beneficiario"] = df["id_beneficiario"].astype(str).str.strip().str.replace('"', "", regex=False)

    # Prefixos
    att_pref = att.add_prefix("att_").rename(columns={"att_id_beneficiario": "id_beneficiario"})
    saude_pref = saude.add_prefix("saude_").rename(columns={"saude_id_beneficiario": "id_beneficiario"})
    local_pref = local.add_prefix("local_").rename(columns={"local_id_beneficiario": "id_beneficiario"})

    # ✅ Mapeia valores da coluna ATENDIMENTO
    if "att_atendimento" in att_pref.columns:
        def map_atendimento(val):
            if pd.isna(val):
                return pd.NA
            val = str(val).strip()
            return {
                "1": "Refeicao",
                "2": "Banho"
            }.get(val, "Outros")

        att_pref["att_atendimento"] = att_pref["att_atendimento"].apply(map_atendimento)

    # Deduplicar saúde por beneficiário
    saude_dedup = saude_pref.drop_duplicates(subset=["id_beneficiario"])

    # LEFT JOIN atendimentos + saúde
    merged = pd.merge(att_pref, saude_dedup, on="id_beneficiario", how="left", sort=True)

    # LEFT JOIN com local
    merged = pd.merge(merged, local_pref, on="id_beneficiario", how="left")

    # Substituir campos vazios por null
    merged = merged.replace(r"^\s*$", pd.NA, regex=True)

    # Adicionar coluna de categoria com base em fkcategoria
    cat_col = next((c for c in merged.columns if "fkcategoria" in c.lower()), None)
    if cat_col:
        merged["categoria"] = merged[cat_col].map({
            "1": "deficiencia",
            "2": "doenca",
            "3": "transtorno"
        }).fillna(pd.NA)
    else:
        print("⚠️ Coluna 'fkcategoria' não encontrada. A coluna 'categoria' não será criada.")

    # Garantir que dados de saúde e categoria apareçam só na primeira linha por beneficiário
    saude_cols = [c for c in merged.columns if c.startswith("saude_") or c == "categoria"]
    merged[saude_cols] = merged.groupby("id_beneficiario")[saude_cols].transform(
        lambda x: x.where(x.index == x.first_valid_index())
    )

    # Ordenar
    sort_cols = [c for c in ("id_beneficiario", "att_data", "att_hora") if c in merged.columns]
    if sort_cols:
        merged = merged.sort_values(by=sort_cols, kind="stable")

    # Salvar
    merged.to_csv(OUT_FILE, index=False, sep=";", encoding="utf-8-sig", na_rep="null")
    print(f"\n✅ Arquivo final salvo em:\n{OUT_FILE}\nLinhas: {len(merged):,}")

if __name__ == "__main__":
    main()
