# autolara

This scraper will check https://alaragames.se for new cards and send webhook notification on discord when the card is in stock

## Installation
The easiest way to run this project is with docker.

1. Create file cards.txt with one cardname per row.
2. Add discord [Webhook URL](https://support.discord.com/hc/en-us/articles/228383668-Anv%C3%A4nda-Webhooks). to the docker-compose environment variables
3. docker-compose up -d

## cards.txt example

```
Endurance
Lightning bolt
Abrupt decay
``` 
