
# Corretor de CSV para ETL
API em **FastAPI** desenvolvida para corrigir arquivos CSV exportados do banco **Firebird** do ERP da **LightSystem**, ajustando a codificação e o número de colunas para até 51 (se necessário pode deixar dinâmico a quantidade).

---

## Requisitos

- VPS com acesso ao **EasyPanel**
- Docker instalado no servidor
- Arquivos do projeto (`Dockerfile`, `app.py`, etc.)

---

## Deploy no VPS via EasyPanel

1. **Acesse o EasyPanel** no seu VPS.  
2. **Crie um novo container** ou serviço do tipo **Docker**.  
3. **Envie os arquivos do projeto** para o VPS (via FTP, Git ou upload direto no painel).  
4. **Configure o Docker**:
   - Defina a **imagem** a partir do `Dockerfile` do projeto.
   - Configure a **porta** para a API (ex: `8000`).
   - Ajuste variáveis de ambiente se necessário.  
5. **Construa e inicie o container**. O EasyPanel irá gerar o container executando a API.  
6. **Acesse a API** via navegador ou ferramentas como Postman:
   - Health check: `http://<seu_vps>:8000/`
   - Endpoint CSV: `POST http://<seu_vps>:8000/fix-csv`

---

## Exemplo de requisição via cURL

curl -X POST "http://<seu_vps>:8000/fix-csv" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/para/seu/arquivo.csv" \
  --output fixed_arquivo.csv

---
  
## Observações
- Pode ser adicionado uma opção de converter diretamente o CSV para XLSX para facilitar o processo de ETL.
- Pode ser adicionado a quantidade de colunas de maneira dinâmica para não quebrar o processo, pois passando de 51 ele estoura.
