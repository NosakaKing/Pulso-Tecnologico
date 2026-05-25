# pyrefly: ignore [missing-import]
import polars as pl

def clasificar_tendencia(crecimiento_pct: str = "Crecimiento_Pct", new_col: str = "Categoria_Tendencia") -> pl.Expr:
    """
    Clasifica el estado de una tecnología según su crecimiento porcentual anual.
    
    Reglas:
    - En Auge: Crecimiento >= 20%
    - Madurando: Crecimiento entre -5% y 20% (sin incluir 20%)
    - En Declive: Crecimiento < -5%
    
    Args:
        crecimiento_pct (str): Nombre de la columna con el crecimiento porcentual.
        new_col (str): Nombre de la columna resultante con la clasificación.
        
    Returns:
        pl.Expr: Expresión de Polars para crear la nueva columna categorizada.
    """
    return pl.when(pl.col(crecimiento_pct) >= 20).then(pl.lit("En Auge")) \
             .when(pl.col(crecimiento_pct) < -10).then(pl.lit("En Declive")) \
             .otherwise(pl.lit("Madurando")).alias(new_col)
