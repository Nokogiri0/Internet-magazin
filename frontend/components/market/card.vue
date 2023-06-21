<template>
    <div class="market-card">
        <div class="marker-image">
            <Icon name="fluent:building-shop-24-filled" />
        </div>
        <div class="market-info">
            <div class="market-address">{{ market.address }}</div>
            <div class="description">
                {{ market.phone }}
            </div>
            <div class="work-time">
                <div class="time-item">
                    <span>Пн-Пт: {{ market.weekday_hours }}</span>
                </div>
                <div class="time-item">
                    <span>Сб-Вс: {{ market.weekend_hours }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
const { market } = defineProps({
    market: Object,
});
</script>
<style lang="scss" scoped>
.market-card {
    width: 100%;
    height: 100%;
    background-color: #fff;
    border-radius: 20px;
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
    display: grid;
    grid-template-columns: 100px 1fr;
    padding: 10px;
    gap: 10px;
    .marker-image {
        background-color: $accent-5;
        aspect-ratio: 1;
        @include flex-center;
        border-radius: 10px;

        svg {
            font-size: 50px;
            color: $accent-1;
        }
    }
    .market-info {
        display: flex;
        flex-direction: column;
        gap: 5px;

        .market-address {
            font-size: large;
            font-weight: bolder;
        }
        .description {
            font-size: medium;
        }
        .work-time {
            display: flex;
            margin-top: auto;
            justify-content: space-between;
            gap: 5px;
            .time-item {
                display: flex;
                gap: 5px;
                align-items: center;
                svg {
                    color: $accent-5;
                }
            }
        }
    }
}
</style>
