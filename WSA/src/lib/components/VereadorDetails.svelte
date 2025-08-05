<!-- src/lib/components/VereadorDetails.svelte -->
<script lang="ts">
  import { appStore } from '$lib/stores/appStore';
</script>

<section class="lg:col-span-2">
  <article class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-8">
    {#if $appStore.loading && $appStore.vereadorDetalhes}
      <!-- Indicador de carregamento secundário -->
      <div class="flex items-center justify-center min-h-[300px]">
        <svg class="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span class="ml-4 text-xl">Carregando detalhes...</span>
      </div>
    {:else if $appStore.vereadorDetalhes}
      <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-200 mb-4 leading-snug">
        Análise Detalhada: {$appStore.vereadorDetalhes.Nome}
      </h2>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Abaixo estão os detalhes sobre as atividades e despesas de <span class="font-bold">{$appStore.vereadorDetalhes.Nome}</span>, para o período de 2023-2025.
      </p>

      <!-- Resumo da Presença -->
      <div class="bg-blue-50 dark:bg-blue-950 p-6 rounded-lg mb-6">
        <h3 class="text-xl font-semibold text-blue-700 dark:text-blue-300 mb-2">Presença em Sessões</h3>
        <p>
          <span class="font-bold text-green-600">Presente em {$appStore.vereadorDetalhes.Sessoes_Presente.length} sessões</span> e
          <span class="font-bold text-red-600">ausente em {$appStore.vereadorDetalhes.Sessoes_Ausente.length} sessões</span>.
        </p>
      </div>

      <!-- Tabela de Despesas -->
      <h3 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">Despesas</h3>
      <div class="overflow-x-auto mb-6">
        <table class="min-w-full bg-white dark:bg-gray-800 shadow-md rounded-lg">
          <thead class="bg-gray-200 dark:bg-gray-700">
            <tr>
              <th class="py-2 px-4 text-left font-semibold text-gray-700 dark:text-gray-300">Especificação</th>
              <th class="py-2 px-4 text-left font-semibold text-gray-700 dark:text-gray-300">Valor</th>
              <th class="py-2 px-4 text-left font-semibold text-gray-700 dark:text-gray-300">Mês/Ano</th>
            </tr>
          </thead>
          <tbody>
            {#if $appStore.vereadorDetalhes.Despesas.length > 0}
              {#each $appStore.vereadorDetalhes.Despesas as despesa (despesa.Especificação + despesa.Valor_Total)}
                <tr class="border-b last:border-b-0 border-gray-200 dark:border-gray-700">
                  <td class="py-2 px-4 text-gray-700 dark:text-gray-300">{despesa.Especificação}</td>
                  <td class="py-2 px-4 text-gray-700 dark:text-gray-300 font-medium">R$ {despesa.Valor_Total.toFixed(2)}</td>
                  <td class="py-2 px-4 text-gray-700 dark:text-gray-300">{despesa.Mês}/{despesa.Ano}</td>
                </tr>
              {/each}
            {:else}
              <tr>
                <td colspan="3" class="text-center py-4 text-gray-500">Nenhuma despesa registrada.</td>
              </tr>
            {/if}
          </tbody>
        </table>
      </div>

      <!-- Lista de Matérias Legislativas -->
      <h3 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4">Matérias Legislativas</h3>
      <div class="space-y-4">
        {#if $appStore.vereadorDetalhes.Materias_Legislativas.length > 0}
          {#each $appStore.vereadorDetalhes.Materias_Legislativas as materia (materia.Número)}
            <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg shadow">
              <p class="font-semibold text-lg text-gray-800 dark:text-gray-200">{materia.Tipo} - {materia.Número}</p>
              <p class="text-gray-600 dark:text-gray-300 mt-1">{materia.Ementa}</p>
              <p class="text-sm text-gray-500 dark:text-gray-400 mt-2">Status: <span class="font-medium">{materia.Status}</span></p>
            </div>
          {/each}
        {:else}
          <p class="text-center text-gray-500 dark:text-gray-400">Nenhuma matéria legislativa registrada.</p>
        {/if}
      </div>

    {:else}
      <!-- Mensagem caso nenhum vereador seja selecionado -->
      <div class="text-center text-gray-500 dark:text-gray-400">
        Selecione um vereador na lista ao lado para ver os detalhes.
      </div>
    {/if}
  </article>
</section>
