<template>
    <div class="index-page">
        <Slider />
        <Stocks class="index-page-stocks" />
        <CatalogParent class="index-page-categories" />
    </div>
</template>
<script setup></script>
<style lang="scss">
.index-page {

    .index-page-stocks {
        margin-top: 10px;
    }

    .index-page-categories {
        margin-top: 20px;
    }
}
</style>
