# Reusable bot image. Playwright ships a base image with Chromium + all the
# system libs already installed, which saves a lot of apt wrangling.
FROM mcr.microsoft.com/playwright:v1.45.0-jammy

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

COPY bot.js ./

ENV PORT=3001
EXPOSE 3001
CMD ["node", "bot.js"]
