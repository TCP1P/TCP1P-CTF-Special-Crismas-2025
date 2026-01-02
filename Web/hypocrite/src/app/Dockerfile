# Use the official Bun image
FROM oven/bun:latest

# Set working directory inside container
WORKDIR /app

# Copy package.json, bun.lockb first (better caching)
COPY package.json bun.lockb* ./

# Install dependencies
RUN bun i

# Copy rest of the project
COPY . .

# Run your app
CMD ["bun", "run", "index.ts"]
