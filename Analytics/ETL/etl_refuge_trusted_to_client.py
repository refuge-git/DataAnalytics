# -*- coding: utf-8 -*-
"""
Combina Atendimentos.csv + condicao_saude_tratado.csv por beneficiário
Leitura:  Analytics/s3-refuge-analysis-trusted/base-refuge/
Saída:    Analytics/s3-refuge-analysis-client/base-refuge/beneficiarios_atendimento_saude.csv
Junção:   FULL OUTER (mantém quem aparece em qualquer um dos dois)
"""

import os
import glob
import unicodedata
import pandas as pd


# ---------------- paths ----------------
def data_analytics_root(script_dir: str) -> str:
    """Retorna o caminho até .../DataAnalytics a partir do diretório do script."""
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
OUT_FILE   = os.path.join(CLIENT_DIR, "beneficiarios_atendimento_saude.csv")


# ---------------- helpers ----------------
def norm_str(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.strip().lower()


def load_from_trusted(filename: str) -> pd.DataFrame:
    """Carrega arquivo da pasta TRUSTED (sep=';'). Se não achar, tenta busca recursiva dentro de TRUSTED."""
    path = os.path.join(TRUSTED_DIR, filename)
    if os.path.exists(path):
        df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
        df.columns = [norm_str(c) for c in df.columns]
        # remove colunas totalmente vazias
        empty_cols = [c for c in df.columns if df[c].isna().all()]
        if empty_cols:
            df = df.drop(columns=empty_cols)
        print(f"✓ Carregado: {path}  ({len(df):,} linhas)")
        return df

    # fallback: busca recursiva apenas em TRUSTED
    hits = glob.glob(os.path.join(TRUSTED_DIR, "**", filename), recursive=True)
    if hits:
        path = hits[0]
        df = pd.read_csv(path, sep=";", dtype=str, encoding="utf-8-sig")
        df.columns = [norm_str(c) for c in df.columns]
        print(f"✓ Carregado (busca recursiva): {path}  ({len(df):,} linhas)")
        return df

    raise FileNotFoundError(f"Arquivo não encontrado em TRUSTED: {filename}\n"
                            f"Tentado em:\n - {os.path.join(TRUSTED_DIR, filename)}")


def find_beneficiary_key(cols) -> str | None:
    """Localiza a coluna de beneficiário por nomes comuns/variações."""
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
    # 1) leitura (TRUSTED)
    att   = load_from_trusted(ATEND_FILE)
    saude = load_from_trusted(SAUDE_FILE)

    # 2) chaves
    att_key = find_beneficiary_key(att.columns)
    sd_key  = find_beneficiary_key(saude.columns)
    if att_key is None:
        raise KeyError(f"Não encontrei coluna de beneficiário em Atendimentos. Colunas: {list(att.columns)}")
    if sd_key is None:
        raise KeyError(f"Não encontrei coluna de beneficiário em Condição de Saúde. Colunas: {list(saude.columns)}")

    # 3) padronizar chave/id
    att   = att.rename(columns={att_key: "id_beneficiario"}).copy()
    saude = saude.rename(columns={sd_key: "id_beneficiario"}).copy()

    att["id_beneficiario"]   = att["id_beneficiario"].astype(str).str.strip().str.replace('"', "", regex=False)
    saude["id_beneficiario"] = saude["id_beneficiario"].astype(str).str.strip().str.replace('"', "", regex=False)

    # 4) prefixos p/ evitar colisão
    att_pref = att.add_prefix("att_").rename(columns={"att_id_beneficiario": "id_beneficiario"})
    sd_pref  = saude.add_prefix("saude_").rename(columns={"saude_id_beneficiario": "id_beneficiario"})

    # 5) FULL OUTER JOIN
    merged = pd.merge(att_pref, sd_pref, on="id_beneficiario", how="outer", sort=True)

    # 6) ordenar (melhor esforço) se colunas existirem
    for c in ("att_data", "att_hora", "saude_data", "saude_hora"):
        if c in merged.columns:
            merged[c] = merged[c].astype(str)
    sort_cols = [c for c in ("id_beneficiario", "att_data", "att_hora", "saude_data", "saude_hora") if c in merged.columns]
    if sort_cols:
        merged = merged.sort_values(by=sort_cols, kind="stable")

    # 7) salvar no CLIENT
    merged.to_csv(OUT_FILE, index=False, sep=";", encoding="utf-8-sig")
    print(f"\n✅ Arquivo final salvo no CLIENT:\n{OUT_FILE}\nLinhas: {len(merged):,}")


if __name__ == "__main__":
    main()
