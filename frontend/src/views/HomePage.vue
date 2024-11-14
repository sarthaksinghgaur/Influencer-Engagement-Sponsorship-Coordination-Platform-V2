<template>
  <div class="container mt-5">
    <div class="text-center">
      <h1 class="display-4">Influencer Engagement & Sponsorship Coordination Platform - V2</h1>
      <h2 class="text-muted">IITM MAD2 PROJECT</h2>
    </div>

    <!-- Flash messages section -->
    <div v-if="messages.length" class="alert alert-info mt-4">
      <ul class="list-unstyled">
        <li v-for="(message, index) in messages" :key="index">
          {{ message }}
        </li>
      </ul>
    </div>

    <div class="button-container mt-4 d-flex justify-content-center">
      <router-link :to="{ name: 'LoginPage' }">
        <button class="btn btn-primary mx-2">Login</button>
      </router-link>
      <router-link :to="{ name: 'SignupPage' }">
        <button class="btn btn-success mx-2">Sign Up</button>
      </router-link>
    </div>
    <div class="text-center">
    <p></p>
    <p></p>
    <p></p>
    <p class="lead">21f3001936 : Sarthak Singh Gaur</p>
  </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      messages: []
    };
  },
  created() {
    if (this.$route.query.message) {
      this.messages.push(this.$route.query.message);
    }
  }
};
</script>