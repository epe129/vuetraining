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
      title: 'Kirjaudu'
    }
  },
  methods: {
    kirjauduAnswer() {
      const path = 'http://127.0.0.1:5000/kirjaudu'
      // Send login credentials to the backend. `withCredentials: true`
      // ensures the browser will accept/set the session cookie sent
      // by Flask; the cookie is then used for subsequent `/me` checks.
      axios.post(path, {
        name: this.name,
        password: this.password,
      }, { withCredentials: true })
      .then(response => {
        // Explicit, simple success check: if backend returns 200
        // treat it as successful login and redirect.
        if (response.status === 200) {
          this.$router.push('/protected')
        } else {
          this.errorMessage = response.data?.error || 'Login failed'
        }
      })
      .catch(error => {
        // Show a readable error message if available from the server
        this.errorMessage = error.response?.data?.error || error.message || 'Network error'
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
</style>