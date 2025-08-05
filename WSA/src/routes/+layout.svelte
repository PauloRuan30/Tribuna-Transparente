<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import '../app.css'; // Importa os estilos globais, incluindo Tailwind
  import { onMount } from 'svelte';
  import { fetchVereadores, fetchVereadorDetalhes } from '$lib/stores/appStore';
  import { appStore } from '$lib/stores/appStore';
  
  // Carrega a lista de vereadores no início da aplicação.
  onMount(async () => {
    const vereadores = await fetchVereadores();
    if (vereadores.length > 0) {
      await fetchVereadorDetalhes(vereadores[0].Nome);
    }
  });
</script>

<main class="min-h-screen bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 p-4 md:p-8 font-sans transition-colors duration-300">
  <!-- Cabeçalho estilo "Jornal" -->
  <header class="text-center mb-10">
    <h1 class="text-4xl md:text-6xl font-extrabold text-blue-700 dark:text-blue-400 leading-tight tracking-wide">
      Tribuna Transparente
    </h1>
    <p class="mt-2 text-lg md:text-xl font-light text-gray-600 dark:text-gray-400">
      Análise de Despesas, Atividades e Presença dos Vereadores.
    </p>
    <hr class="mt-4 border-gray-300 dark:border-gray-700">
  </header>

  <!-- O slot é onde o conteúdo das páginas (como +page.svelte) será renderizado -->
  <slot />

  {#if $appStore.error}
    <div class="bg-red-500 text-white p-4 rounded-lg shadow-md max-w-xl mx-auto text-center">
      {$appStore.error}
    </div>
  {:else if $appStore.loading && !$appStore.vereadorDetalhes}
    <!-- Indicador de carregamento inicial -->
    <div class="flex items-center justify-center min-h-[300px]">
      <svg class="animate-spin h-10 w-10 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <span class="ml-4 text-xl">Carregando dados...</span>
    </div>
  {/if}
</main>

<style>
  /* Estilos globais para a página */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Merriweather:wght@700&display=swap');
  :global(body) {
    font-family: 'Inter', sans-serif;
  }
  h1, h2 {
    font-family: 'Merriweather', serif;
  }
</style>
