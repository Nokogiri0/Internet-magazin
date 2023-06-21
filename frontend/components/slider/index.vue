<template>
    <Swiper :modules="[EffectCreative, Autoplay, Pagination]" :grabCursor="true" :effect="'creative'" :creativeEffect="{
        prev: {
            shadow: true,
            translate: [0, 0, -400],
        },
        next: {
            translate: ['100%', 0, 0],
        },

    }" :autoplay="{
    delay: 5500,
    disableOnInteraction: false,
}" :pagination="{
    clickable: true,
}">

        <SwiperSlide :slide="slide" v-for="slide in slides" :key="slide.id">
            <SliderItem :slide="slide" />
        </SwiperSlide>
    </Swiper>
</template>
<script setup>
import { EffectCreative, Autoplay, Pagination } from 'swiper';
import { Service } from '@/client';
const slides = await Service.getAllSlidesApiV1SliderGet();
</script>
<style lang="scss">
.swiper {
    user-select: none;
}
</style>