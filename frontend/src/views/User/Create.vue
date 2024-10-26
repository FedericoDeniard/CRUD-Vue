<template>
  <div class="container mt-5">
    <div class="card p-2">
      <div class="card-header">
        <h4>Add User</h4>
      </div>
      <ul v-if="errors.length > 0" class="text-dark mb-3 bg-danger card mt-2">
        <li v-for="(error, index) in errors" :key="index">
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
          <label for="password" class="form-label">Password*</label>
          <div class="input-group">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              class="form-control"
              v-model="model.user.password"
              placeholder="password"
            />
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="showPassword = !showPassword"
            >
              <span v-if="!showPassword">Show</span>
              <span v-else>Hide</span>
            </button>
          </div>
        </div>
        <div class="mb-3">
          <label for="repeat-password" class="form-label"
            >Repeat Password*</label
          >
          <div class="input-group">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="repeat-password"
              class="form-control"
              v-model="model.user.repeatPassword"
              placeholder="password"
            />
            <button
              class="btn btn-outline-secondary"
              type="button"
              @click="showPassword = !showPassword"
            >
              <span v-if="!showPassword">Show</span>
              <span v-else>Hide</span>
            </button>
          </div>
        </div>
        <div v-if="!checkPasswords()" class="text-danger mb-3">
          Passwords do not match
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
          <label class="form-label">Timezone*</label>
          <select v-model="model.user.user_timezone" class="form-select">
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
      </div>
      <div class="mb-3">
        <button
          type="button"
          class="btn btn-primary"
          @click="openConfirmationModal"
          :disabled="!formCompleted || !checkPasswords()"
        >
          Save
        </button>
      </div>
    </div>
  </div>
  <Modal
    v-if="showModal"
    title="Confirm User Creation"
    body="Are you sure you want to create this user?"
    confirmText="Confirm"
    :isVisible="showModal"
    @close="showModal = false"
    @confirm="save"
  />
</template>

<script>
import Modal from '../../components/Modal.vue'
import moment from 'moment-timezone'

export default {
  name: 'AddUser',
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
          is_user_admin: false,
          is_user_manager: false,
          is_user_tester: false,
          user_timezone: '',
          is_user_active: true,
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
        this.model.user.password &&
        this.model.user.repeatPassword &&
        this.model.user.user_timezone
      )
    },
  },
  methods: {
    openConfirmationModal() {
      this.showModal = true
    },
    async save() {
      this.errors = []
      this.successMessages = []
      this.model.user.created_at = new Date().toISOString()
      try {
        const newUser = await fetch(
          import.meta.env.VITE_API_URL + '/new_user',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.model.user),
          },
        )

        if (!newUser.ok) {
          const res = await newUser.json()
          this.errors.push(res.data.error)
          return
        }

        const res = await newUser.json()
        this.successMessages.push(res.data.message)

        this.model.user = {
          user: '',
          password: '',
          repeatPassword: '',
          is_user_admin: false,
          is_user_manager: false,
          is_user_tester: false,
          user_timezone: '',
          is_user_active: true,
          created_at: null,
        }
      } catch (error) {
        this.errors.push(error.message)
      } finally {
        this.showModal = false
      }
    },
    checkPasswords() {
      return this.model.user.password === this.model.user.repeatPassword
    },
  },
}
</script>
