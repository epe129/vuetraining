<template>
    <h1>{{ title }}</h1>
    <br/>
    <form @submit.prevent="kirjauduAnswer">
      <p>nimi: <input type="text" required v-model="name"></p>
      <p>salasana: <input type="password" v-model="password"></p>
      <button type="submit" class="b">kirjaudu</button>
    </form>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      name: '',
      password: '',
      nameSubmitted: '',
      passwordSubmitted: '',
      title: 'Kirjaudu'
    }
  },
  methods: {
    kirjauduAnswer() {
      if(this.name || this.password) {
        this.nameSubmitted = this.name;
        this.passwordSubmitted = this.password;
        console.log(this.nameSubmitted, " ", this.passwordSubmitted)
      }
      const path = 'http://127.0.0.1:5000/kirjaudu'
      axios.post(path, {
        name: this.nameSubmitted,
        password: this.passwordSubmitted,
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
</style>