<template>
    <a class="slide" :href="slide.url" target="_blank">
        <img :src="slide.picture" alt="slide" />
    </a>
</template>
<script setup>
const { slide } = defineProps({ slide: Object });
</script>
<style lang="scss">
.slide {
    width: 100%;
    aspect-ratio: 3;
    display: flex;
    overflow: hidden;
    border-radius: 10px;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}
</style>