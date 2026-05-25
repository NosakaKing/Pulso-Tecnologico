"""
src/survey_utils.py — Funciones reutilizables para el cruce Survey ↔ Stack Overflow.

Contiene:
- Cálculo vectorizado de Brecha de Demanda (Demand Gap).
- Correlación de Pearson implementada con la API nativa de Polars.
- Normalización de tags para compatibilizar esquemas.
"""
import polars as pl
import math


def calcular_demand_gap(
    lf: pl.LazyFrame,
    wanted_col: str = "wanted_pct",
    used_col: str = "used_pct",
    output_col: str = "Demand_Gap",
) -> pl.LazyFrame:
    """
    Calcula la Brecha de Demanda de forma vectorizada sobre un LazyFrame.

    Demand_Gap = wanted_pct - used_pct

    Una brecha positiva indica que más desarrolladores *desean* aprender
    la tecnología frente a los que actualmente la *usan*, lo cual señala
    alta tracción en el mercado laboral.

    Args:
        lf: LazyFrame con columnas de porcentaje de uso y deseo.
        wanted_col: Nombre de la columna de porcentaje deseado.
        used_col: Nombre de la columna de porcentaje en uso.
        output_col: Nombre de la columna resultado.

    Returns:
        LazyFrame con la nueva columna de Demand Gap añadida.
    """
    return lf.with_columns(
        (pl.col(wanted_col) - pl.col(used_col)).alias(output_col)
    )


def pearson_correlation(
    df: pl.DataFrame,
    col_x: str,
    col_y: str,
) -> float:
    """
    Calcula la correlación de Pearson entre dos columnas numéricas
    usando exclusivamente la API nativa de Polars (sin NumPy/SciPy).

    Fórmula:
        r = Σ[(xi - x̄)(yi - ȳ)] / √[Σ(xi - x̄)² · Σ(yi - ȳ)²]

    Args:
        df: DataFrame de Polars con las dos columnas.
        col_x: Nombre de la primera variable.
        col_y: Nombre de la segunda variable.

    Returns:
        Coeficiente de correlación de Pearson (float entre -1 y 1).
        Retorna 0.0 si alguna de las varianzas es cero.
    """
    stats = df.select(
        ((pl.col(col_x) - pl.col(col_x).mean()) * (pl.col(col_y) - pl.col(col_y).mean()))
        .sum()
        .alias("cov_xy"),
        ((pl.col(col_x) - pl.col(col_x).mean()) ** 2)
        .sum()
        .alias("var_x"),
        ((pl.col(col_y) - pl.col(col_y).mean()) ** 2)
        .sum()
        .alias("var_y"),
    )

    cov_xy = stats["cov_xy"][0]
    var_x = stats["var_x"][0]
    var_y = stats["var_y"][0]

    denominator = math.sqrt(var_x * var_y)
    if denominator == 0:
        return 0.0

    return cov_xy / denominator


def normalizar_tag_survey(tag_col: str = "tag") -> pl.Expr:
    """
    Normaliza los nombres de tags del Survey de Stack Overflow para
    hacerlos compatibles con los tags del dataset de preguntas de SO.

    Mapeos principales:
    - 'html/css' → 'html'   (en el dataset SO, html y css son tags separados)
    - 'bash/shell (all shells)' → 'bash'
    - 'visual basic (.net)' → 'vb.net'

    Además aplica .str.to_lowercase() y .str.strip_chars() como
    limpieza general.

    Args:
        tag_col: Nombre de la columna a normalizar.

    Returns:
        Expresión de Polars con el tag normalizado.
    """
    return (
        pl.col(tag_col)
        .str.to_lowercase()
        .str.strip_chars()
        .str.replace("html/css", "html")
        .str.replace(r"bash/shell \(all shells\)", "bash")
        .str.replace(r"visual basic \(\.net\)", "vb.net")
        .alias(tag_col)
    )
