<template>
    <div class="orders">
        <Order v-for="order in orders" :order="order" :key="order.id" />
    </div>
</template>
<script setup>
import { OrdersService } from "~~/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
if (!logined.value) {
    navigateTo({ name: "login" });
}
const orders = ref([]);
const page = ref(1);
const getNextPage = async () => {
    const newOrders = await OrdersService.getMyOrdersApiV1OrdersMyGet(
        page.value
    );
    orders.value = [...orders.value, ...newOrders];
    page.value++;
};
getNextPage();
</script>
<style lang="scss" scoped>
.orders {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
