<template>
    <div class="index-page">
        <Catalog :catalog="category.children" :text="category.name" />
    </div>
</template>
<script setup>
import { CategoriesService } from '~~/client';
const route = useRoute();
const categoryId = computed(() => route.params.id || 1);
const category = await CategoriesService.getCategoryInfoApiV1CategoriesCategoryIdSubcategoriesGet(categoryId.value);
if (category.children.length == 0) {
    const router = useRouter();
    router.push({ name: 'category-id-products', params: { id: categoryId.value } });
}

</script>
