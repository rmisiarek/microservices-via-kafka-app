<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>


## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

The project - [microservices-via-kafka-app](https://github.com/rmisiarek/microservices-via-kafka-app) - started with a few ideas in mind:
* []() Build simple application for learning Kubernetes.
* []() Learn how Apache Kafka might be used for communication between microservices.
* []() Test Python libraries for Apache Kafka.
* []() Test FastAPI together with WebSockets.
* []() In general: test, learn and have some fun, definitely not for production usage.


### Built With

* []() ***Python 3.9***
* []() Apache Kafka without Zookeeper (KRaft mode)
* []() Docker and docker-compose
* []() Python libraries for Kafka:
  * []() confluent-kafka
  * []() aiokafka
* []() FastAPI & Uvicorn
* []() Poetry as dependency manager


## Getting Started

To get a local copy up and running follow these simple steps.


### Prerequisites

This project requires Docker and docker-compose installed on your system. Please follow steps:
* Docker - https://docs.docker.com/get-docker/
* Docker-compose - https://docs.docker.com/compose/install/


### Installation

1. Clone the repo
   ```
   git clone https://github.com/rmisiarek/microservices-via-kafka-app.git
   ```
2. Use docker-compose to start services
   ```
   cd microservices-via-kafka-app
   docker-compose up
   ```
3. Open `dashboard.html` in your browser.

## Usage

The project consists of four services:
* Stock-Quotes-Service - reads sample stock quotes data from file and then - by using Kafka - send them to Recommendation-Service and Dashboard-Service.
* Recommendation-Service - receives message from Stock-Quotes-Service with data about HLOC prices in one point in time and calculates average price from last five records. If current price is above average it is signal to buy, if not sell recommendation is generated. Message with recommendation is send to Dashboard-Service.
* Dashboard-Service - receives messages from both Stock-Quotes-Service (to present price changes over time) and Recommendation-Service (to present buy/sell recommendation).
* Broker - Kafka service used to microservices orchestration.


## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## License

Distributed under the MIT License.


## Contact

Rafał Misiarek

Project Link: [https://github.com/rmisiarek/microservices-via-kafka-app](https://github.com/rmisiarek/microservices-via-kafka-app)
