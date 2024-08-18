# Task Scheduler Service

## Description

This service allows the execution of scheduled tasks using timers.

## How to run

1. Run the following command to start the service:

```bash
docker build -t app .

docker run -p 8080:8080 app
```

2. Access the service at `http://localhost:8080`
3. Access the servuce documentation at `http://localhost:8080/docs`

## Endpoints

- 'POST /timer': Create a new timer
- 'GEST /timer/{timer_id}': Get a timer by id

## Testing

- Execute the following command to run the tests:

```bash
pytest
```

## Linting
- The linter is configured to use `black` to automatically format the code and check for linting errors when the project is build.
- Additionally, you can execute the following command to run the linting:

```bash
docker-compose run linter
```
