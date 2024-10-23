<template>
  <div class="container mt-5">
    <div class="card">
      <div class="card-header">
        <h4>
          Users
          <RouterLink to="/users/create" class="btn btn-primary float-end">
            Add User
          </RouterLink>
        </h4>
      </div>
      <div class="card-body">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Username</th>
              <th>Roles</th>
              <th>Timezone</th>
              <th>Active</th>
              <th>Created</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody v-if="users.length > 0">
            <tr v-for="(user, index) in users" :key="index">
              <td class="align-middle">{{ user.username }}</td>
              <td>
                <ul v-for="role in user.roles" :key="role" class="list-group">
                  <li class="list-group-item border-0">{{ role }}</li>
                </ul>
              </td>
              <td class="align-middle">{{ user.preferences.timezone }}</td>
              <td class="align-middle">{{ user.active }}</td>
              <td class="align-middle">
                {{ new Date(user.created_ts).toISOString() }}
              </td>
              <td class="align-middle text-center">
                <RouterLink
                  :to="{ path: '/users/' + user._id + '/edit' }"
                  class="btn btn-success me-1"
                >
                  Edit
                </RouterLink>
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="openConfirmationModal(user._id, user.username)"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="6" class="text-center">
                <div class="spinner-border" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <Modal
      v-if="showModal"
      title="Confirm Delete"
      :body="`Are you sure you want to delete this user? ${userToDelete}`"
      confirmText="Delete"
      :isVisible="showModal"
      @close="handleClose"
      @confirm="deleteUser"
    />
  </div>
</template>

<script>
import Modal from '../components/Modal.vue'

export default {
  name: 'Users',
  components: {
    Modal,
  },
  data() {
    return {
      users: [],
      showModal: false,
      userIdToDelete: null,
      userToDelete: null,
    }
  },
  mounted() {
    this.getUsers()
  },
  methods: {
    async getUsers() {
      try {
        const url = import.meta.env.VITE_API_URL + '/users'
        const response = await fetch(url)
        const data = await response.json()
        this.users = data
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    },
    openConfirmationModal(userId, username) {
      this.userIdToDelete = userId
      this.userToDelete = username
      this.showModal = true
    },
    async deleteUser() {
      if (!this.userIdToDelete) return

      try {
        const url = `${import.meta.env.VITE_API_URL}/delete_user/${this.userIdToDelete}`
        await fetch(url, {
          method: 'DELETE',
        })
        this.users = this.users.filter(user => user._id !== this.userIdToDelete)
        this.showModal = false
        this.userIdToDelete = null
        this.userToDelete = null
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    },
    handleClose() {
      this.showModal = false
      this.userIdToDelete = null
      this.userToDelete = null
    },
  },
}
</script>
