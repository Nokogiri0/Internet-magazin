<template>
    <div class="login-form-container">
        <div class="form-container">
            <div class="form">
                <div class="headline">
                    <span>{{ register ? "Регистрация" : "Вход" }}</span>
                </div>
                {{ message }}
                <template v-if="register">
                    <el-input v-model="name" placeholder="Имя"></el-input>
                    <el-input
                        v-model="last_name"
                        placeholder="Фамилия"
                    ></el-input>
                </template>
                <el-input v-model="login" placeholder="Логин"></el-input>
                <el-input
                    v-model="password"
                    placeholder="Пароль"
                    type="password"
                    show-password
                ></el-input>
                <div
                    :class="['login-button hover:shadow-lg transition-shadow']"
                    @click="loginHandler"
                >
                    <span>{{ register ? "Зарегистрироваться" : "Войти" }}</span>
                </div>
                <nuxt-link :to="register ? '/login' : '/register'">
                    {{ register ? "Уже есть аккаунт?" : "Нет аккаунта?" }}
                </nuxt-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useAuthStore } from "~~/stores/auth";
import { HandleOpenApiError } from "@/composables/errors";
const authStore = useAuthStore();
const { register } = defineProps({
    register: { type: Boolean, default: false },
});

const login = ref("");
const name = ref("");
const last_name = ref("");
const password = ref("");
const runtimeConfig = useRuntimeConfig();

const {
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MAX_USERNAME_LENGTH,
    MIN_USERNAME_LENGTH,
    MAX_FIRSTNAME_LENGTH,
    MAX_LASTNAME_LENGTH,
} = runtimeConfig.public;

const message = ref("");
const messageIsShowed = ref(false);
const messageTimer = ref(null);
const messageNestedTimer = ref(null);
const isErrorMessage = ref(false);
const showMessage = (messageText, isError) => {
    if (messageTimer.value) {
        clearTimeout(messageTimer.value);
        if (messageNestedTimer.value) {
            clearTimeout(messageNestedTimer.value);
        }
    }
    isErrorMessage.value = isError;
    message.value = messageText;
    messageIsShowed.value = true;
    messageTimer.value = setTimeout(() => {
        messageIsShowed.value = false;
        messageNestedTimer.value = setTimeout(() => {
            message.value = "";
        }, 500);
    }, 3000 * (isError ? 2 : 1));
};

const loginHandler = async () => {
    console.log(
        MIN_PASSWORD_LENGTH,
        MAX_PASSWORD_LENGTH,
        MAX_USERNAME_LENGTH,
        MIN_USERNAME_LENGTH,
        MAX_FIRSTNAME_LENGTH,
        MAX_LASTNAME_LENGTH
    );
    if (login.value.length < MIN_USERNAME_LENGTH) {
        showMessage(`Логин должен быть не менее ${MIN_LOGIN_LENGTH} символов`);
        return;
    }
    if (password.value.length < MIN_PASSWORD_LENGTH) {
        showMessage(
            `Пароль должен быть не менее ${MIN_PASSWORD_LENGTH} символов`
        );
        return;
    }
    if (password.value.length > MAX_PASSWORD_LENGTH) {
        showMessage(
            `Пароль должен быть не более ${MAX_PASSWORD_LENGTH} символов`
        );
        return;
    }
    if (login.value.length > MAX_USERNAME_LENGTH) {
        showMessage(`Логин должен быть не более ${MAX_LOGIN_LENGTH} символов`);
        return;
    }
    const error = register
        ? await authStore.registerRequest(
              login.value,
              password.value,
              name.value,
              last_name.value
          )
        : await authStore.loginRequest(login.value, password.value);
    if (error) {
        showMessage(HandleOpenApiError(error).message);
        return;
    }
    const router = useRouter();
    router.push({ name: "profile" });
};
const validateLogin = (value) => {
    const regex = /[^a-zA-Z0-9_]/g;
    if (regex.test(value)) {
        showMessage(
            "Логин может содержать только латинские буквы, цифры и нижнее подчеркивание"
        );
    }
    return value.replace(regex, "");
};
</script>
<style lang="scss">
.login-form-container {
    height: 100%;
    align-items: center;
    display: flex;
    @include flex-center;

    .form-container {
        background-color: white;
        flex-direction: column;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
        max-height: 500px;
        max-width: 500px;
        width: 100%;
        border-radius: 20px;

        .form {
            display: flex;
            flex-direction: column;
            width: 100%;
            padding: 20px;
            max-width: 350px;
            gap: 10px;

            .login-button {
                // border: 1px solid ;
                border-radius: 5px;
                background-color: $accent-2;
                padding: 5px;
                text-align: center;
                color: $primary-bg;
                font-weight: bold;
                user-select: none;
                cursor: pointer;
            }
        }
    }

    .image-container {
        background-image: url("@/assets/images/login-image.jpg");
        background-repeat: no-repeat;
        background-size: 100% 100%;
    }
}
</style>
