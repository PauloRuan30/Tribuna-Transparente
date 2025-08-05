# app/models.py
# Este arquivo contém todos os modelos de dados Pydantic usados pela API.
# Separar os modelos facilita a manutenção e a reutilização do código.

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Despesa(BaseModel):
    Ano: int
    Mês: int
    Especificação: str
    Valor_Total: float
    Saldo: float

class MateriaLegislativa(BaseModel):
    Número: str
    Tipo: str
    Ementa: str
    Apresentação: str
    Status: str
    Última_Ação: str

class VereadorResumo(BaseModel):
    Nome: str
    Total_Despesas: float
    Num_Proposições: int
    Total_Sessões_Presente: int
    Total_Sessões_Ausente: int

class VereadorDetalhes(BaseModel):
    Nome: str
    Despesas: List[Despesa]
    Materias_Legislativas: List[MateriaLegislativa]
    Sessoes_Presente: List[str]
    Sessoes_Ausente: List[str]
