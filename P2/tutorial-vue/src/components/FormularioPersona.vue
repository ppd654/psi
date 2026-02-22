<template>
  <div id="formulario-persona">
    <form @submit.prevent="enviarFormulario">
      <div class="container">
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <label>Nombre</label>
              <input v-model="persona.nombre" type="text" class="form-control" />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>Apellido</label>
              <input v-model="persona.apellido" type="text" class="form-control" />
            </div>
          </div>
          <div class="col-md-4">
            <div class="form-group">
              <label>Email</label>
              <input v-model="persona.email" type="email" class="form-control" />
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-4">
            <div class="form-group">
              <br />
              <button class="btn btn-primary">Añadir persona</button>
            </div>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineOptions({
  name: 'formulario-persona',
});

// Variables donde se guardan los datos mientras escribes
const persona = ref({
  nombre: '',
  apellido: '',
  email: '',
});

// Definimos el evento que vamos a enviar a App.vue
const emit = defineEmits(['add-persona']);

const enviarFormulario = () => {
  // Emitimos el evento 'add-persona' adjuntando los datos escritos
  emit('add-persona', persona.value);
  
  // Limpiamos las cajas de texto para poder añadir otro
  persona.value = { nombre: '', apellido: '', email: '' };
};
</script>

<style scoped>
form {
  margin-bottom: 2rem;
}
</style>