import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '@/views/HomePage.vue';
import LoginPage from '@/views/LogInPage.vue';
import SignupPage from '@/views/SignupPage.vue';
import LogoutPage from '@/views/LogoutPage.vue';
import SponsorRegistration from '@/views/SponsorRegistration.vue';
import InfluencerRegistration from '@/views/InfluencerRegistration.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import AdminViewUsers from '@/views/AdminViewUsers.vue';
import AdminViewInfluencers from '@/views/AdminViewInfluencers.vue';
import AdminViewSponsors from '@/views/AdminViewSponsors.vue';
import AdminViewCampaigns from '@/views/AdminViewCampaigns.vue';
import AdminViewAdrequests from '@/views/AdminViewAdrequests.vue';
import SponsorDashboard from '@/views/SponsorDashboard.vue';
import CreateCampaign from '@/views/CreateCampaign.vue';
import CreateAdrequest from '@/views/CreateAdrequest.vue';
import FindInfluencers from '@/views/FindInfluencers.vue';
import ActionInfluencer from '@/views/ActionInfluencer.vue';
import UpdateCampaign from '@/views/UpdateCampaign.vue';
import UpdateAdRequest from '@/views/UpdateAdRequest.vue';
import InfluencerDashboard from '@/views/InfluencerDashboard.vue';
import ActionAdRequest from '@/views/ActionAdRequest.vue';
import UpdateInfluencerProfile from '@/views/UpdateInfluencerProfile.vue';
import FindCampaigns from '@/views/FindCampaigns.vue';
import FindAdRequests from '@/views/FindAdRequests.vue';

const routes = [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/login',
      name: 'LoginPage',
      component: LoginPage,
    },
    {
      path: '/signup',
      name: 'SignupPage',
      component: SignupPage,
    },
    {
      path: '/logout',
      name: 'LogoutPage',
      component: LogoutPage,
    },
    {
      path: '/sponsor/register',
      name: 'SponsorRegistration',
      component: SponsorRegistration,
    },
    {
      path: '/influencer/register',
      name: 'InfluencerRegistration',
      component: InfluencerRegistration,
    },
  {
      path: '/admindashboard',
      name: 'AdminDashboard',
      component: AdminDashboard,
    },
    {
      path: '/admin/users',
      name: 'AdminViewUsers',
      component: AdminViewUsers,
    },
    {
      path: '/admin/influencers',
      name: 'AdminViewInfluencers',
      component: AdminViewInfluencers,
    },
    {
      path: '/admin/sponsors',
      name: 'AdminViewSponsors',
      component: AdminViewSponsors,
    },
    {
      path: '/admin/campaigns',
      name: 'AdminViewCampaigns',
      component: AdminViewCampaigns,
    },
      {
      path: '/admin/adrequests',
      name: 'AdminViewAdrequests',
      component: AdminViewAdrequests,
    },
    {
      path: '/sponsordashboard',
      name: 'SponsorDashboard',
      component: SponsorDashboard,
    },
    {
      path: '/sponsor/create-campaign',
      name: 'CreateCampaign',
      component: CreateCampaign,
    },
    {
      path: '/sponsor/create-ad-request',
      name: 'CreateAdrequest',
      component: CreateAdrequest,
    },
    {
      path: '/sponsor/find-influencers',
      name: 'FindInfluencers',
      component: FindInfluencers,
    },
    {
      path: '/sponsor/action-influencer/:influencerId',
      name: 'ActionInfluencer',
      component: ActionInfluencer,
      props: true,
    },
    {
      path: '/sponsor/update-campaign/:campaignId',
      name: 'UpdateCampaign',
      component: UpdateCampaign,
      props: true,
    },
    {
      path: '/sponsor/update-ad-request/:adrequestId',
      name: 'UpdateAdRequest',
      component: UpdateAdRequest,
      props: true,
    },
    {
      path: '/influencerdashboard',
      name: 'InfluencerDashboard',
      component: InfluencerDashboard,
    },
    {
      path: '/influencer/action-ad-request/:adrequestId',
      name: 'ActionAdRequest',
      component: ActionAdRequest,
      props: true,
    },
    {
      path: '/influencer/update-profile',
      name: 'UpdateInfluencerProfile',
      component: UpdateInfluencerProfile,
    },
    {
      path: '/influencer/find-campaigns',
      name: 'FindCampaigns',
      component: FindCampaigns,
    },
    {
      path: '/influencer/find-ad-requests/:campaign_id',
      name: 'FindAdRequests',
      component: FindAdRequests,
      props: true
    },
  ];

const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
  export default router;