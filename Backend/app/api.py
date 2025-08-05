# app/api.py
# Este arquivo define a instância do FastAPI e as rotas da sua API.
# Ele usa o módulo `data_loader` para obter os dados.

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware # Importe o CORSMiddleware
from typing import List, Dict, Any
from .data_loader import carregar_e_processar_dados
from .models import VereadorResumo, VereadorDetalhes, Despesa, MateriaLegislativa

# Variável para armazenar os dados processados globalmente.
vereadores_dados: Dict[str, Any] = {}

# Configuração do FastAPI
app = FastAPI(
    title="Análise Legislativa e de Despesas",
    description="Uma API para explorar dados de despesas e atividades de vereadores.",
    version="1.0.0"
)

# Configuração do CORS
# Adicione esta seção para permitir que seu frontend acesse a API
origins = [
    "http://localhost",
    "http://localhost:5173", # Onde seu frontend SvelteKit está rodando
    "http://127.0.0.1:5173", # Outra forma comum de localhost
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todos os cabeçalhos
)

# Carrega e processa os dados no startup da aplicação
@app.on_event("startup")
async def startup_event():
    """
    Esta função é executada quando o servidor inicia.
    Ela carrega todos os dados necessários do módulo `data_loader`.
    """
    global vereadores_dados
    vereadores_dados = carregar_e_processar_dados()

# Endpoints da API

@app.get("/", summary="Endpoint inicial", tags=["Geral"])
async def read_root():
    """
    Retorna uma mensagem de boas-vindas e um resumo dos dados disponíveis.
    """
    return {
        "message": "Bem-vindo à API de Análise Legislativa!",
        "resumo_dados": {
            "total_vereadores": len(vereadores_dados),
            # total_despesas_registradas pode ser calculado aqui se necessário
            "total_vereadores_detalhes": list(vereadores_dados.keys())
        }
    }

@app.get("/vereadores", response_model=List[VereadorResumo], summary="Lista todos os vereadores", tags=["Vereadores"])
async def get_vereadores():
    """
    Retorna uma lista com um resumo de cada vereador, incluindo despesas e proposições.
    """
    resumo_vereadores = []
    for nome, dados in vereadores_dados.items():
        total_despesas = sum(d.get('Valor Total', 0) for d in dados['despesas'])
        num_proposicoes = len(dados['materias_legislativas'])
        resumo = VereadorResumo(
            Nome=nome,
            Total_Despesas=total_despesas,
            Num_Proposições=num_proposicoes,
            Total_Sessões_Presente=len(dados['sessoes_presente']),
            Total_Sessões_Ausente=len(dados['sessoes_ausente'])
        )
        resumo_vereadores.append(resumo)
    return resumo_vereadores

@app.get("/vereadores/{nome_vereador}", response_model=VereadorDetalhes, summary="Detalhes de um vereador específico", tags=["Vereadores"])
async def get_vereador(nome_vereador: str):
    """
    Retorna todos os detalhes disponíveis para um vereador específico.
    """
    nome_padronizado = nome_vereador.strip().upper().replace('DO NOSSA CARA', '').replace('PROFESSOR ', '').replace('PROFESSORA ', '').strip()
    if nome_padronizado not in vereadores_dados:
        raise HTTPException(status_code=404, detail="Vereador não encontrado")

    dados = vereadores_dados[nome_padronizado]
    
    # Processar despesas
    despesas_lista = [
        Despesa(
            Ano=int(d.get('Ano')),
            Mês=int(d.get('Mês')),
            Especificação=d.get('Especificação'),
            Valor_Total=float(d.get('Valor Total', 0)),
            Saldo=float(d.get('Saldo', 0))
        ) for d in dados['despesas']
    ]
    
    # Processar matérias legislativas
    materias_lista = [
        MateriaLegislativa(
            Número=m.get('Número'),
            Tipo=m.get('Tipo'),
            Ementa=m.get('Ementa'),
            Apresentação=m.get('Apresentação'),
            Status=m.get('Status'),
            Última_Ação=m.get('Última Ação')
        ) for m in dados['materias_legislativas']
    ]

    return VereadorDetalhes(
        Nome=nome_padronizado,
        Despesas=despesas_lista,
        Materias_Legislativas=materias_lista,
        Sessoes_Presente=dados['sessoes_presente'],
        Sessoes_Ausente=dados['sessoes_ausente']
    )
