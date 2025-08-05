<!-- src/lib/components/VereadorList.svelte -->
<script lang="ts">
  import { appStore, fetchVereadorDetalhes } from '$lib/stores/appStore';
</script>

<aside class="lg:col-span-1">
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 h-full overflow-y-auto max-h-[80vh]">
    <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-4 border-b pb-2 border-gray-200 dark:border-gray-700">
      Últimas Notícias:
    </h2>
    <ul>
      {#each $appStore.vereadores as vereador (vereador.Nome)}
        <li class="mb-4">
          <button
            on:click={() => fetchVereadorDetalhes(vereador.Nome)}
            class="w-full text-left p-4 rounded-lg transition-all duration-200
            {$appStore.nomeVereadorSelecionado === vereador.Nome ? 'bg-blue-100 dark:bg-blue-900 border-l-4 border-blue-500' : 'hover:bg-gray-50 dark:hover:bg-gray-700'}">
            <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-200">
              {vereador.Nome}
            </h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
              Despesas: <span class="font-bold text-red-500">R$ {vereador.Total_Despesas.toFixed(2)}</span>
              <br/>
              Proposições: <span class="font-bold text-green-500">{vereador.Num_Proposições}</span>
            </p>
          </button>
        </li>
      {/each}
    </ul>
  </div>
</aside>
