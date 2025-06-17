# Monitor de Serviços Web

Este projeto monitora a disponibilidade de sites/serviços web e envia alertas por e-mail e/ou Telegram caso algum serviço fique fora do ar. Ideal para automação, portfólio de DevOps e estudos de monitoramento.

## Funcionalidades
- Checagem periódica de múltiplos sites (configurável via YAML)
- Notificações por e-mail e Telegram
- Logs de auditoria em arquivo
- Código pronto para rodar localmente ou em cloud VM

## Como usar

1. **Clone o repositório**
    ```bash
    git clone https://github.com/SEU_USUARIO/web_monitor.git
    cd web_monitor
    ```

2. **Crie um ambiente virtual e instale as dependências**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure o arquivo `config.yaml`** com os sites e dados de notificação.

4. **Execute o monitor**
    ```bash
    python monitor.py
    ```

5. **Verifique os logs em `logs/monitor.log`** e os alertas recebidos.

## Exemplo de Configuração

```yaml
check_interval: 5  # minutos
websites:
  - name: Google
    url: https://www.google.com
notifications:
  email:
    enabled: true
    smtp_server: smtp.gmail.com
    smtp_port: 587
    username: seu_email@gmail.com
    password: sua_senha_de_app
    from: seu_email@gmail.com
    to: destinatario@gmail.com
  telegram:
    enabled: false
    bot_token: SEU_TOKEN_AQUI
    chat_id: SEU_CHAT_ID_AQUI
