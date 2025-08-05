// src/lib/stores/appStore.ts
import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

// Definição das interfaces para tipagem
export interface VereadorResumo {
  Nome: string;
  Total_Despesas: number;
  Num_Proposições: number;
  Total_Sessões_Presente: number;
  Total_Sessões_Ausente: number;
}

export interface Despesa {
    Ano: number;
    Mês: number;
    Especificação: string;
    Valor_Total: number;
    Saldo: number;
}

export interface MateriaLegislativa {
    Número: string;
    Tipo: string;
    Ementa: string;
    Apresentação: string;
    Status: string;
    Última_Ação: string;
}

export interface VereadorDetalhes {
    Nome: string;
    Despesas: Despesa[];
    Materias_Legislativas: MateriaLegislativa[];
    Sessoes_Presente: string[];
    Sessoes_Ausente: string[];
}

// Interface para o estado global da aplicação
interface AppState {
  vereadores: VereadorResumo[];
  vereadorDetalhes: VereadorDetalhes | null;
  nomeVereadorSelecionado: string;
  loading: boolean;
  error: string | null;
}

// URL da sua API FastAPI.
const API_URL = 'http://127.0.0.1:8000';

// Cria um Svelte store reativo para gerenciar o estado da aplicação.
export const appStore: Writable<AppState> = writable({
  vereadores: [],
  vereadorDetalhes: null,
  nomeVereadorSelecionado: '',
  loading: true,
  error: null,
});

/**
 * Função para buscar a lista de todos os vereadores.
 * Atualiza o store com os dados e o estado de carregamento.
 */
export async function fetchVereadores(): Promise<VereadorResumo[]> {
  appStore.update(state => ({ ...state, loading: true, error: null }));
  try {
    const response = await fetch(`${API_URL}/vereadores`);
    if (!response.ok) {
      throw new Error(`Erro ao carregar a lista de vereadores: ${response.statusText}`);
    }
    const vereadores: VereadorResumo[] = await response.json();
    appStore.update(state => ({ ...state, vereadores, loading: false }));
    return vereadores;
  } catch (err: any) {
    console.error(err);
    appStore.update(state => ({ ...state, error: 'Não foi possível carregar a lista de vereadores.', loading: false }));
    return [];
  }
}

/**
 * Função para buscar os detalhes de um vereador específico.
 * @param {string} nome O nome do vereador a ser buscado.
 */
export async function fetchVereadorDetalhes(nome: string): Promise<void> {
  appStore.update(state => ({ ...state, loading: true, error: null, nomeVereadorSelecionado: nome }));
  try {
    const response = await fetch(`${API_URL}/vereadores/${nome}`);
    if (!response.ok) {
      throw new Error(`Erro ao carregar os detalhes do vereador: ${response.statusText}`);
    }
    const vereadorDetalhes: VereadorDetalhes = await response.json();
    appStore.update(state => ({ ...state, vereadorDetalhes, loading: false }));
  } catch (err: any) {
    console.error(err);
    appStore.update(state => ({ ...state, vereadorDetalhes: null, error: 'Não foi possível carregar os detalhes do vereador.', loading: false }));
  }
}
