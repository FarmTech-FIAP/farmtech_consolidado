import numpy as np
import pandas as pd

# cria a base inicial de talhoes e salva em csv
def gerar_base_insumos(caminho_csv="services/ir_alem/insumos_otimizacao.csv"):
    np.random.seed(42)
    dados = {
        "talhao_id": [f"Talhao_{i+1}" for i in range(12)],
        "cultura": ["Milho", "Soja", "Milho", "Feijao", "Soja", "Milho", "Soja", "Algodao", "Milho", "Soja", "Milho", "Feijao"],
        "consumo_agua_m3": [120, 95, 140, 70, 85, 130, 90, 160, 110, 100, 135, 75],
        "custo_insumo_mil_brl": [4.2, 3.1, 5.0, 2.5, 3.0, 4.8, 3.2, 6.0, 4.0, 3.5, 4.9, 2.7],
        "produtividade_esperada_sacas": [180, 140, 210, 90, 135, 195, 145, 230, 170, 150, 205, 100]
    }
    df = pd.DataFrame(dados)
    df.to_csv(caminho_csv, index=False)
    return df

# algoritmo genetico baseado no problema da mochila
def executar_algoritmo_genetico(
    df_talhoes,
    limite_agua=700,
    orcamento_max=25.0,
    tam_populacao=40,
    geracoes=50,
    taxa_mutacao=0.05,
    tipo_selecao="roleta"
):
    total = len(df_talhoes)
    agua = df_talhoes["consumo_agua_m3"].values
    custos = df_talhoes["custo_insumo_mil_brl"].values
    sacas = df_talhoes["produtividade_esperada_sacas"].values

    # pontuacao do individuo
    def calcular_fitness(individuo):
        gasto_agua = np.sum(individuo * agua)
        gasto_custo = np.sum(individuo * custos)
        # se ultrapassar os recursos da fazenda, zera a pontuacao
        if gasto_agua > limite_agua or gasto_custo > orcamento_max:
            return 1e-4
        return np.sum(individuo * sacas)

    # populacao inicial com valores 0 ou 1
    populacao = np.random.randint(0, 2, size=(tam_populacao, total))
    historico = []

    for _ in range(geracoes):
        notas = np.array([calcular_fitness(ind) for ind in populacao])
        historico.append(np.max(notas))

        # selecao dos melhores
        if tipo_selecao == "torneio":
            selecionados = []
            for _ in range(tam_populacao):
                i1, i2 = np.random.choice(tam_populacao, 2, replace=False)
                selecionados.append(populacao[i1] if notas[i1] > notas[i2] else populacao[i2])
            populacao = np.array(selecionados)
        else: # roleta
            soma = np.sum(notas)
            probs = notas / soma if soma > 0 else np.ones(tam_populacao) / tam_populacao
            idx = np.random.choice(tam_populacao, size=tam_populacao, p=probs)
            populacao = populacao[idx]

        # cruzamento de um ponto
        filhos = []
        for i in range(0, tam_populacao, 2):
            p1, p2 = populacao[i], populacao[(i + 1) % tam_populacao]
            corte = np.random.randint(1, total)
            filhos.append(np.concatenate([p1[:corte], p2[corte:]]))
            filhos.append(np.concatenate([p2[:corte], p1[corte:]]))
        populacao = np.array(filhos[:tam_populacao])

        # mutacao simples
        mascara = np.random.rand(*populacao.shape) < taxa_mutacao
        populacao = np.bitwise_xor(populacao, mascara.astype(int))

    notas_finais = np.array([calcular_fitness(ind) for ind in populacao])
    melhor_idx = np.argmax(notas_finais)
    melhor = populacao[melhor_idx]

    return {
        "melhor_individuo": melhor,
        "produtividade_max": notas_finais[melhor_idx],
        "consumo_agua": np.sum(melhor * agua),
        "custo_total": np.sum(melhor * custos),
        "historico": historico
    }
