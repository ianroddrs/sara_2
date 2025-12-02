class App {
    constructor() {
        this.csrfToken = document.querySelector("meta[name='csrf-token']").getAttribute('content');
        this.loadingContainer = document.getElementById('loading')
        this.alertContainer = document.getElementById('messages')

        this.modalLogin = new bootstrap.Modal(document.querySelector('#login-modal'))
        this.formularioLogin = document.getElementById('login-form')
        this.logoutButton = document.getElementById('logoutBtn')

        
        this.formularioLogin.addEventListener('submit', async (event) => {this.login(event)})
        if(this.logoutButton){
            this.logoutButton.addEventListener('click', async(event)=> {this.logout(event)})
        }

        window.addEventListener('DOMContentLoaded', () => this.toggleLoading())
    }

    async request(url, method = 'GET', data = null) {
        const options = {
            method: method.toUpperCase(),
            headers: {
                'X-CSRFToken': this.csrfToken,
            },
        };
        
        try {
            if (data) {
                if (!(data instanceof FormData)) {
                    let formulario = new FormData();

                    for (const [chave, valor] of Object.entries(data)) {
                        formulario.append(chave, valor);
                    }
                    
                    data = formulario

                }

                options.body = data;
            }

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
        let icon = ''
        if(type=='danger'){
            icon = '<i class="bi bi-exclamation-triangle-fill me-2"></i>'
        }
        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center" role="alert">
                ${icon}
                <div>
                    ${message}
                </div>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;

        this.alertContainer.innerHTML = alertHtml;
    }


    toggleLoading() {
        this.loadingContainer.classList.toggle('d-none')
    }


    async login(event){
        event.preventDefault();
        const urlParams = new URLSearchParams(window.location.search);
        const formulario = new FormData(this.formularioLogin);

        if(urlParams.has('next')){ 
            formulario.append('next', urlParams.get('next'))
        }

        this.modalLogin.hide()

        const response = await this.request('/login', 'POST', formulario);
        
        if (response.redirect_url) {
            window.location.href = response.redirect_url;
        }
        this.showAlert(response.message, 'success');
    }

    async logout(event){
        event.preventDefault();
        const response = await this.request('/logout', 'POST');
        location.reload();
        this.showAlert(response.message, 'success');
    }
}

window.app = new App();

class Sara {
    constructor() {
        
        // Propriedades para o controle do tema
        this.themeToggleButton = document.getElementById('theme-toggle-btn');
        this.themeToggleIcon = null; // Será definido na inicialização
        this.themeSaveUrl = ''; // Será pego do atributo data-* do botão

        this._initThemeToggleButton(); // Inicia a funcionalidade do tema
        
    }

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
}