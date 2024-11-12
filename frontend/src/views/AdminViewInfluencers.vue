<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Influencers</h1>
              <h2 class="text-center mb-4">Your Influencers</h2>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Influencers Table -->
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Influencer Name</th>
                    <th>Category</th>
                    <th>Niche</th>
                    <th>Reach</th>
                    <th>Platform</th>
                    <th>Flagged</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="influencer in influencers" :key="influencer.id">
                    <td>{{ influencer.name }}</td>
                    <td>{{ influencer.category }}</td>
                    <td>{{ influencer.niche }}</td>
                    <td>{{ influencer.reach }}</td>
                    <td>{{ influencer.platform }}</td>
                    <td>{{ influencer.flagged ? 'Flagged' : 'Not Flagged' }}</td>
                    <td>
                      <!-- Flag/Unflag Button -->
                      <button @click="toggleFlagInfluencer(influencer.id)" class="btn btn-warning btn-sm">
                        {{ influencer.flagged ? 'Unflag' : 'Flag' }}
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
  
              <!-- Back to Dashboard Button -->
              <div class="d-flex justify-content-end mt-4">
                <button @click="navigateToDashboard" class="btn btn-secondary">Back to Dashboard</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        influencers: [],
        messages: []
      };
    },
    created() {
      this.fetchInfluencers();
    },
    methods: {
      fetchInfluencers() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the influencers.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/AdminViewInfluencers', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.influencers = response.data.map(influencer => ({
              id: influencer.id,
              name: influencer.name,
              category: influencer.category,
              niche: influencer.niche,
              reach: influencer.reach,
              platform: influencer.platform,
              flagged: influencer.flagged
            }));
          })
          .catch(error => {
            console.error('Error fetching influencers:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching influencers. Please try again.');
          });
      },
  
      toggleFlagInfluencer(influencerId) {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to perform this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/admin/FlagInfluencer/${influencerId}`, {}, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            console.log(response.data.message);
            this.messages.push(response.data.message || 'Influencer status updated.');
            const updatedInfluencer = this.influencers.find(influencer => influencer.id === influencerId);
            if (updatedInfluencer) {
              updatedInfluencer.flagged = !updatedInfluencer.flagged;
            }
          })
          .catch(error => {
            console.error('Error toggling influencer flag status:', error.response ? error.response.data : error.message);
            this.messages.push('Error toggling influencer flag status. Please try again.');
          });
      },
  
      navigateToDashboard() {
        this.$router.push({ name: 'AdminDashboard' });
      }
    }
  };
  </script>