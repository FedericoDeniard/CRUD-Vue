<template>
    <div class="modal fade" tabindex="-1" :class="{ show: isVisible }"
        :style="{ display: isVisible ? 'block' : 'none' }" aria-labelledby="modalLabel" aria-hidden="!isVisible">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="modalLabel">{{ title }}</h5>
                    <button type="button" class="btn-close" @click="$emit('close')" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <p>{{ body }}</p>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="$emit('close')">Close</button>
                    <button type="button" class="btn btn-primary" @click="$emit('confirm')">{{ confirmText }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
            required: true
        },
        body: {
            type: String,
            required: true
        },
        confirmText: {
            type: String,
            default: 'Confirm'
        },
        isVisible: {
            type: Boolean,
            required: true
        }
    }
}
</script>

<style scoped>
.modal.show {
    display: block;
}
</style>
