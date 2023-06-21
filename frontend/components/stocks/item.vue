<template>
    <nuxt-link class="stock" :to="{ name: 'stocks-id', params: { id: stock.id } }">
        <img :src="stock.picture" />
    </nuxt-link>
</template>
<script setup>
const { stock } = defineProps({ stock: Object });

</script>
<style lang="scss">
.stock {
    width: 100%;
    aspect-ratio: 2;
    display: flex;
    overflow: hidden;
    border-radius: 15px;
    background-color: white;

    img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}
</style>