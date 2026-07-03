# Elitze Sentinel Frontier — AGENTS.md

## Architecture

Three independent entrypoints, no monorepo tool:

| Layer | Dir | Entrypoint | Port |
|-------|-----|-----------|------|
| Python agent (LangGraph) | `/` | `main.py` (runs `agent/graph.py`) | CLI |
| Backend (Fastify + tRPC + Prisma) | `backend/` | `src/index.ts` | 3001 |
| Frontend (Next.js 16) | `frontend/` | `src/app/page.tsx` | 3000 |
| F5 Platform (FastAPI + WebSocket) | `f5_platform/` | `main.py` | 8000 |

Infrastructure via `docker-compose.yml`: PostgreSQL (pgvector), Redis, Keycloak, MinIO, Prometheus, OpenSearch.

## Commands

```powershell
# Frontend (next dev)
cd frontend; npm run dev

# Backend (ts-node dev)
cd backend; npm run dev
# Backend (build + prod)
cd backend; npm run build; npm start

# Python agent
pip install -r requirements.txt
python main.py "your prompt"
python main.py "your prompt" --llm          # requires ANTHROPIC_API_KEY or OPENAI_API_KEY

# Tests (pytest)
pytest test_agent.py -v

# Lint (frontend)
cd frontend; npm run lint

# Infrastructure
docker compose up -d
```

## Testing

- `pytest test_agent.py -v` — single-file tests for the LangGraph agent
- No Python typecheck config (ruff for lint only)
- No frontend/backend tests found

## Key quirks

- Frontend `@/` path alias maps to `frontend/src/*` (tsconfig `paths`)
- Frontend tRPC client imports types from `../../../backend/src/trpc` — assumes sibling directory layout
- Backend has a bug: `prisma` is imported from `./db` but `PrismaClient` is also instantiated directly in `index.ts` (line 11 vs line 32)
- `.env` lives in `backend/.env` (DATABASE_URL) — no root `.env`
- Root `.gitignore` covers `__pycache__/`, `*.db`, `node_modules/`, `.next/`, `.env`, `.vscode/`
- Frontend uses Next.js 16.2.9 with @base-ui/react, shadcn, framer-motion, reactflow, zustand, socket.io-client
- Backend uses Fastify, Prisma (no schema.prisma found — likely missing or needs `prisma init`), BullMQ (requires Redis), Socket.IO
- Python agent uses LangGraph with five phases: ingest → recon → interview → compile → handoff
- LLM-enhanced graph available via `create_fable5_graph_with_llm(llm)` in `agent/graph.py`

## Existing instruction files

- `frontend/AGENTS.md` — warns that Next.js may have breaking changes; check `node_modules/next/dist/docs/`
- `frontend/CLAUDE.md` — just `@AGENTS.md`
