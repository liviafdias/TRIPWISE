const database = require('../database/connection')

class ClienteController {

    // --------------------------------------------------------------------------
    
    novoCliente(request, response) {

    const {id_cliente, nome, email, senha, telefone, endereco} = request.body;
  
    if (!nome || !email || !senha || !telefone || !endereco) {
        return response.status(400).json({ error: 'Todos os campos são obrigatórios.' });
    }
  
    database.insert({ id_cliente, nome, email, senha, telefone, endereco }).table('Cliente')
        .then(() => {
            response.status(201).json({ message: 'Cliente adicionado com sucesso!' });
        })
        .catch((error) => {
            console.error(error);
            response.status(500).json({ error: 'Erro ao adicionar cliente.' });
        });

    }

    // --------------------------------------------------------------------------

    listarClientes(request, response) {
        database.select('*').table('Cliente')
            .then((clientes) => {
                response.status(200).json(clientes); // Retorna a lista de clientes
            })
            .catch((error) => {
                console.error(error);
                response.status(500).json({ error: 'Erro ao listar clientes.' });
            });
    }

    // --------------------------------------------------------------------------

    deletarCliente(request, response) {
        const { id_cliente } = request.params; // Captura o ID do cliente da URL
    
        if (!id_cliente) {
            return response.status(400).json({ error: 'O ID do cliente é obrigatório.' });
        }
    
        database('Cliente')
            .where('id_cliente', id_cliente) // Localiza o cliente pelo ID
            .del() // Deleta o registro
            .then((result) => {
                if (result) {
                    response.status(200).json({ message: 'Cliente deletado com sucesso!' });
                } else {
                    response.status(404).json({ error: 'Cliente não encontrado.' });
                }
            })
            .catch((error) => {
                console.error(error);
                response.status(500).json({ error: 'Erro ao deletar cliente.' });
            });
    }


    // --------------------------------------------------------------------------

    atualizarCliente(request, response) {
        const { id_cliente } = request.params; // Captura o ID do cliente da URL
        const { nome, email, senha, telefone, endereco } = request.body; // Captura os novos dados
    
        if (!id_cliente) {
            return response.status(400).json({ error: 'O ID do cliente é obrigatório.' });
        }
    
        // Verifica se pelo menos um campo foi enviado para atualização
        if (!nome && !email && !senha && !telefone && !endereco) {
            return response.status(400).json({ error: 'É necessário enviar ao menos um campo para atualizar.' });
        }
    
        const camposAtualizados = { nome, email, senha, telefone, endereco };
        // Remove campos não enviados
        Object.keys(camposAtualizados).forEach((key) => {
            if (!camposAtualizados[key]) delete camposAtualizados[key];
        });
    
        database('Cliente')
            .where('id_cliente', id_cliente) // Localiza o cliente pelo ID
            .update(camposAtualizados) // Atualiza os campos fornecidos
            .then((result) => {
                if (result) {
                    response.status(200).json({ message: 'Cliente atualizado com sucesso!' });
                } else {
                    response.status(404).json({ error: 'Cliente não encontrado.' });
                }
            })
            .catch((error) => {
                console.error(error);
                response.status(500).json({ error: 'Erro ao atualizar cliente.' });
            });
    }
    

  }

module.exports = new ClienteController()