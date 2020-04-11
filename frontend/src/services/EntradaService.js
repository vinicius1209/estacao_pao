import axios from 'axios';
import { getAuthorization } from '../auth.js';

class EntradaService {

    static async get() {
        try {
            const response = await axios
                .get("http://127.0.0.1:5000/entradas", {
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

    static async delete(id) {
        try {
            const response = await axios
                .post("http://127.0.0.1:5000/compras",
                    {
                        deletedId: id
                    },
                    {
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

    static async post(produtos) {
        try {
            const response = await axios
                .post("http://127.0.0.1:5000/entradas",
                    {
                        produtos: produtos
                    },
                    {
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

export default EntradaService