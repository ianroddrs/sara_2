/**
 * Classe Phoenix: Gerencia as interações específicas da aplicação "Phoenix".
 * Herda da classe Sara para reutilizar funcionalidades comuns.
 */
class Phoenix extends Sara {
    constructor() {
        super(); // ESSENCIAL: Chama o construtor da classe mãe (Sara)
        this.specificButton = document.getElementById('phoenix-specific-button');
        this.init(); // Chama o método para iniciar os eventos
    }

    /**
     * Inicia os "event listeners" específicos desta aplicação.
     */
    init() {
        if (this.specificButton) {
            this.specificButton.addEventListener('click', () => this.handleSpecificAction());
        }
        console.log("Módulo Phoenix inicializado.");
    }

    /**
     * Lida com uma ação específica da aplicação Phoenix.
     * Usa o método 'sendRequest' herdado de Sara.
     */
    async handleSpecificAction() {
        const dataToSend = {
            id: 123,
            action: 'process_phoenix_data'
        };

        this.showToast('Enviando dados para o Phoenix...', 'info');

        try {
            const response = await this.sendRequest('/api/phoenix/process/', 'POST', dataToSend);
            console.log('Resposta do backend:', response);
            this.showToast(response.message, 'success'); // Usa outro método herdado

            // Aqui você pode atualizar a interface específica do Phoenix
            this.updatePhoenixUI(response.data);

        } catch (error) {
            // O tratamento de erro já é feito na classe Sara,
            // mas você pode adicionar lógicas extras aqui se quiser.
            console.log("Tratamento de erro adicional específico do Phoenix.");
        }
    }

    /**
     * Atualiza a interface do usuário com base nos dados recebidos.
     * @param {object} data - Os dados para atualizar a UI.
     */
    updatePhoenixUI(data) {
        const resultContainer = document.getElementById('phoenix-result');
        if (resultContainer) {
            resultContainer.innerHTML = `<h3>Dados Atualizados</h3><p>${JSON.stringify(data)}</p>`;
        }
    }
}


// Inicia a lógica da aplicação Phoenix quando o DOM estiver pronto.
document.addEventListener('DOMContentLoaded', () => {
    new Phoenix();
});