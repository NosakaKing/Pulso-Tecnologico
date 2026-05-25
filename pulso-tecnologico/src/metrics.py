import polars as pl
import numpy as np

def calculate_relative_percentage(df: pl.DataFrame, count_col: str, total_count: int, percentage_col_name: str = "Porcentaje") -> pl.DataFrame:
    """
    Calcula el porcentaje relativo de una columna de conteo frente a un total absoluto.
    
    Args:
        df (pl.DataFrame): DataFrame de Polars con los datos.
        count_col (str): Nombre de la columna con el conteo absoluto.
        total_count (int): Conteo total absoluto a utilizar como denominador.
        percentage_col_name (str): Nombre de la nueva columna de porcentaje.
        
    Returns:
        pl.DataFrame: DataFrame con la nueva columna de porcentaje.
    """
    return df.with_columns(
        ((pl.col(count_col) / total_count) * 100).alias(percentage_col_name)
    )

def categorize_technology(tag_col: str = "Tag", new_col: str = "Categoria") -> pl.Expr:
    """
    Genera una expresión de Polars para categorizar tecnologías (tags) 
    en Lenguajes, Frameworks, Bases de Datos, y Otros.
    
    Args:
        tag_col (str): Nombre de la columna de tags.
        new_col (str): Nombre de la columna de categorías a crear.
        
    Returns:
        pl.Expr: Expresión de Polars con la lógica condicional de categorización.
    """
    lenguajes = [
        'javascript', 'python', 'java', 'c#', 'php', 'c++', 'c', 'typescript', 
        'ruby', 'swift', 'go', 'kotlin', 'rust', 'objective-c', 'scala', 'dart',
        'r', 'vba', 'matlab', 'perl', 'haskell', 'lua'
    ]
    frameworks = [
        'reactjs', 'angular', 'angularjs', 'vue.js', 'django', 'flask', 
        'spring', 'spring-boot', 'ruby-on-rails', 'asp.net', 'asp.net-mvc', 
        'asp.net-core', 'laravel', 'express', 'node.js', 'react-native', 
        'flutter', 'pandas', 'jquery', 'bootstrap'
    ]
    bases_de_datos = [
        'sql', 'mysql', 'postgresql', 'sql-server', 'mongodb', 'oracle', 
        'redis', 'sqlite', 'elasticsearch', 'firebase', 'cassandra', 'mariadb'
    ]
    
    return pl.when(pl.col(tag_col).is_in(lenguajes)).then(pl.lit("Lenguaje")) \
             .when(pl.col(tag_col).is_in(frameworks)).then(pl.lit("Framework")) \
             .when(pl.col(tag_col).is_in(bases_de_datos)).then(pl.lit("Base de Datos")) \
             .otherwise(pl.lit("Otros")).alias(new_col)


    
def crecimiento_anual(df: pl.DataFrame, count_col: str = 'Count', tag_col: str = 'Tag', year_col: str = 'Year') -> pl.DataFrame:
    # 1. Agrupar el volumen absoluto anualmente por Tag
    df_yearly = df.group_by([tag_col, year_col]).agg(
        pl.col(count_col).sum().alias('Total_Tag')
    )
    
    # 2. Calcular el tamaño total del "pastel" por año (sumando todos los tags)
    totales_por_ano = df_yearly.group_by(year_col).agg(
        pl.col('Total_Tag').sum().alias('Total_Global_Ano')
    )
    
    # 3. Unir para sacar el Porcentaje Relativo (Market Share)
    df_yearly = df_yearly.join(totales_por_ano, on=year_col)
    df_yearly = df_yearly.with_columns(
        ((pl.col('Total_Tag') / pl.col('Total_Global_Ano')) * 100).alias('Pct_Relativo')
    )
    
    # 4. Extraer la cuota de mercado de 2022 y 2023
    df_2022 = df_yearly.filter(pl.col(year_col) == 2022).select([tag_col, pl.col('Pct_Relativo').alias('Share_2022')])
    df_2023 = df_yearly.filter(pl.col(year_col) == 2023).select([tag_col, pl.col('Pct_Relativo').alias('Share_2023')])
    
    # 5. Unir y calcular el crecimiento del Market Share
    df_crecimiento = df_2022.join(df_2023, on=tag_col, how='full', coalesce=True).fill_null(0)
    
    df_crecimiento = df_crecimiento.with_columns(
        pl.when(pl.col('Share_2022') > 0)
        .then(((pl.col('Share_2023').cast(pl.Float64) - pl.col('Share_2022').cast(pl.Float64)) / pl.col('Share_2022').cast(pl.Float64)) * 100.0)
        .otherwise(0.0)
        .alias('Crecimiento_Pct')
    )
    
    return df_crecimiento.select([tag_col, 'Share_2022', 'Share_2023', 'Crecimiento_Pct'])

