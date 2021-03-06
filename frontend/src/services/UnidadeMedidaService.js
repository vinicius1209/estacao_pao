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

    static async delete(id) {
        try {
            const response = await axios
                .post("http://127.0.0.1:5000/unidade-medida",
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

    static async post(id, abreviacao, descricao, fracionavel) {
        try {
            const response = await axios
                .post("http://127.0.0.1:5000/unidade-medida",
                    {
                        id: id,
                        abreviacao: abreviacao,
                        descricao: descricao,
                        fracionavel: fracionavel
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

export default UnidadeMedidaService