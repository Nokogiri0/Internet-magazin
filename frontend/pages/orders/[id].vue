<template>
    <div class="order-page">
        <div class="head-line">
            <div class="title">Заказ {{ id }}</div>
            <div class="date">{{ dataAndTime }}</div>
        </div>
        <div class="order-products">
            <ProductsItem
                v-for="product in order.order_products"
                :key="product.id"
                :product="product"
            />
        </div>
    </div>
</template>
<script setup>
import { OrdersService } from "~~/client";
const { id } = useRoute().params;
const order = await OrdersService.getOrderApiV1OrdersOrderIdGet(id);
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
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }
}
</style>
