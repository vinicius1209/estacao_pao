import axios from 'axios';
import { getAuthorization } from '../auth.js';

class CategoriaService {

    static async get() {
        try {
            const response = await axios
                .get("http://127.0.0.1:5000/categorias", {
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
                .post("http://127.0.0.1:5000/categorias",
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

    static async post(id, nome) {
        try {
            const response = await axios
                .post("http://127.0.0.1:5000/categorias",
                    {
                        id: id,
                        nome: nome
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

export default CategoriaService