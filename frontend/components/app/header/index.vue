<template>
    <header>
        <nuxt-link to="/" class="header-button logo">
            <Icon name="ph:house" />
        </nuxt-link>
        <nuxt-link to="/markets" class="header-button">
            <Icon name="fluent:building-shop-24-filled" />
            <span>Магазины</span>
        </nuxt-link>
        <nuxt-link to="/#parent-categories" class="header-button">
            <Icon name="ph:github-logo"></Icon>
            <span>Категории</span>
        </nuxt-link>
        <nuxt-link to="/profile" class="header-button" v-if="logined">
            <Icon name="mi:user" />
            <span>Профиль</span>
        </nuxt-link>
        <NuxtLink class="header-button" v-else to="/login">
            <Icon name="material-symbols:login" />
            <span>Войти в аккаунт</span>
        </NuxtLink>
        <nuxt-link to="/cart" class="header-button cart">
            <div class="icon">
                <Icon name="mi:shopping-cart" />
                <div class="count">
                    {{ cartStore.count }}
                </div>
            </div>
            <span>Корзина</span>
        </nuxt-link>
    </header>
</template>
<script setup>
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { useCartStore } from "@/stores/cart";
const cartStore = useCartStore();
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
</script>
<style lang="scss">
header {
    display: flex;
    gap: 20px;
    padding: 20px;

    .header-button {
        @include flex-center;
        gap: 5px;
        transition: color 0.005s;

        &.cart {
            padding: 0 10px;

            .icon {
                position: relative;

                .count {
                    position: absolute;
                    @include flex-center;
                    right: 80%;
                    bottom: 100%;
                    font-size: 10px;
                    background-color: $accent-2;
                    padding: 3px;
                    min-width: 20px;
                    border-radius: 10px;
                }
            }
        }

        &.logo {
            margin-right: auto;
        }

        &:hover {
            color: $accent-1;
        }
    }
}
</style>
