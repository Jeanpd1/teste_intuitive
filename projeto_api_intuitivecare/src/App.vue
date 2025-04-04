<script setup>
import BuscaOperadoras from './components/BuscaOperadoras.vue';
</script>
<template>
  <div id="app">
    <BuscaOperadoras />
  </div>
</template>

<script>
import BuscaOperadoras from './components/busca_operadoras.vue';

export default {
  name: 'App',
  components: {
    BuscaOperadoras
  }
};
</script>
<template>
  <div>
    <header>
      <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
      <h1>Consulta de Operadoras</h1>
    </header>

    <main>
      <BuscaOperadoras />
    </main>
  </div>
</template>

<style scoped>
header {
  text-align: center;
  margin-bottom: 20px;
}

.logo {
  display: block;
  margin: 0 auto;
}
</style>