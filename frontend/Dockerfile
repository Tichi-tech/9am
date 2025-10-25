FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy application
COPY . .

# Build
RUN npm run build

# Expose port
EXPOSE 3000

# Serve with preview (for quick deploy) or use a static server
CMD ["npm", "run", "preview", "--", "--port", "3000", "--host", "0.0.0.0"]
