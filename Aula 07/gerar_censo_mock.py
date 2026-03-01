#mock de dados reais do Censo Escolar 2023, com buracos injetados propositalmente 
# em QT_MAT_BAS e QT_DOC_BAS, e alguns outliers violentos
# 
import csv
import random

def generate_censo_mock():
    random.seed(2026)
    n_rows = 5000

    # Headers for the CSV
    headers = [
        'NU_ANO_CENSO', 'SG_UF', 'NO_MUNICIPIO', 'TP_DEPENDENCIA',
        'QT_MAT_BAS', 'QT_DOC_BAS', 'IN_AGUA_FILTRADA', 
        'IN_BIBLIOTECA', 'IN_INTERNET', 'COLUNA_OBSOLETA'
    ]
    
    ufs = ['SP', 'MG', 'RJ', 'BA', 'RS', 'PE', 'CE']
    municipios = ['São Paulo', 'Campinas', 'Belo Horizonte', 'Rio de Janeiro', 'Salvador', 'Porto Alegre', 'Recife']
    
    rows = []
    
    for i in range(n_rows):
        ano = 2023
        uf = random.choice(ufs)
        municipio = random.choice(municipios)
        
        # Dependencia: 1-Federal, 2-Estadual, 3-Municipal, 4-Privada
        rnd_dep = random.random()
        if rnd_dep < 0.1: dependencia = 1
        elif rnd_dep < 0.5: dependencia = 2
        elif rnd_dep < 0.8: dependencia = 3
        else: dependencia = 4
            
        mat_bas = random.randint(50, 1500)
        doc_bas = random.randint(5, 120)
        
        agua = 1 if random.random() < 0.8 else 0
        bib = 1 if random.random() < 0.6 else 0
        net = 1 if random.random() < 0.7 else 0
        col_obs = '' # Vazia
        
        # Injecting nulls (empty strings)
        if random.random() < 0.25:
            mat_bas = '' # 25% missing
            
        if random.random() < 0.15:
            doc_bas = '' # 15% missing
            
        if random.random() < 0.05:
            bib = '' # 5% missing
            
        # Outliers in QT_DOC_BAS (around 1% chance for non-nulls)
        if doc_bas != '' and random.random() < 0.01:
            doc_bas = random.randint(5000, 10000)
            
        rows.append([ano, uf, municipio, dependencia, mat_bas, doc_bas, agua, bib, net, col_obs])

    output_path = r'g:\Meu Drive\Concursos\Atividades acadêmicas\IBEMEC\Disciplinas\Extração de dados\data-extraction-course\Aula 07\censo_escolar_amostra_com_nulos.csv'
    
    with open(output_path, 'w', newline='', encoding='latin-1') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(headers)
        writer.writerows(rows)
        
    print(f"Dataset Censo Escolar ('censo_escolar_amostra_com_nulos.csv') gerado com sucesso!")
    print(f"Total de Linhas: {n_rows}")

if __name__ == "__main__":
    generate_censo_mock()
