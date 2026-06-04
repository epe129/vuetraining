<template>
  <h1>{{ title }}</h1>
  <br/>
  <form @submit.prevent="registerAnswer">
    <p>nimi: <input type="text" required v-model="name"></p>
    <p>salasana: <input type="password" v-model="password"></p>
    <button type="submit" class="b">Rekisteröidy</button>
  </form>
  <a><router-link to="/kirjaudu">kirjaudu</router-link></a>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      name: '',
      password: '',
      title: 'Rekisteröidy'
    }
  },
  methods: {
    registerAnswer() {
      const path = 'http://127.0.0.1:5000/rekisteröidy'
      axios.post(path, {
        name: this.name,
        password: this.password,
      })
      .then(response => console.log(response))
      .catch(error => {
        this.errorMessage = error.message;
        console.error("There was an error!", error);
      })
    }
  }
};
</script>
<style>
  form {
    border-radius: 5px;
    background-color: #f2f2f2;
    padding: 20px;
  }

  label {display: block;}

  input {
    width: 100%;
    padding: 12px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .b {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    padding: 14px;
    margin: 8px 0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .b:hover {
    background-color: #45a049;
  }

  p {
    color: black;
  }

  a { 
    margin-left: 110px;
    color: white;
    cursor: pointer;
  }
</style>