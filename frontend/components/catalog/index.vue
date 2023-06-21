<template>
    <div class="categories-container" v-if="catalog?.length">
        <div class="headline">{{ text }}</div>
        <div class="categories-items-containr">
            <CatalogItem v-for="category in catalog" :category="category" :key="category.id" />
        </div>
    </div>
</template>
<script setup>
const { catalog, text } = defineProps({
    catalog: Array,
    text: {
        type: String,
        default: "Доступные категории",
    },
});
</script>
<style lang="scss">
.categories-container {
    display: flex;
    flex-direction: column;
    gap: 10px;


    .headline {
        font-size: 20px;
        font-weight: bold;
    }

    .categories-items-containr {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px;
    }
}
</style>
