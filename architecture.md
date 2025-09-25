ASCII architecture diagram

+----------------------+       HTTPS       +------------------------+
|      React UI        | <---------------> |   FastAPI backend      |
|  (frontend, Vite)    |                   |  - /api/review         |
+----------------------+                   |  - stores to MongoDB   |
           |                              +------------------------+
           |                                         |
           v                                         v
     Browser (HTTP)                             MongoDB Atlas / Local
                                                (collection: reviews)
           |
           v
      Optional: LLM (OpenAI) via backend
