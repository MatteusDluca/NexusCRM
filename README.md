<div align="center">
  <h1>🚀 Nexus Board</h1>
  <p><strong>A Premium Full-Stack Kanban Application</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js" />
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=FastAPI&logoColor=white" alt="FastAPI" />
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
  </p>
</div>

---

## 📋 Sobre o Projeto

O **Nexus Board** é um sistema de gerenciamento de tarefas visual (Kanban) de alto nível, construído com foco em **Arquitetura Limpa**, **Segurança** e **Experiência do Usuário (UX/UI)** imersiva. Este não é apenas um clone comum; é uma demonstração de engenharia de software Fullstack Moderna.

### 🌟 Features de Destaque
- **Painel Interativo:** Drag-and-Drop fluído de Cartões e Tarefas com atualizações otimistas na interface (*Optimistic UI*), minimizando a percepção de latência do servidor.
- **Atributos Avançados Sênior:** Gerenciamento cirúrgico de Cartões com suporte para Seleção de Prazos, Níveis dinâmicos de Prioridade, Tags em massa e **Atribuição de Usuários** resolvida em complexidade *O(1)*.
- **Design System Customizado:** Arquitetado com **Design Tokens** do Material Design 3 e Componentes Headless (Shadcn/Radix), garantindo acessibilidade (ARIA) perfeita e estética Premium.
- **Micro-interações:** Componentes táteis guiados pelas heurísticas da *Apple Human Interface Guidelines*.

---

## 🏗️ Stack Tecnológica & Engenharia de Arquitetura

### 🖥️ Frontend Sênior
- **Framework:** Next.js Sólido (App Router) + React.
- **Styling:** Tailwind CSS + Shadcn UI (Radix Primitives).
- **Core de Arraste:** Biblioteca profissional `@hello-pangea/dnd` controlando blocos React.
- **Estratégia:** Prevenção massiva de *Prop Drilling*, com mapeamento assíncrono em `Promise.all()` mitigando o *N+1 query problem*.

### ⚙️ Backend e Banco de Dados Limpo
- **Framework:** Python FastAPI (Assíncrono, Integrado, Ultrarrápido).
- **Modelagem ORM:** PostgreSQL blindado em SQLAlchemy Models.
- **Migrations:** Controle restrito de schema via `Alembic` (DDLs controladas).
- **Auth:** JWT (JSON Web Tokens) State-of-the-art com Passwords assíncronas criptografadas em bcrypt.
- **Domain-Driven REST:** Clean Architecture com separação em três camadas rígidas (Rotas, Domain Services, Repositories).

### 🐳 Infraestrutura (DevSecOps)
- **Containerização:** Orquestrado em `Docker Compose`.
- **Performance de Base:** Process Manager de Servidor combinando *Gunicorn e Uvicorn Workers*.
- **Segurança Padrão Zero-Trust:** Execução *Rootless* nas imagens Docker usando Linux base Users, e Builds *Multi-Stage* mitigando ataques CVE de supply-chain e imagens ultra leves.

---

## 🚀 Como Executar Localmente

Preparado para produção. Você precisará de **Docker** e **Docker Compose** instalados na sua máquina.

1. Clone o repositório:
```bash
git clone https://github.com/MatteusDluca/NexusCRM.git
cd NexusCRM
```

2. Usando o Docker Compose, suba a infraestrutura pesada (Banco de Dados + API + Frontend) num comando mágico:
```bash
docker-compose up --build -d
```

3. Acesse os serviços hospedados na rede nativa:
- **Painel Frontend (UI):** [http://localhost:3000](http://localhost:3000)
- **Documentação de API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

<br>

<div align="center">
  <h3>Arquitetado e Desenvolvido por</h3>
  <h2><strong>Matteus Dluca</strong></h2>
  <p>Software Engineer</p>
</div>
