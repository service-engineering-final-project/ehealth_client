# HealthyMe

## Service design and engineering final project (Alan Ramponi, 179850)

### Introduction

Hypertension is a common issue that generally develops over many years, and it affects nearly everyone eventually. Uncontrolled high blood pressure increases the risk of serious health problems, including heart attack and stroke. Fortunately, nowadays it can be easily detected and once a person know he has it, he can work with his doctor to control it. This service aims to help the interaction between two main agents, a doctor and a patient, to reach a patient's healthier life style. In particular way, a doctor can set some goals for his patient so the latter can use the service by updating his measurements each day. The service automatically checks if the patient is on the right track and if so, it suggests a healthy recipe (i.e. a treat), and otherwise it sends a motivational phrase to encourage the user to come back to the right direction. Indeed, the patient can autonomously request an healthy recipe by indicating a keyword (note that all the recipes collected from the external API service are filtered to a maximum amount of sodium, since it is an important player in hypertensive patients), and the service replies with all the nutrition facts of the recipe along with a URL with the direction to prepare it.

### Overview

During the initial phase a concept was designed along with a concrete scenario. Thus, drafts of related services for each module were conceived. The software architecture for the project was then finalized planning, among the other things, a possible user interface (see [here](https://github.com/service-engineering-final-project/healthyme_client/blob/master/img/client_interaction_design.png) for its interaction design). The services were then implemented, often in parallel, to taste the actual outcome of the whole system.

In a nutshell, the system provides the following functionalities:
* Create, read, update, delete users, measurements and goals;
* Set user's goals to be achieved with a target value and a deadline (e.g. loss weight, max sodium intake, min steps/day, sleep hours, nutrient accepted range);
* Add new health measurements regarding the health status and lifestyle (e.g. weight, steps, sleep_hours, proteins, carbohydrates, lipids, sodium);
* Get a summary of the progress regarding supported goals exploiting the business logic of the service;
* Get an healthy recipe with a low amount of sodium given a particular keyword;
* Get a tasty and healthy recipe if the user is on the right track, otherwise motivate him with a motivational phrase.

### Service architecture

The service architecture is partitioned into three main layers. The lower one deals with data; in particular, it is composed by four services that handles both data persistence and external data. The middle one deals with the system logic and it is composed by two services: a dispatcher one and a computational one. The upper layer, instead, is the client user interface that allows the doctor to insert a new person along with his determined goals and the patient to insert his measurements and get feedbacks on his situation.

In particular, the modules are the following:
* **Health internal service**: a SOAP web service that is responsible for all data-related requests (CRUD operations).
* **Recipe adapter service**: a REST web service that interacts with external APIs provided by [Yummly](http://www.yummly.com/). Thus, it retrieves data and it transforms it into a smarter for, more usable for our goals.
* **Quote adapter service**: 
* **Storage data service**: a REST web service that redirects requests from above to the right data source below.
* **Business logic service**: a REST web service that manipulates data to take decisions. It receives requests from the process centric service and gets data from the storage data service to compute results.
* **Process centric service**: a REST web service that receives requests form the user interface (client) and redirects them to the right module. It integrates both business logic methods and storage data service methods.
* [**User interface client**]: a Telegram bot that handles in an automatic fashion the patient actions. It doesn't represent a real intelligence; instead, it can be seen as a state diagram, so it manages user's decisions replying to him calling the REST process centric service to retrieve or manage data.

In order to have more details, see the resources below:

| module | technology |repository | API documentation | server URL |
|--------|------------|------------|-------------------| -------- |
| **Health internal service** | SOAP | [link](https://github.com/service-engineering-final-project/health_internal_service) | [link](http://docs.healthinternalservice.apiary.io/) | [link](https://health-internal-service-ar.herokuapp.com/soap/people?wsdl) |
| **Recipe adapter service** | REST | [link](https://github.com/service-engineering-final-project/recipe_adapter_service) | [link](http://docs.recipeadapterservice.apiary.io/) | [link](https://recipe-adapter-service-ar.herokuapp.com/rest/) |
| **Quote adapter service** | REST | [link](https://github.com/service-engineering-final-project/quote_adapter_service) | [link](http://docs.quoteadapterservice.apiary.io/) | [link](https://quote-adapter-service-ar.herokuapp.com/rest/) |
| **Storage data service** | REST | [link](https://github.com/service-engineering-final-project/storage_data_service) | [link](http://docs.storagedataservice.apiary.io/) | [link](https://storage-data-service-ar.herokuapp.com/rest/) |
| **Business logic service** | REST | [link](https://github.com/service-engineering-final-project/business_logic_service) | [link](http://docs.businesslogicservice1.apiary.io/) | [link](https://business-logic-service-ar.herokuapp.com/rest/) |
| **Process centric service** | REST | [link](https://github.com/service-engineering-final-project/process_centric_service) | [link](http://docs.processcentricservice1.apiary.io/) | [link](https://process-centric-service-ar.herokuapp.com/rest/) |

The repository for the **telegram bot client** can be found [here](https://github.com/service-engineering-final-project/healthyme_client). Note that the client is for demonstration purpose only, and it represents a sort of prototype of the real possible client.

![alt tag](img/service_architecture.png)

### How to run it
Since the server is already deployed on Heroku, it is only needed to go to the Heroku base URL (http://example.com). However, you can also deploy again the server on Heroku via git.

**Optional**: If you want to try the server locally, you can follow the steps below:
* **Clone** the repo: `git clone https://github.com/service-engineering-final-project/health_internal_service.git`;
* **Navigate** into the project folder: `cd health_internal_service`;
* **Install** the packages needed: `ant install`;
* **Run** the server using ant: `ant execute.server`.
