<template>
    <div class="markets">
        <MarketCard :market="market" v-for="market in markets" />
    </div>
</template>
<script setup>
import { Service } from "~~/client";
const markets = await Service.getMarketsApiV1MarketsGet();
</script>
<style lang="scss" scoped>
.markets {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
}
</style>
