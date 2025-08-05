
# Instalação e Execução do Projeto

Para rodar a aplicação completa, você precisará de **dois terminais abertos simultaneamente**.

---

## 1. Configuração do Backend

Navegue até a pasta do Backend:

```bash
cd C:\Users\Paulo Ruan\Documents\UNIFOR\OPovo_Site-Model\Backend
````

Crie e ative o ambiente virtual (se ainda não o fez):

```powershell
python -m venv .env
.env\Scripts\activate
```

Instale as dependências do Python:

```powershell
pip install fastapi "uvicorn[standard]" pandas
```

---

## 2. Configuração do Frontend

Abra um **NOVO terminal**.

Navegue até a pasta do Frontend (substitua `wsa` pelo nome real da sua pasta SvelteKit, se for diferente):

```bash
cd C:\Users\Paulo Ruan\Documents\UNIFOR\OPovo_Site-Model\wsa
```

Instale as dependências do Node.js:

```bash
npm install
```

---

## 3. Execução da Aplicação

### No terminal do Backend, inicie o servidor FastAPI:

```powershell
uvicorn app.api:app --reload
```

### No terminal do Frontend, inicie o servidor de desenvolvimento do SvelteKit:

```bash
npm run dev
```

---

## Acesse a aplicação:

Abra seu navegador e vá para:
[http://localhost:5173/](http://localhost:5173/)


