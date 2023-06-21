<template>
    <div class="review">
        <div class="line">
            <div class="date">
                {{ review.time_created }}
            </div>
            <div class="rating">{{ review.rating }} / 10</div>
        </div>

        <div class="text">
            {{ review.description }}
        </div>
        <div class="buttons" v-if="user_is_owner">
            <button class="button" @click="edit">Редактировать</button>
            <button class="button" @click="remove">Удалить</button>
        </div>
    </div>
</template>
<script setup>
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { Service } from "~~/client";
const authStore = useAuthStore();
const { userData, logined } = storeToRefs(authStore);
const user_is_owner = computed(() => {
    if (!logined.value) return false;
    return userData.value?.id === review.user_id;
});
const emit = defineEmits(["edit", "remove"]);
const remove = async () => {
    await Service.deleteReviewApiV1ReviewsReviewIdDelete(review.id);
    emit("remove");
};

const { review } = defineProps({
    review: Object,
});
</script>
<style lang="scss" scoped>
.review {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    background-color: $secondary-bg;
    border-radius: 20px;
    margin-bottom: 10px;
    .line {
        display: flex;
        justify-content: space-between;
        .rating {
            font-size: large;
            font-weight: bold;
        }
        .date {
            color: $secondary-text;
        }
    }
    .text {
        font-size: medium;
        word-break: break-all;
    }

    .buttons {
        display: flex;

        gap: 10px;
        .button {
            background-color: $primary-bg;
            border: none;
            border-radius: 10px;
            padding: 5px 10px;
            color: $primary-text;
            font-size: medium;
            font-weight: bold;
            cursor: pointer;
            flex-grow: 1;

            &:hover {
                background-color: $tertiary-bg;
            }
        }
    }
}
</style>
