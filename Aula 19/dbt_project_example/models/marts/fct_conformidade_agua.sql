-- models/marts/fct_conformidade_agua.sql
-- Tabela analítica agregando a conformidade por ponto amostral e parâmetro

with stg_qualidade as (
    select * from {{ ref('stg_qualidade_agua') }}
)

select
    ponto_amostral,
    parametro,
    count(id_amostra) as total_amostras,
    count_if(flg_em_conformidade) as amostras_em_conformidade,
    count_if(not flg_em_conformidade) as amostras_fora_conformidade,
    round(100.0 * count_if(flg_em_conformidade) / count(id_amostra), 2) as taxa_conformidade_pct,
    current_timestamp() as _processado_em
from stg_qualidade
group by ponto_amostral, parametro
