<template>
  <div class="busca-operadoras">
    <h2>Buscar Operadoras</h2>
    
    <input
      type="text"
      v-model="termoBusca"
      placeholder="Digite o nome da operadora"
      @input="buscarOperadoras"
    />

    <div v-if="carregando">Buscando...</div>

    <ul v-if="resultados.length">
      <li v-for="(operadora, index) in resultados" :key="index">
        <strong>{{ operadora.nome_fantasia }}</strong><br />
        CNPJ: {{ operadora.cnpj }}<br />
        Cidade: {{ operadora.cidade }} - {{ operadora.uf }}
      </li>
    </ul>

    <div v-else-if="!carregando && termoBusca.length > 2">
      Nenhuma operadora encontrada.
    </div>
  </div>
</template>

<script>
export default {
  name: "BuscaOperadoras",
  data() {
    return {
      termoBusca: "",
      resultados: [],
      carregando: false,
      delayBusca: null,
    };
  },
  methods: {
    buscarOperadoras() {
      clearTimeout(this.delayBusca);

      // Pequeno delay para não fazer requisições a cada tecla
      this.delayBusca = setTimeout(async () => {
        if (this.termoBusca.length < 3) {
          this.resultados = [];
          return;
        }

        this.carregando = true;

        try {
          const resposta = await fetch(`http://127.0.0.1:5000/buscar?q=${encodeURIComponent(this.termoBusca)}`);
          const dados = await resposta.json();
          this.resultados = dados;
        } catch (erro) {
          console.error("Erro ao buscar operadoras:", erro);
          this.resultados = [];
        } finally {
          this.carregando = false;
        }
      }, 300);
    },
  },
};
</script>

<style scoped>
.busca-operadoras {
  max-width: 600px;
  margin: 2rem auto;
  font-family: Arial, sans-serif;
}
input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1rem;
}
li {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
  padding-bottom: 0.5rem;
}
</style>
