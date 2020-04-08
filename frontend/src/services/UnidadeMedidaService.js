import axios from 'axios';
import { getAuthorization } from '../auth.js';

class UnidadeMedidaService {

    static async get() {
        try {
            const response = await axios
                .get("http://127.0.0.1:5000/unidade-medida", {
                    headers: {
                        Authorization: getAuthorization(),
                        "Content-Type": "application/json"
                    }
                });
            return response.data;
        }
        catch (error) {
            console.log(error);
            return [];
        }
    }
}

export default UnidadeMedidaService