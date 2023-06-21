<template>
    <div class="stocks-slider">
        <span class="stocks-special-for-you">Специально для вас</span>
        <Swiper :modules="[EffectCreative, Pagination]" :grabCursor="true" :autoplay="{
            delay: 5500,
            disableOnInteraction: false,
        }" :slidesPerView="4" :spaceBetween="10">
            <SwiperSlide v-for="stock in stocks" :key="stock.id">
                <StocksItem :stock="stock" />
            </SwiperSlide>
        </Swiper>
    </div>
</template>
<script setup>
import { EffectCreative, Autoplay, Pagination } from 'swiper';
import { Service } from '~~/client';
const stocks = await Service.getOpenStocksApiV1StocksGet(1);

</script>
<style lang="scss" scoped>
.stocks-slider {
    gap: 10px;

    .stocks-special-for-you {
        margin-bottom: 20px;
        font-weight: bold;
    }
}
</style>