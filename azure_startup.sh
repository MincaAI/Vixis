#!/bin/bash
cd /home/site/wwwroot
mkdir -p .streamlit
python azure_write_secrets.py || echo "Warning: azure_write_secrets.py failed"
pip install -r requirements.txt
exec python -m streamlit run main.py --server.port 8000 --server.address 0.0.0.0 --server.useStarlette false
