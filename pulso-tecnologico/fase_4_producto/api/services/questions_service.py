# fase_4_producto/api/services/questions_service.py
import polars as pl
from data.loader import get_top_questions

def obtener_top_questions(tag: str) -> dict | None:
    df = get_top_questions()

    df_tag = df.filter(
        pl.col("Tag").str.to_lowercase() == tag.lower()
    )

    # Si el tag no existe devolvemos None para manejarlo en el router
    if df_tag.is_empty():
        return None

    registros = (
        df_tag
        .sort("Score", descending=True)
        .select([
            pl.col("Id").alias("id"),
            pl.col("Score").alias("score"),
            pl.col("ViewCount").alias("view_count"),
            pl.col("AnswerCount").alias("answer_count"),
            pl.col("url"),
        ])
        .to_dicts()
    )

    return {
        "tag": tag.lower(),
        "total": len(registros),
        "data": registros,
    }