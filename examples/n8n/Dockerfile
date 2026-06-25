FROM n8nio/n8n:2.27.1

COPY workflow_triaje.json workflow_triaje_chat.json /home/node/workflows/

USER root
COPY init-workflows.sh /init-workflows.sh
RUN chmod +x /init-workflows.sh
USER node

ENTRYPOINT ["/init-workflows.sh"]
