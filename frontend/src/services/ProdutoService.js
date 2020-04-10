import axios from 'axios';
import { getAuthorization } from '../auth.js';

class ProdutoService {

    static async get() {
        try {
            const response = await axios
                .get("http://127.0.0.1:5000/produtos", {
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
                .post("http://127.0.0.1:5000/produtos",
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

    static async post(id, nome, cod_venda, preco_venda, preco_compra, qtd_min, ativado, unidade, categoria, fornecedor) {
        try {
            const response = await axios
                .post("http://127.0.0.1:5000/produtos",
                    {
                        id: id,
                        nome: nome,
                        cod_venda: cod_venda,
                        preco_venda: preco_venda,
                        preco_compra: preco_compra,
                        qtd_min: qtd_min,
                        ativado: ativado,
                        unidade: unidade,
                        categoria: categoria,
                        fornecedor: fornecedor
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

export default ProdutoService