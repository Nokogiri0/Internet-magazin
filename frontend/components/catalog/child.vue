<template>
    <Catalog :catalog="childrens" :text="catalog.name" />
</template>
<script setup>
import { CategoriesService } from "@/client";
const { id } = defineProps({
    id: {
        type: String,
        required: true,
    },
});
const childrens = await CategoriesService.getCategoryInfoApiV1CategoriesCategoryIdSubcategoriesGet(id)
const catalog =
    await CategoriesService.getCategoryInfoApiV1CategoriesCategoryIdGet(id);
</script>
