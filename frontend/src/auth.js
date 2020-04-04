import VueJwtDecode from 'vue-jwt-decode'


export function login(token) {
    localStorage.setItem("token", token);
}

export function logout() {
    localStorage.removeItem('token');
}

export function isLoged() {
    const token = localStorage.getItem('token');

    if (!token) {
        return false;
    }

    try {
        const { exp: expiration } = VueJwtDecode.decode(token);
        const isExpired = !!expiration && Date.now() > expiration * 1000;

        if (isExpired)
            return false;

        return true;
    } catch (_) {
        return false;
    }

}