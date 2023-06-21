import { useAuthStore } from "@/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames, navigateTo } from "@typed-router";
export const useAuthMiddleware = async (context, isAdmin) => {
    const authStore = useAuthStore();
    const { logout, refresh } = authStore;
    const { logined, userData } = storeToRefs(authStore);
    if (process.server) {
        await authStore.getUserData();
        if (!logined.value || (isAdmin && userData.value?.is_superuser !== true)) {
            logout();
            return navigateTo({ name: routesNames.login });
        }
    } else if (process.client) {
        await refresh();
        if (!logined.value || (isAdmin && userData.value?.is_superuser !== true)) {
            return navigateTo({ name: routesNames.login });
        }
    }
};