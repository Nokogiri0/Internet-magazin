<template>
    <div class="order-page">
        <div class="head-line">
            <div class="title">Заказ {{ id }}</div>
            <div class="date">{{ dataAndTime }}</div>
        </div>
        <div class="order-products">
            <ProductsItem
                v-for="order_product in order.order_products"
                :key="order_product.id"
                :product="order_product.product"
            />
        </div>
    </div>
</template>
<script setup>
const { order } = defineProps({
    order: {
        type: String,
        required: true,
    },
});

const dataAndTime = computed(() => {
    const date = new Date(order.time_created);
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const hours = date.getHours().toString().padStart(2, "0");
    const minutes = date.getMinutes().toString().padStart(2, "0");
    return `${day}.${month}.${year} ${hours}:${minutes}`;
});
</script>
<style lang="scss" scoped>
.order-page {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    .head-line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        .title {
            font-size: 24px;
            font-weight: 500;
        }
        .date {
            font-size: 16px;
            color: #a0a0a0;
        }
    }

    .order-products {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
    }
}
</style>
