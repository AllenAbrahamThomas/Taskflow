FROM node:20-slim

WORKDIR /app

# Copy dependency files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose Next.js port
EXPOSE 3000

# Start Next.js in development mode
CMD ["npm", "run", "dev"]
