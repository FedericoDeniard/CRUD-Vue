<template>
  <div class="container mt-5">
    <div class="card p-2">
      <div class="card-header">
        <h4>Edit User</h4>
      </div>
      <ul v-if="errors.length > 0" class="text-dark mb-3 bg-danger card mt-2">
        <li v-for="(error, index) in errors" :key="index" class="">
          {{ error }}
        </li>
      </ul>
      <ul
        v-if="successMessages.length > 0"
        class="text-success mb-3 bg-success card mt-2"
      >
        <li
          v-for="(message, index) in successMessages"
          :key="index"
          class="text-light"
        >
          {{ message }}
        </li>
      </ul>
      <div class="card-body">
        <div class="mb-3">
          <label for="" class="form-label">Username*</label>
          <input
            type="text"
            class="form-control"
            v-model="model.user.user"
            placeholder="username"
          />
        </div>
        <div class="mb-3">
          <label class="form-label">Roles*</label>
          <div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="admin"
                v-model="model.user.is_user_admin"
              />
              <label class="form-check-label" for="admin">Admin</label>
            </div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="manager"
                v-model="model.user.is_user_manager"
              />
              <label class="form-check-label" for="manager">Manager</label>
            </div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="tester"
                v-model="model.user.is_user_tester"
              />
              <label class="form-check-label" for="tester">Tester</label>
            </div>
          </div>
        </div>
        <div class="mb-3">
          <label for="timezone" class="form-label">Timezone*</label>
          <select
            id="timezone"
            class="form-select"
            v-model="model.user.user_timezone"
          >
            <option v-for="tz in timezones" :key="tz" :value="tz">
              {{ tz }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label class="form-label">Active*</label>
          <div>
            <div class="form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="is_active"
                v-model="model.user.is_user_active"
              />
              <label class="form-check-label" for="is_active">Active</label>
            </div>
          </div>
        </div>
        <div class="mb-3">
          <button
            type="button"
            class="btn btn-primary"
            @click="openConfirmationModal"
            :disabled="!formCompleted || !checkPasswords()"
          >
            Update
          </button>
        </div>
      </div>
    </div>

    <Modal
      v-if="showModal"
      title="Confirm Update"
      body="Are you sure you want to save these changes?"
      confirmText="Confirm"
      :isVisible="showModal"
      @close="showModal = false"
      @confirm="update"
    />
  </div>
</template>

<script>
import Modal from '../../components/Modal.vue'
import moment from 'moment-timezone'

export default {
  name: 'EdtUser',
  components: {
    Modal,
  },
  data() {
    return {
      model: {
        user: {
          user: '',
          password: '',
          repeatPassword: '',
          is_user_admin: null,
          is_user_manager: null,
          is_user_tester: null,
          user_timezone: '',
          is_user_active: null,
          created_at: null,
        },
      },
      errors: [],
      successMessages: [],
      showPassword: false,
      showModal: false,
      timezones: moment.tz.names(),
    }
  },
  computed: {
    formCompleted() {
      return (
        this.model.user.user &&
        this.model.user.user_timezone &&
        (this.model.user.is_user_admin ||
          this.model.user.is_user_manager ||
          this.model.user.is_user_tester)
      )
    },
  },
  mounted() {
    this.getUserData(this.$route.params.id)
  },
  methods: {
    openConfirmationModal() {
      this.showModal = true
    },
    async update() {
      this.errors = []
      this.successMessages = []
      try {
        const editedUser = await fetch(
          import.meta.env.VITE_API_URL +
            '/users/' +
            this.$route.params.id +
            '/edit',
          {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.model.user),
          },
        )

        if (!editedUser.ok) {
          const res = await editedUser.json()
          this.errors.push(res.error)
          return
        }
        this.errors = []
        const res = await editedUser.json()

        this.successMessages.push(res.data.message)
      } catch (error) {
        this.errors.push(error.message)
      } finally {
        this.showModal = false
      }
    },
    checkPasswords() {
      return this.model.user.password === this.model.user.repeatPassword
    },
    async getUserData(id) {
      try {
        const user = await fetch(import.meta.env.VITE_API_URL + '/user/' + id, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })

        if (!user.ok) {
          if (user.status === 404) {
            alert('User not found')
            this.$router.push('/')
            return
          }
          const res = await user.json()
          this.errors.push(res.error)
          return
        }
        this.errors = []
        const res = await user.json()

        this.model.user.user = res.data.username || ''
        this.model.user.password = res.data.password || ''
        this.model.user.repeatPassword = res.data.password || ''
        this.model.user.is_user_admin = res.data.roles.includes('admin')
        this.model.user.is_user_manager = res.data.roles.includes('manager')
        this.model.user.is_user_tester = res.data.roles.includes('tester')
        this.model.user.user_timezone = res.data.preferences.timezone || ''
        this.model.user.is_user_active = res.data.active
        this.model.user.created_at = new Date(
          res.data.created_ts * 1000,
        ).toISOString()
      } catch (error) {
        this.errors.push(error.message)
      }
    },
  },
}
</script>
