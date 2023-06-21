<template>
    <nuxt-link class="category hover:shadow-lg transition-shadow " :to="link">
        <img :src="category.picture" alt="category" />

        <span class="category-text font-medium ">{{ category.name }}</span>
    </nuxt-link>
</template>
<script setup>
const { category } = defineProps({
    category: Object,
});
const link = computed(() => {
    return { name: category.children.length !== 0 ? 'category-id' : 'category-id-products', params: { id: category.id } }
});
</script>
<style lang="scss">
.category {
    background-color: $secondary-bg;
    border-radius: 10px;
    overflow: hidden;
    position: relative;
    width: 100%;


    .category-text {
        position: absolute;
        top: 20px;
        left: 0;
        width: 100%;
        padding: 0px 10px;
        text-align: center;

    }

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

}
</style>
