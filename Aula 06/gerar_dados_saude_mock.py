#Um 'mock' de 2.000 pacientes, injetado intencionalmente 
# com os 3 mecanismos explicados em sala:
# - IMC "apagado" na sorte (MCAR).
# - Retorno_Consulta falhando mais dependendo do 'Sexo' (MAR).
# - Renda propositadamente faltando nos extremos mais ricos e nas rendas mais baixas (MNAR).

import csv
import random

def generate_medical_mock():
    random.seed(42)
    n_rows = 2000

    headers = [
        'ID_Paciente', 'Idade', 'Sexo', 'Fumante', 
        'Pressao_Sistolica', 'Pressao_Diastolica', 'Colesterol_Total', 
        'IMC', 'Retorno_Consulta', 'Renda_Familiar'
    ]
    
    rows = []
    
    for i in range(1, n_rows + 1):
        id_paciente = f"PAC-{i:04d}"
        idade = random.randint(18, 90)
        sexo = random.choice(['M', 'F'])
        fumante = random.choice(['Sim', 'Não'])
        
        # Base vitals dependent on age and smoking
        psist = random.randint(110, 160) + (10 if idade > 60 else 0) + (15 if fumante == 'Sim' else 0)
        pdiast = random.randint(70, 100) + (5 if idade > 60 else 0)
        colesterol = random.randint(150, 280) + (20 if idade > 50 else 0)
        
        imc = round(random.uniform(18.5, 40.0), 1)
        retorno = random.choice([0, 1])
        
        # MNAR in income - lower response rates from higher and lower income brackets
        renda_base = random.randint(1500, 20000)
        
        # Creating missing data scenarios
        
        # 1. MCAR: 'IMC' missing completely at random (15% missing)
        imc_val = '' if random.random() < 0.15 else imc
        
        # 2. MAR: Men are more likely to have missing 'Retorno_Consulta' (30% missing for M, 10% for F)
        retorno_val = retorno
        if sexo == 'M' and random.random() < 0.30:
            retorno_val = ''
        elif sexo == 'F' and random.random() < 0.10:
            retorno_val = ''
            
        # 3. MNAR: Missing Not At Random in Renda_Familiar. VERY common in practice.
        # High and Low earners are less likely to disclose.
        renda_val = renda_base
        if (renda_base > 15000 and random.random() < 0.6) or (renda_base < 3000 and random.random() < 0.4):
            renda_val = ''
            
        # 4. Total Loss / Unsalvageable Column ('Colesterol_Total')
        # We will make 80% missing to act as the column students will eventually drop in the next class
        colesterol_val = '' if random.random() < 0.8 else colesterol
            
        # Small MCAR injection just to dirty things up a bit
        psist_val = '' if random.random() < 0.05 else psist
        pdiast_val = '' if random.random() < 0.05 else pdiast
        
        rows.append([
            id_paciente, idade, sexo, fumante, 
            psist_val, pdiast_val, colesterol_val, 
            imc_val, retorno_val, renda_val
        ])

    output_path = r'g:\Meu Drive\Concursos\Atividades acadêmicas\IBEMEC\Disciplinas\Extração de dados\data-extraction-course\Aula 06\dados_clinicos_brutos.csv'
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(headers)
        writer.writerows(rows)
        
    print(f"Dataset Clínico ('dados_clinicos_brutos.csv') gerado com sucesso!")
    print(f"Total de Registros: {n_rows}")

if __name__ == "__main__":
    generate_medical_mock()
