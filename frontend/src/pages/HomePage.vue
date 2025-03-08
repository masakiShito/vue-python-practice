<template>
  <div>
    <h1>FastAPI + Vue (TypeScript)</h1>
    <p>Message: {{ message }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api';

// TypeScriptで型を定義
const message = ref<string>('');

onMounted(async () => {
  try {
    const response = await api.get<{ message: string }>('/');
    message.value = response.data.message;
  } catch (error) {
    console.error('APIエラー:', error);
  }
});
</script>