def tendencia_lineal(df: pl.DataFrame, time_col: str = "Mes_Indice", count_col: str = "Count", tag_col: str = "Tag") -> pl.DataFrame:
    """
    Aplica una regresión lineal sobre una serie temporal para calcular la pendiente (beta_1) y el R-cuadrado.
    
    Args:
        df (pl.DataFrame): DataFrame con la serie temporal mensual ordenada.
        time_col (str): Nombre de la columna numérica secuencial del tiempo (ej. índice de mes 1, 2, 3...).
        count_col (str): Nombre de la columna del volumen.
        tag_col (str): Nombre de la columna de la tecnología.
        
    Returns:
        pl.DataFrame: DataFrame con 'Tag', 'Pendiente' y 'R2'.
    """
    tags = df[tag_col].unique().to_list()
    resultados = []
    
    for tag in tags:
        df_tag = df.filter(pl.col(tag_col) == tag).sort(time_col)
        x = df_tag[time_col].to_numpy()
        y = df_tag[count_col].to_numpy()
        
        if len(x) > 1:
            # np.polyfit grado 1
            coefs = np.polyfit(x, y, deg=1)
            pendiente = coefs[0]
            
            # Calcular R-cuadrado
            p = np.poly1d(coefs)
            yhat = p(x)
            ybar = np.sum(y) / len(y)
            ssreg = np.sum((yhat - ybar)**2)
            sstot = np.sum((y - ybar)**2)
            
            r2 = ssreg / sstot if sstot != 0 else 0.0
        else:
            pendiente = 0.0
            r2 = 0.0
            
        resultados.append({tag_col: tag, "Pendiente": pendiente, "R2": r2})
        
    return pl.DataFrame(resultados)


def tasa_resolucion(df: pl.DataFrame, tag_col: str = 'Tag', answer_col: str = 'AnswerCount',
                    closed_col: str = 'es_cerrada') -> pl.DataFrame:
    """
    Calcula la tasa de resolución (% preguntas con respuesta) y la tasa de cierre
    por cada tecnología.
    
    Args:
        df (pl.DataFrame): DataFrame con columnas de tag, respuestas y cierre.
        tag_col (str): Nombre de la columna de tecnología.
        answer_col (str): Nombre de la columna de conteo de respuestas.
        closed_col (str): Nombre de la columna booleana de cierre.
        
    Returns:
        pl.DataFrame: DataFrame con tasas de resolución y cierre por tag.
    """
    return (
        df.group_by(tag_col).agg([
            pl.len().alias('Total_Preguntas'),
            (pl.col(answer_col).fill_null(0) >= 1).sum().alias('Con_Respuesta'),
            pl.col(closed_col).sum().alias('Cerradas'),
        ])
        .with_columns([
            ((pl.col('Con_Respuesta') / pl.col('Total_Preguntas')) * 100)
                .round(2).alias('Tasa_Respuesta_Pct'),
            ((pl.col('Cerradas') / pl.col('Total_Preguntas')) * 100)
                .round(2).alias('Tasa_Cierre_Pct'),
        ])
        .sort('Tasa_Respuesta_Pct', descending=True)
    )


def top_n_por_grupo(df: pl.DataFrame, n: int = 5, tag_col: str = 'Tag',
                    score_col: str = 'Score') -> pl.DataFrame:
    """
    Extrae las N filas con mayor score dentro de cada grupo (tag).
    
    Args:
        df (pl.DataFrame): DataFrame de entrada.
        n (int): Número de filas top a extraer por grupo.
        tag_col (str): Nombre de la columna de agrupación.
        score_col (str): Nombre de la columna a rankear.
        
    Returns:
        pl.DataFrame: DataFrame filtrado con las top-N filas por grupo.
    """
    return (
        df.with_columns(
            pl.col(score_col).rank(method='ordinal', descending=True)
            .over(tag_col).alias('_rank')
        )
        .filter(pl.col('_rank') <= n)
        .drop('_rank')
        .sort([tag_col, score_col], descending=[False, True])
    )
