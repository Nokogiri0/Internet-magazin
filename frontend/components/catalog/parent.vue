<template>
    <Catalog :catalog="catalog" id="parent-categories" />
</template>
<script setup>
import { CategoriesService } from "@/client";
const catalog = await CategoriesService.getCategoriesApiV1CategoriesGet();
</script>
