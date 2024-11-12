<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-10">
          <div class="card shadow">
            <div class="card-body">
              <h1 class="text-center mb-4">Admin Dashboard</h1>
              <h2 class="text-center mb-4">Welcome, Admin</h2>
  
              <!-- Flash messages section -->
              <div v-if="messages.length" class="alert alert-info">
                <ul class="list-unstyled mb-0">
                  <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
                </ul>
              </div>
  
              <div class="statistics mt-4">
                <h2>Statistics</h2>
                <ul>
                  <li><strong>Active Users:</strong> {{ stats.active_users }}</li>
                  <li><strong>Total Campaigns:</strong> {{ stats.total_campaigns }}</li>
                  <li><strong>Public Campaigns:</strong> {{ stats.public_campaigns }}</li>
                  <li><strong>Private Campaigns:</strong> {{ stats.private_campaigns }}</li>
                  <li><strong>Ad Requests:</strong> {{ stats.ad_requests }}</li>
                  <li><strong>Negotiations Ad Requests:</strong> {{ stats.pending_ad_requests }}</li>
                  <li><strong>Accepted Ad Requests:</strong> {{ stats.accepted_ad_requests }}</li>
                  <li><strong>Rejected Ad Requests:</strong> {{ stats.rejected_ad_requests }}</li>
                  <li><strong>Flagged Sponsors:</strong> {{ stats.flagged_sponsors }}</li>
                  <li><strong>Flagged Influencers:</strong> {{ stats.flagged_influencers }}</li>
                </ul>
              </div>
  
              <!-- Pending Sponsors Section -->
              <div class="pending-sponsors mt-5">
                <h2>Pending Sponsors for Approval</h2>
                <table class="table table-bordered table-hover mt-4">
                  <thead class="table-light">
                    <tr>
                      <th>Company Name</th>
                      <th>Industry</th>
                      <th>Budget</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="sponsor in pendingSponsors" :key="sponsor.id">
                      <td>{{ sponsor.company_name }}</td>
                      <td>{{ sponsor.industry }}</td>
                      <td>{{ sponsor.budget }}</td>
                      <td>
                        <!-- Approve Sponsor Button -->
                        <button @click="approveSponsor(sponsor.id)" class="btn btn-success btn-sm">Approve</button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
  
              <h2 class="mt-5">Actions</h2>
                <div class="button-container mt-4">
                <button @click="navigateTo('AdminViewUsers')" class="btn btn-primary">Manage Accounts</button>
                <button @click="navigateTo('AdminViewInfluencers')" class="btn btn-primary">Manage Influencers Database</button>
                <button @click="navigateTo('AdminViewSponsors')" class="btn btn-primary">Manage Sponsors Database</button>
                <button @click="navigateTo('AdminViewCampaigns')" class="btn btn-primary">Manage Campaigns Database</button>
                <button @click="navigateTo('AdminViewAdrequests')" class="btn btn-primary">Manage Ad Requests Database</button>
                <button @click="logout" class="btn btn-danger">Logout</button>
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
        stats: {
          active_users: 0,
          total_campaigns: 0,
          public_campaigns: 0,
          private_campaigns: 0,
          ad_requests: 0,
          pending_ad_requests: 0,
          accepted_ad_requests: 0,
          rejected_ad_requests: 0,
          flagged_sponsors: 0,
          flagged_influencers: 0,
        },
        pendingSponsors: [],
        messages: []
      };
    },
    created() {
      this.fetchAdminDashboard();
      this.fetchPendingSponsors();
    },
    methods: {
      fetchAdminDashboard() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the dashboard.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/AdminDashboard', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.stats = response.data.stats;
            this.messages = response.data.flashMessages || [];
          })
          .catch(error => {
            console.error('Error fetching admin dashboard data:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching admin dashboard data. Please try again.');
          });
      },
  
      fetchPendingSponsors() {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in as an admin to view the pending sponsors.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .get('http://localhost:8008/api/admin/PendingSponsors', {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            this.pendingSponsors = response.data.pending_sponsors;
          })
          .catch(error => {
            console.error('Error fetching pending sponsors:', error.response ? error.response.data : error.message);
            this.messages.push('Error fetching pending sponsors. Please try again.');
          });
      },
  
      approveSponsor(sponsorId) {
        const authToken = localStorage.getItem('authToken');
        if (!authToken) {
          this.messages.push('You must be logged in to perform this action.');
          setTimeout(() => {
            this.$router.push({ name: 'LoginPage' });
          }, 3000);
          return;
        }
  
        axios
          .post(`http://localhost:8008/api/admin/ApproveSponsor/${sponsorId}`, {}, {
            headers: {
              Authorization: authToken
            }
          })
          .then(response => {
            console.log(response.data.message);
            this.messages.push(response.data.message || 'Sponsor approved successfully.');
            this.pendingSponsors = this.pendingSponsors.filter(sponsor => sponsor.id !== sponsorId);
          })
          .catch(error => {
            console.error('Error approving sponsor:', error.response ? error.response.data : error.message);
            this.messages.push('Error approving sponsor. Please try again.');
          });
      },
  
      navigateTo(pageName) {
        this.$router.push({ name: pageName });
      },
  
      logout() {
        this.$router.push({ name: 'LogoutPage' });
        return;
      }
    }
  };
  </script>