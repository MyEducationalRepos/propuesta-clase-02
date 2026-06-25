## 1. Docker volume mount

- [x] 1.1 Add `./data:/data` volume mount to the n8n service in `docker-compose.yml`

## 2. Workflow JSON changes

- [x] 2.1 Re-enable the "If Severidad Alta?" node (remove `"disabled": true`)
- [x] 2.2 Replace the disabled Gmail node with a Code node ("Alerta Reaseguro") that appends a markdown table row to `/data/alertas_reaseguro.md` (creates file with header if missing)
- [x] 2.3 Replace the disabled Google Sheets node with a Code node ("Registro Log") that appends a markdown table row to `/data/log_triaje.md` (creates file with header if missing)
- [x] 2.4 Wire connections: Agent -> If -> Alta: Alerta Reaseguro + Registro Log; No Alta: Registro Log only
- [x] 2.5 Keep the Agent -> webhook response path (`responseMode: lastNode`) unchanged

## 3. Documentation

- [x] 3.1 Update `examples/n8n/README.md`: document the output files at `./data/`, update node descriptions table, remove Gmail/Sheets from config checklist

## 4. Verify

- [x] 4.1 Rebuild and start n8n, send a Baja severity curl request, confirm `./data/log_triaje.md` is created with the entry
- [x] 4.2 Send an Alta severity curl request, confirm both `./data/alertas_reaseguro.md` and `./data/log_triaje.md` are updated
