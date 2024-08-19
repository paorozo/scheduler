# Task Scheduler Service

## Description

The **Task Scheduler Service** is a scalable and reliable API designed to manage and execute scheduled tasks using timers. The service supports the creation, querying, and triggering of timers, which can be configured to send a webhook once expired. It is built with FastAPI, PostgreSQL, and Docker, ensuring easy deployment and horizontal scalability.

## Features

- **Create Timers**: Schedule tasks by creating timers with custom durations.
- **Query Timers**: Retrieve the status of any timer using its unique identifier.
- **Webhook Triggering**: Automatically trigger webhooks when timers expire, ensuring that each timer fires only once.
- **Persistence and Fault Tolerance**: Timers are stored in a PostgreSQL database, ensuring they persist through service restarts. Expired timers are processed as soon as the service is back online.
- **Scalability**: The service is containerized using Docker, allowing for easy scaling and deployment across multiple instances.
- **API Documentation**: Explore the API endpoints and models using the Swagger UI interface.
- **Unit Testing**: Comprehensive unit tests ensure the correctness of the service components.
- **Linting and Formatting**: Code linting and formatting checks are included to maintain code quality and consistency.
- **Error Handling**: Custom error handling ensures that users receive informative messages when issues occur.
- **Logging**: Detailed logs are generated to track the service's activity and troubleshoot any problems.
- **Configuration Management**: Environment variables are used to configure the service, allowing for easy customization and deployment.
- **Docker Compose**: The service can be easily built and started using Docker Compose, simplifying the development and deployment process.
- **Code Coverage**: Unit tests are run with code coverage analysis, providing insights into the test coverage of the codebase.
- 
## Prerequisites

- Docker
- Docker-compose

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/paorozo/scheduler.git
   cd scheduler
   ```

2. Build and start the service using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Access the service at `http://localhost:8080`.

4. Explore the API documentation using Swagger UI at `http://localhost:8080/docs`.

## API Endpoints

### Timer Management

- **Create Timer**

  - **POST /timer**: Create a new timer.
  - **Request Body**:
    ```json
    {
      "hours": 1,
      "minutes": 30,
      "seconds": 45,
      "url": "http://example.com/webhook"
    }
    ```
  - **Response**:
    ```json
    {
      "timer_id": 1,
      "time_left": 10
    }
    ```

- **Get Timer by ID**

  - **GET /timer/{timer_id}**: Retrieve the status and details of a timer by its ID.
  - **Path Parameter**:
    - `timer_id`: The unique identifier of the timer.
  - **Response**:
    ```json
     {
      "timer_id": 1,
      "time_left": 10
    }
    ```

## Architecture

The service is built using the following components:

- **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.8+.
- **PostgreSQL**: A powerful, open-source object-relational database system used for storing timer information.
- **Docker**: Containerization technology that packages the application and its dependencies into a single unit, ensuring consistency across different environments.
- **SQLAlchemy**: An SQL toolkit and Object-Relational Mapping (ORM) library for Python, used to interact with the PostgreSQL database.
- **Pydantic**: Data validation and settings management using Python type annotations, utilized for request and response models.

## Testing

- The project includes a comprehensive suite of unit tests to ensure the correct functionality of all components.
- To run the tests, execute the following command:

  ```bash
  docker-compose run test
  ```
- After running the tests, you can view the coverage report by navigating to the generated HTML report:

  ```bash
  open htmlcov/index.html
  ```

  This report provides detailed insights into the code coverage, helping to identify untested parts of the codebase.


## Linting

- The linter is configured to use `black` for automatic code formatting and linting checks.
- The linting checks are automatically run when the project is built, but you can also run them manually with:

  ```bash
  docker-compose run linter
  ```

## Future Enhancements

- **Metrics and Monitoring**: Integrating with a monitoring service to track performance metrics and errors.
- **Authentication and Authorization**: Implementing security measures for endpoints to restrict access based on roles.
