<script setup>
import { ref } from 'vue';
import axios from 'axios';

const termo = ref('');
const operadoras = ref([]);
const erro = ref('');

const buscarOperadoras = async () => {
  if (!termo.value) {
    erro.value = 'Digite um termo para buscar!';
    return;
  }

  erro.value = '';
  try {
    const response = await axios.get(`http://127.0.0.1:5000/api/busca?termo=${termo.value}`);
    operadoras.value = response.data;
  } catch (err) {
    erro.value = 'Erro ao buscar operadoras.';
  }
};
</script>

<template>
  <div>
    <h2>Buscar Operadoras</h2>
    <input v-model="termo" placeholder="Digite um nome" />
    <button @click="buscarOperadoras">Buscar</button>
    
    <p v-if="erro" style="color: red;">{{ erro }}</p>
    
    <ul v-if="operadoras.length">
      <li v-for="(operadora, index) in operadoras" :key="index">
        {{ operadora.nome }} - {{ operadora.cidade }}
      </li>
    </ul>
  </div>
</template>
