FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --silent

# Copy application code
COPY . .

# Set environment variable to avoid opening browser
ENV BROWSER=none

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
