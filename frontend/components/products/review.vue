<template>
    <div class="review">{{ review }}</div>
</template>
<script setup>
const { review } = defineProps({
    review: Object,
})
</script>