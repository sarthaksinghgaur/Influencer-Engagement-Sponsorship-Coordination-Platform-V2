<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Sponsors</h1>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <!-- Sponsors Table -->
              <table class="table table-bordered table-hover mt-4">
                <thead class="table-light">
                  <tr>
                    <th>Company Name</th>
                    <th>Industry</th>
                    <th>Budget</th>
                    <th>Flagged</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="sponsor in sponsors" :key="sponsor.id">
                    <td>{{ sponsor.company_name }}</td>
                    <td>{{ sponsor.industry }}</td>
                    <td>{{ sponsor.budget }}</td>
                    <td>{{ sponsor.flagged ? 'Flagged' : 'Not Flagged' }}</td>
                    <td>
                      <!-- Flag/Unflag Button -->
                      <button @click="toggleFlagSponsor(sponsor.id)" class="btn btn-warning btn-sm">
                        {{ sponsor.flagged ? 'Unflag' : 'Flag' }}
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
        sponsors: [],
        messages: []
      };
    },
    created() {
      this.fetchSponsors();
    },
    methods: {
      fetchSponsors() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the sponsors.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/AdminViewSponsors', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.sponsors = response.data.map(sponsor => ({
              id: sponsor.id,
              company_name: sponsor.company_name,
              industry: sponsor.industry,
              budget: sponsor.budget,
              flagged: sponsor.flagged
            }));
          })
          .catch(error => {
            console.error('Error fetching sponsors:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching sponsors. Please try again.');
          });
      },
  
      toggleFlagSponsor(sponsorId) {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to perform this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/admin/FlagSponsor/${sponsorId}`, {}, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            console.log(response.data.message);
            this.messages.push(response.data.message || 'Sponsor status updated.');
            const updatedSponsor = this.sponsors.find(sponsor => sponsor.id === sponsorId);
            if (updatedSponsor) {
              updatedSponsor.flagged = !updatedSponsor.flagged;
            }
          })
          .catch(error => {
            console.error('Error toggling sponsor flag status:', error.response ? error.response.data : error.message);
            this.messages.push('Error toggling sponsor flag status. Please try again.');
          });
      },
  
      navigateToDashboard() {
        this.$router.push({ name: 'AdminDashboard' });
      }
    }
  };
  </script>