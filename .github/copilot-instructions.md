# Arquimedes workspace

- Use Python 3.14 and Streamlit for the main application.
- Keep reusable UI in `components/` and route pages through `views/`.
- Preserve responsive tablet and mobile layouts.
- Use local assets from `assets/`; keep external videos limited to deliberate fallbacks.
- Keep Supabase integration isolated under `services/` and add it only when credentials are configured.
- Run validation with `C:/Python314/python.exe -m compileall -q app.py views components services`.
- Launch with `C:/Python314/python.exe -m streamlit run app.py`.
