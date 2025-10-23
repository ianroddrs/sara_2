class App {
    constructor() {
        this.csrfToken = this._getCookie('csrftoken');
        this.loadingContainer = document.getElementById('loading')
        this.alertContainer = document.getElementById('messages')

        window.addEventListener('DOMContentLoaded', () => this.toggleLoading())
    }

    _getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async request(url, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'X-CSRFToken': this.csrfToken,
            },
        };

        if (data) {
            if (!(data instanceof FormData)) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(data);
            } else {
                options.body = data;
            }
        }

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(errorData.message || 'Erro na requisição.');
            }
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                throw new Error(errorData.message || 'Erro na requisição.');
            }
        } catch (error) {
            this.showAlert(error, 'danger');
        }
    }

    showAlert(message, type) {
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        this.alertContainer.innerHTML = alertHtml;
    }


    toggleLoading() {
        this.loadingContainer.classList.toggle('d-none')
    }
}

window.app = new App();

class Sara {
    constructor() {
        this.csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        
        // Propriedades para o controle do tema
        this.themeToggleButton = document.getElementById('theme-toggle-btn');
        this.themeToggleIcon = null; // Será definido na inicialização
        this.themeSaveUrl = ''; // Será pego do atributo data-* do botão

        this._initThemeToggleButton(); // Inicia a funcionalidade do tema
        
        console.log("Sara inicializada. Pronta para ajudar!");
    }

    /**
     * Envia uma requisição assíncrona (AJAX) para o backend.
     * Usa a API Fetch e adiciona o token CSRF automaticamente.
     * @param {string} url - A URL do endpoint.
     * @param {string} method - O método HTTP (GET, POST, PUT, DELETE, etc.).
     * @param {object} [data=null] - O corpo da requisição (para POST, PUT).
     * @returns {Promise<object>} - Uma Promise que resolve com a resposta JSON.
     */
    async sendRequest(url, method = 'GET', data = null) {
        const options = {
            method: method.toUpperCase(),
            headers: {
                'X-CSRFToken': this.csrfToken,
                // O Content-Type é necessário para requisições POST/PUT com JSON
                'Content-Type': 'application/json',
            }
        };

        if (data && (method.toUpperCase() === 'POST' || method.toUpperCase() === 'PUT')) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                // Se a resposta não for bem-sucedida (status 4xx ou 5xx), lança um erro.
                const errorData = await response.json().catch(() => ({ message: 'Erro desconhecido' }));
                throw new Error(`Erro ${response.status}: ${errorData.message || response.statusText}`);
            }

            // Se a resposta não tiver conteúdo (status 204), retorna um objeto vazio.
            if (response.status === 204) {
                return {};
            }
            
            return await response.json(); // Retorna os dados da resposta em formato JSON

        } catch (error) {
            console.error('Falha na requisição:', error);
            this.showToast(error.message, 'error'); // Mostra um toast de erro
            throw error; // Propaga o erro para quem chamou a função
        }
    }

    /**
     * Inicia o listener de eventos para o botão de troca de tema.
     * Este é um método "privado", indicado pelo underscore.
     * @private
     */
    _initThemeToggleButton() {
        if (!this.themeToggleButton) {
            return; // Se o botão não existe na página, não faz nada.
        }

        // Pega o ícone e a URL para salvar o tema diretamente do botão
        this.themeToggleIcon = this.themeToggleButton.querySelector('i');
        this.themeSaveUrl = this.themeToggleButton.dataset.url; // Pega a URL do atributo 'data-url'

        // Adiciona o evento de click, garantindo que o 'this' se refira à instância da classe Sara
        this.themeToggleButton.addEventListener('click', (event) => this.toggleTheme(event));
    }

    /**
     * Executa a lógica de troca de tema.
     * @param {Event} event - O objeto do evento de clique.
     */
    toggleTheme(event) {
        // Previne o comportamento padrão do link
        event.preventDefault();
        event.stopPropagation();

        // 1. Alterna a classe no body
        document.body.classList.toggle('dark');

        // 2. Determina o novo tema
        const newTheme = document.body.classList.contains('dark') ? 'dark' : 'light';

        // 3. Alterna o ícone
        if (newTheme === 'dark') {
            this.themeToggleIcon.classList.remove('fa-moon');
            this.themeToggleIcon.classList.add('fa-sun');
        } else {
            this.themeToggleIcon.classList.remove('fa-sun');
            this.themeToggleIcon.classList.add('fa-moon');
        }

        // 4. Salva a preferência no backend usando o método da própria classe
        this._saveThemePreference(newTheme);
    }

    /**
     * Salva a preferência de tema no backend usando o método genérico sendRequest.
     * @param {string} theme - O tema a ser salvo ('light' ou 'dark').
     * @private
     */
    _saveThemePreference(theme) {
        if (!this.themeSaveUrl) {
            console.error('URL para salvar o tema não foi definida no atributo data-url do botão.');
            return;
        }
        
        // REUTILIZANDO o método sendRequest!
        this.sendRequest(this.themeSaveUrl, 'POST', { theme: theme })
            .then(data => {
                if (data.status === 'ok') {
                    console.log('Tema salvo com sucesso!');
                } else {
                    console.error('Falha ao salvar o tema:', data.message);
                }
            })
            .catch(error => {
                // O método sendRequest já loga o erro detalhado.
                // Aqui podemos apenas registrar o contexto.
                console.error('Ocorreu um erro na operação de salvar o tema.');
            });
    }

    /**
     * Exibe uma notificação toast na tela.
     * (Este é um exemplo simples. Você pode integrar com uma biblioteca como Toastify.js ou criar seu próprio CSS)
     * @param {string} message - A mensagem a ser exibida.
     * @param {string} [type='success'] - O tipo de toast ('success', 'error', 'info').
     */
    showToast(message, type = 'success') {
        // Lógica para criar e exibir um toast
        // Por enquanto, vamos usar um console.log para simular.
        console.log(`[TOAST - ${type.toUpperCase()}]: ${message}`);
        // Exemplo real:
        // const toast = document.createElement('div');
        // toast.className = `toast toast-${type}`;
        // toast.textContent = message;
        // document.body.appendChild(toast);
        // setTimeout(() => toast.remove(), 3000);
    }

    /**
     * Exibe um modal.
     * (Pode ser integrado com Bootstrap Modal, ou um componente customizado)
     * @param {string} title - O título do modal.
     * @param {string} content - O conteúdo HTML do modal.
     */
    showModal(title, content) {
        // Lógica para criar e exibir um modal
        console.log(`[MODAL]: Título: ${title}`);
        alert(content); // Simulação simples
    }
}