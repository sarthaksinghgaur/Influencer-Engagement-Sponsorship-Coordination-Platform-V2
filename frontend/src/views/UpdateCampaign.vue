<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Edit Campaign</h1>
  
              <!-- Flash Messages -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Edit Campaign Form -->
              <form @submit.prevent="updateCampaign">
                <div class="mb-3">
                  <label for="name" class="form-label">Name:</label>
                  <input type="text" id="name" v-model="campaignData.name" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="description" class="form-label">Description:</label>
                  <textarea id="description" v-model="campaignData.description" class="form-control" rows="3" required></textarea>
                </div>
  
                <div class="mb-3">
                  <label for="start_date" class="form-label">Start Date:</label>
                  <input type="date" id="start_date" v-model="campaignData.start_date" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="end_date" class="form-label">End Date:</label>
                  <input type="date" id="end_date" v-model="campaignData.end_date" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="budget" class="form-label">Budget:</label>
                  <input type="number" id="budget" v-model="campaignData.budget" class="form-control" required />
                </div>
  
                <div class="mb-3">
                  <label for="visibility" class="form-label">Visibility:</label>
                  <select id="visibility" v-model="campaignData.visibility" class="form-select" required>
                    <option value="public">Public</option>
                    <option value="private">Private</option>
                  </select>
                </div>
  
                <div class="mb-3">
                  <label for="goals" class="form-label">Goals:</label>
                  <textarea id="goals" v-model="campaignData.goals" class="form-control" rows="3" required></textarea>
                </div>
  
                <!-- Action Buttons -->
                <div class="d-flex justify-content-between mt-4">
                  <button type="submit" class="btn btn-primary">Update Campaign</button>
                  <router-link :to="{ name: 'SponsorDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
                </div>
              </form>
  
              <!-- Delete Campaign Section -->
              <div class="d-flex justify-content-between mt-5">
                <h5>Want to delete this campaign?</h5>
                <button @click="deleteCampaign" class="btn btn-danger">Delete Campaign</button>
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
        campaignData: {
          name: '',
          description: '',
          start_date: '',
          end_date: '',
          budget: '',
          visibility: 'public',
          goals: ''
        },
        messages: []
      };
    },
    created() {
      this.fetchCampaignData();
    },
    methods: {
      fetchCampaignData() {
        const campaignId = this.$route.params.campaignId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to edit a campaign.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get(`http://localhost:8008/api/sponsor/UpdateCampaign/${campaignId}`, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            const data = response.data;
            this.campaignData = {
              name: data.name,
              description: data.description,
              start_date: data.start_date,
              end_date: data.end_date,
              budget: data.budget,
              visibility: data.visibility,
              goals: data.goals
            };
          })
          .catch(error => {
            console.error('Error fetching campaign data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching campaign data. Please try again.');
          });
      },
      updateCampaign() {
        const campaignId = this.$route.params.campaignId;
        const authToken = localStorage.getItem('authToken');
  
        if (!authToken) {
          this.messages.push('You must be logged in to update a campaign.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/sponsor/UpdateCampaign/${campaignId}`, this.campaignData, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.messages.push(response.data.message || 'Campaign updated successfully.');
          })
          .catch(error => {
            console.error('Error updating campaign:', error.response ? error.response.data : error.message);
            this.messages.push('Error updating campaign. Please try again.');
          });
      },
      deleteCampaign() {
        if (confirm('Are you sure you want to delete this campaign? This action cannot be undone.')) {
          const campaignId = this.$route.params.campaignId;
          const authToken = localStorage.getItem('authToken');
  
          if (!authToken) {
            this.messages.push('You must be logged in to delete a campaign.');
            setTimeout(() => {
              this.$router.push({ name: 'LoginPage' });
            }, 3000);
            return;
          }
  
          axios
            .delete(`http://localhost:8008/api/sponsor/DeleteCampaign/${campaignId}`, {
              headers: {
                Authorization: authToken
              }
            })
            .then(response => {
              this.messages.push(response.data.message || 'Campaign deleted successfully.');
              setTimeout(() => {
                this.$router.push({ name: 'SponsorDashboard' });
              }, 2000);
            })
            .catch(error => {
              console.error('Error deleting campaign:', error.response ? error.response.data : error.message);
              this.messages.push('Error deleting campaign. Please try again.');
            });
        }
      }
    }
  };
  </script>