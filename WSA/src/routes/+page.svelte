<!-- src/routes/+page.svelte -->
<script lang="ts">
  import VereadorList from '$lib/components/VereadorList.svelte';
  import VereadorDetails from '$lib/components/VereadorDetails.svelte';
  import { appStore } from '$lib/stores/appStore';
</script>

<!-- A lógica principal da página é renderizada somente se não houver erro ou carregamento inicial -->
{#if !$appStore.error && !$appStore.loading}
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- O componente da lista de vereadores agora é importado -->
    <VereadorList />
    <!-- O componente de detalhes do vereador agora é importado -->
    <VereadorDetails />
  </div>
{/if}
