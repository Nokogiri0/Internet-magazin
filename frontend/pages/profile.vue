<template>
    <div class="profile">
        <div class="profile-editor" v-if="userData">
            <div class="avatar-contaner">
                <Upload
                    action="/api/v1/users/me/avatar"
                    method="PUT"
                    :on-success="handleAvatarSuccess"
                    :imageUrl="userData.picture"
                    border-radius="50%"
                    class="avatar-uploader"
                    name="userPicture"
                />
                <div
                    :class="[
                        'delete-button-contaner',
                        { active: userData.picture },
                    ]"
                >
                    <div
                        class="delete-button"
                        @[userData.picture&&`click`]="
                            showDeleteAvatarModal = true
                        "
                    >
                        <Icon name="material-symbols:close" />
                    </div>
                </div>
                <ModalDialog
                    :active="showDeleteAvatarModal"
                    @close="showDeleteAvatarModal = false"
                    :buttons="[
                        {
                            text: 'Удалить',
                            type: 'danger',
                            onClick: deleteUserAvatar,
                        },
                        {
                            text: 'Отмена',
                            type: 'primary',
                            onClick: () => {
                                showDeleteAvatarModal = false;
                            },
                        },
                    ]"
                >
                    <template #content>
                        <div class="warning-modal">
                            <div class="warning-modal-headline">
                                Вы уверены, что хотите удалить аватар?
                            </div>
                        </div>
                    </template>
                </ModalDialog>
            </div>
            <div class="profile-form-fields">
                <AppInput
                    v-model="firstName"
                    label="Имя"
                    :max-length="MAX_FIRSTNAME_LENGTH"
                    show-word-limit
                />
                <AppInput
                    v-model="lastName"
                    label="Фамилия"
                    :max-length="MAX_LASTNAME_LENGTH"
                    show-word-limit
                />
                <AppInput v-model="phone" label="Телефон" />
                <el-tooltip :visible="usernameAlreadyExists" placement="top">
                    <template #content>
                        <span>Этот никнейм занят</span>
                    </template>
                    <AppInput
                        v-model="username"
                        label="Никнейм"
                        :max-length="MAX_LOGIN_LENGTH"
                        :min-length="MIN_LOGIN_LENGTH"
                        show-word-limit
                        :error="usernameAlreadyExists || usernameIsShort"
                        :formatter="formatUsername"
                    />
                </el-tooltip>
            </div>

            <AppButton @click="saveProfile" :active="buttonActive">
                Сохранить
            </AppButton>
            <AppButton active @click="goToOrders"> Мои заказы </AppButton>
            <AppButton active @click="logout"> Выйти </AppButton>
        </div>
    </div>
</template>
<script setup>
import { CategoriesService, Service } from "~~/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
useHead({ title: "Профиль" });
definePageMeta({
    middleware: ["auth"],
});
const runtimeConfig = useRuntimeConfig();
const {
    MAX_FIRSTNAME_LENGTH,
    MAX_LASTNAME_LENGTH,
    MAX_LOGIN_LENGTH,
    MIN_LOGIN_LENGTH,
} = runtimeConfig.public;
const { $toast } = useNuxtApp();
const authStore = useAuthStore();
const { userData } = storeToRefs(authStore);
const firstName = ref(userData.value.first_name || "");
const lastName = ref(userData.value.last_name || "");
const username = ref(userData.value.username);
const phone = ref(userData.value.phone || "");
const usernameAlreadyExists = ref(false);
watch(username, async (newUsername) => {
    if (newUsername !== userData.value.username) {
        usernameAlreadyExists.value =
            await CategoriesService.checkUsernameExistsApiV1UsersUsernameExistsGet(
                newUsername
            );
    } else {
        usernameAlreadyExists.value = false;
    }
});
const formatUsername = (value) => {
    return value.replace(/[^a-zA-Z0-9_]/g, "");
};
const showDeleteAvatarModal = ref(false);
const valuesChanged = computed(() => {
    return (
        firstName.value !== userData.value.first_name ||
        lastName.value !== userData.value.last_name ||
        username.value !== userData.value.username ||
        phone.value !== userData.value.phone
    );
});
const usernameIsShort = computed(() => {
    return username.value.length < MIN_LOGIN_LENGTH;
});
const valuesCorrect = computed(() => {
    return (
        firstName.value.length <= MAX_FIRSTNAME_LENGTH &&
        lastName.value.length <= MAX_LASTNAME_LENGTH &&
        !usernameIsShort.value
    );
});
const buttonActive = computed(() => {
    return (
        valuesChanged.value &&
        valuesCorrect.value &&
        !usernameAlreadyExists.value
    );
});
const phoneIsCorrect = computed(() => {
    const regex =
        /(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]‌​)\s*)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)([2-9]1[02-9]‌​|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})\s*(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+)\s*)?$/;
    return regex.test(phone.value);
});
const goToOrders = () => {
    navigateTo("/orders");
};
const saveProfile = async () => {
    if (buttonActive.value) {
        if (!phoneIsCorrect.value) {
            $toast.error("Некорректный номер телефона");
            return;
        }
        try {
            userData.value = await Service.updateUserDataApiV1UsersMePut({
                first_name: firstName.value,
                last_name: lastName.value,
                username: username.value,
                phone: phone.value,
            });
        } catch (error) {
            $toast.error(HandleOpenApiError(error).message);
        }
    }
};
const handleAvatarSuccess = (response, uploadFile) => {
    userData.value.picture = response.picture;
};
const deleteUserAvatar = async () => {
    userData.value = await Service.updateUserAvatarApiV1UsersMeAvatarPut();
    showDeleteAvatarModal.value = false;
};
const logout = () => {
    useRouter().push("/");
    authStore.logoutRequest();
};
</script>

<style lang="scss" scoped>
.profile {
    @include flex-center;

    @include sm {
        padding: 2rem;
    }

    .profile-editor {
        max-width: 400px;
        width: 100%;
        display: flex;
        gap: 10px;
        flex-direction: column;
        @include flex-center;

        .avatar-contaner {
            @include flex-center;
            gap: 10px;
            position: relative;
            max-width: 150px;
            aspect-ratio: 1;
            width: 100%;

            .avatar-uploader {
                width: 100%;
                height: 100%;
            }

            .delete-button-contaner {
                position: absolute;
                top: 0;
                bottom: 0;
                left: calc(103%);
                @include flex-center;
                opacity: 0;

                &.active {
                    opacity: 1;
                }

                .delete-button {
                    @include flex-center;
                    border-radius: 50%;
                    cursor: pointer;
                    background-color: white;
                    padding: 10px;
                    height: min-content;

                    @include lg {
                        &:hover {
                            background-color: white;
                        }
                    }
                }
            }
        }

        .profile-form-fields {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 100%;
        }
    }
}
</style>
