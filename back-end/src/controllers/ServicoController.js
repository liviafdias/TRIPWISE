const database = require('../database/connection');

class ServicoController {
    // --------------------------------------------------------------------------
    // Criar um novo serviço
    novoServico(request, response) {
        const {
            id_cliente,
            nome,
            descricao,
            preco,
            data_oferta_inicio,
            data_oferta_fim,
            data_escolhida,
            disponibilidade,
            localizacao,
            duracao,
            capacidade,
            categoria
        } = request.body;

        if (
            !id_cliente ||
            !nome ||
            !preco ||
            !data_oferta_inicio ||
            !data_oferta_fim
        ) {
            return response
                .status(400)
                .json({ error: 'Os campos obrigatórios não foram preenchidos.' });
        }

        const novoServico = {
            id_cliente,
            nome,
            descricao,
            preco,
            data_oferta_inicio,
            data_oferta_fim,
            data_escolhida,
            disponibilidade,
            localizacao,
            duracao,
            capacidade,
            categoria
        };

        database
            .insert(novoServico)
            .table('Servico')
            .then(() => {
                response
                    .status(201)
                    .json({ message: 'Serviço adicionado com sucesso!' });
            })
            .catch((error) => {
                console.error(error);
                response.status(500).json({ error: 'Erro ao adicionar serviço.' });
            });
    }

    // --------------------------------------------------------------------------
    // Listar todos os serviços
    listarServicos(request, response) {
        database
            .select('*')
            .table('Servico')
            .then((servicos) => {
                response.status(200).json(servicos); // Retorna a lista de serviços
            })
            .catch((error) => {
                console.error(error);
                response.status(500).json({ error: 'Erro ao listar serviços.' });
            });
    }

    // --------------------------------------------------------------------------
    // Atualizar um serviço
    atualizarServico(request, response) {
        const { id_servico } = request.params;
        const camposAtualizados = request.body;

        if (!id_servico) {
            return response
                .status(400)
                .json({ error: 'O ID do serviço é obrigatório.' });
        }

        // Remove campos não enviados
        Object.keys(camposAtualizados).forEach((key) => {
            if (!camposAtualizados[key]) delete camposAtualizados[key];
        });

        database('Servico')
            .where('id_servico', id_servico)
            .update(camposAtualizados)
            .then((result) => {
                if (result) {
                    response
                        .status(200)
                        .json({ message: 'Serviço atualizado com sucesso!' });
                } else {
                    response.status(404).json({ error: 'Serviço não encontrado.' });
                }
            })
            .catch((error) => {
                console.error(error);
                response
                    .status(500)
                    .json({ error: 'Erro ao atualizar serviço.' });
            });
    }

    // --------------------------------------------------------------------------
    // Deletar um serviço
    deletarServico(request, response) {
        const { id_servico } = request.params;

        if (!id_servico) {
            return response
                .status(400)
                .json({ error: 'O ID do serviço é obrigatório.' });
        }

        database('Servico')
            .where('id_servico', id_servico)
            .del()
            .then((result) => {
                if (result) {
                    response
                        .status(200)
                        .json({ message: 'Serviço deletado com sucesso!' });
                } else {
                    response.status(404).json({ error: 'Serviço não encontrado.' });
                }
            })
            .catch((error) => {
                console.error(error);
                response.status(500).json({ error: 'Erro ao deletar serviço.' });
            });
    }
}

module.exports = new ServicoController();
