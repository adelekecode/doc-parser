FROM nginx:alpine

COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Create a directory for the file uploads
RUN mkdir -p /tmp/pitch-deck-uploads && chmod 777 /tmp/pitch-deck-uploads
