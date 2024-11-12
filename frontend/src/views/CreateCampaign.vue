<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow">
          <div class="card-body">
            <h1 class="text-center mb-4">Create Campaign</h1>

            <!-- Flash Messages -->
            <div v-if="messages.length" class="alert alert-info">
              <ul class="list-unstyled mb-0">
                <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
              </ul>
            </div>

            <!-- Campaign Form -->
            <form @submit.prevent="submitCampaign">
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
                <button type="submit" class="btn btn-primary">Create Campaign</button>
                <router-link :to="{ name: 'SponsorDashboard' }" class="btn btn-secondary">Back to Dashboard</router-link>
              </div>
            </form>
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
  methods: {
    submitCampaign() {
      const authToken = localStorage.getItem('authToken');
      if (!authToken) {
        this.messages.push('You must be logged in to create a campaign.');
        setTimeout(() => {
          this.$router.push({ name: 'LoginPage' });
        }, 3000);
        return;
      }

      axios
        .post('http://localhost:8008/api/sponsor/CreateCampaign', this.campaignData, {
          headers: {
            Authorization: authToken
          }
        })
        .then(response => {
          this.messages.push(response.data.message || 'Campaign created successfully.');
          this.clearForm();
        })
        .catch(error => {
          console.error('Error creating campaign:', error.response ? error.response.data : error.message);
          this.messages.push('Error creating campaign. Please try again.');
        });
    },
    clearForm() {
      this.campaignData = {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: '',
        visibility: 'public',
        goals: ''
      };
    }
  }
};
</script>