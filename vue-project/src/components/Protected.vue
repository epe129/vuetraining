<template>
  <div>
    <h1>Tervetuloa, {{ username || 'käyttäjä' }}!</h1>
    <p>Tämä sivu on suojattu — vain kirjautuneet käyttäjät näkevät sen.</p>
    <button @click="logout" class="b">Kirjaudu ulos</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      username: ''
    }
  },
  mounted() {
    // Verify authentication by asking the backend for the current user.
    // This request must include cookies so the server can read the
    // session (hence `withCredentials: true`). If unauthenticated,
    // the backend will respond with 401 and we silently ignore it here.
    axios.get('http://127.0.0.1:5000/me', { withCredentials: true })
      .then(res => {
        if (res.data && res.data.username) this.username = res.data.username
      })
      .catch(() => {})
  },
  methods: {
    logout() {
      // Call the backend to clear the server-side session, then
      // redirect the user back to the registration page.
      axios.post('http://127.0.0.1:5000/logout', {}, { withCredentials: true })
        .then(() => {
          this.$router.push('/')
        })
    }
  }
}
</script>

<style scoped>
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
</style>
