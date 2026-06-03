-- models/staging/stg_qualidade_agua.sql
-- View de staging que limpa e formata os dados brutos da qualidade de água

with source as (
    select * from {{ source('raw_data', 'qualidade_agua_bruta') }}
),

renamed as (
    select
        n_amostra::int as id_amostra,
        to_date(execucao_coleta, 'DD/MM/YYYY') as data_coleta,
        ponto_amostral,
        parametro,
        tipo_amostra,
        saa as sistema_abastecimento,
        ut as unidade_tratamento,
        local_amostrado,
        -- Substitui pontos de milhar e vírgula decimal para converter para float
        try_cast(replace(replace(resultado, '.', ''), ',', '.') as float) as valor_resultado,
        case 
            when em_conformidade = 'Sim' then true 
            else false 
        end as flg_em_conformidade
    from source
)

select * from renamed
