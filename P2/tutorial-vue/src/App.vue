<template>
  <div id="app" class="container">
    <div class="row">
      <div class="col-md-12">
        <h1>Personas</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <formulario-persona @add-persona="agregarPersona" />
        
        <tabla-personas :personas="personas" />
      </div>
    </div>
  </div>
</template>

<script setup>
import TablaPersonas from '@/components/TablaPersonas.vue';
import FormularioPersona from '@/components/FormularioPersona.vue';
import { ref } from 'vue';

// Nuestra lista maestra de datos
const personas = ref([
  { id: 1, nombre: 'Jon', apellido: 'Nieve', email: 'jon@email.com' },
  { id: 2, nombre: 'Tyrion', apellido: 'Lannister', email: 'tyrion@email.com' },
  { id: 3, nombre: 'Daenerys', apellido: 'Targaryen', email: 'daenerys@email.com' },
]);

// Esta función se ejecuta cuando el formulario nos avisa de que hay una nueva persona
const agregarPersona = (personaNueva) => {
  let id = 0;
  if (personas.value.length > 0) {
    id = personas.value[personas.value.length - 1].id + 1;
  }
  personas.value = [...personas.value, { ...personaNueva, id }];
};
</script>

<style>
/* Estilos globales para los botones como pide la práctica */
button {
  background: #009435;
  border: 1px solid #009435;
}
</style>