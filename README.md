# HealthyMe

## Service design and engineering final project (Alan Ramponi, 179850)


### Introduction

Hypertension is a common issue that generally develops over many years, and it affects nearly everyone eventually. Uncontrolled high blood pressure increases the risk of serious health problems, including heart attack and stroke. Fortunately, nowadays it can be easily detected and once a person know he has it, he can work with his doctor to control it.


### Overview

This service aims to help the interaction between two main agents, a doctor and a patient, to reach a patient's healthier life style. In particular way, a doctor can set some goals for his patient so the latter can use the service updating his measurements each day. The service automatically checks if the patient is on the right track and if so, it suggests a healthy recipe (i.e. a treat), and otherwise it sends a motivational phrase to encourage the user to come back to the right direction. Indeed, the patient can autonomously request an healthy recipe by indicating a keyword (note that all the recipes collected from the external API service are filtered to a maximum amount of sodium, since it is an important player in hypertensive patients), and the service replies with all the nutrition facts of the recipe along with a URL with the direction to prepare it.


### Design and functionalities

During the initial phase a concept was designed along with a concrete scenario. Thus, drafts of related services for each module were conceived. The software architecture for the project was then finalized planning, among the other things, a possible user interface (see [here](https://github.com/service-engineering-final-project/healthyme_client/blob/master/img/client_interaction_design.png) the interaction design). The services were then implemented, often in parallel, to taste the actual outcome of the whole system.

In a nutshell, the system provides the following functionalities:
* **data management**: create, read, update, delete users, measurements and goals;
* **goals setting**: set user's goals to be achieved with a target value and a deadline:
  * e.g. loss weight, max sodium intake, min steps/day, sleep hours, nutrient accepted range;
* **measurements setting**: add new health measurements regarding the health status and lifestyle:
  * e.g. weight, steps, sleep_hours, proteins, carbohydrates, lipids, sodium;
* **progress summary**: get a summary of user's progresses regarding supported goals (via the business logic service);
* **health recipes discovery**: get an healthy recipe with a low amount of sodium given a particular keyword;
* **progress feedback**: get a healthy, tasty recipe if the user is on the right track, otherwise motivate him with a motivational phrase.


### Service architecture

The service architecture is partitioned into three main layers. The lower one deals with data; in particular, it is composed by four services that handles both data persistence and external data. The middle one deals with the system logic and it is composed by two services: a dispatcher one and a computational one. The upper layer, instead, is the client user interface that firstly allows the doctor to insert a new person along with his defined goals, and then allows the patient to insert his measurements and get feedbacks on his current health progress.

In particular, the modules are the following:
* **Health internal service**: a SOAP web service that is responsible for all data-related requests (CRUD operations). It talks directly to the internal database and replies to the storage data service requests;
* **Recipe adapter service**: a REST web service that provides data to the storage data service through a REST interface. It allows consumers to retrieve recipes and their nutritional facts in a structured, clearer format (both XML and JSON) exploiting the [Yummly APIs](http://www.yummly.com/) (by means of an academic plan); 
* **Quote adapter service**: a REST web service that provides data to the storage data service through a REST interface. It allows consumers to retrieve motivational quotes in a structured format (both XML and JSON) crawled from [Quotelicious](http://quotelicious.com/);
* **Storage data service**: a REST web service that redirects requests from the services above to the right data-related service below. It represents a sort of aggregator that provides a uniform REST interface to the high level services;
* **Business logic service**: a REST web service that deals with the manipulation of data in order to take decisions. It receives requests from the process centric service, then gets data from the storage data service to compute results to send back to the dispatcher;
* **Process centric service**: a REST web service that receives requests from the client (user interface) and redirects them to the right module below. It integrates both business logic methods and storage data service methods;
* [**User interface client**]: a Telegram bot that handles in an automatic fashion the patient actions. It doesn't represent a real intelligence; instead, it can be seen as a state diagram, so it manages user's decisions replying to him after sending requests to the REST process centric service.

![alt tag](img/service_architecture.png)

Note that service implementations are general and reusable in different scenarios. Indeed, each module interacts with other modules only through web services (except for the local database). In order to have more details, see the resources below:

| module | technology |repository | API documentation | server base URL |
|--------|------------|------------|-------------------| -------- |
| **Health internal service** | SOAP | [link](https://github.com/service-engineering-final-project/health_internal_service) | [link](http://docs.healthinternalservice.apiary.io/) | [link](https://health-internal-service-ar.herokuapp.com/ws/people?wsdl) |
| **Recipe adapter service** | REST | [link](https://github.com/service-engineering-final-project/recipe_adapter_service) | [link](http://docs.recipeadapterservice.apiary.io/) | [link](https://recipe-adapter-service-ar.herokuapp.com/rest/) |
| **Quote adapter service** | REST | [link](https://github.com/service-engineering-final-project/quote_adapter_service) | [link](http://docs.quoteadapterservice.apiary.io/) | [link](https://quote-adapter-service-ar.herokuapp.com/rest/) |
| **Storage data service** | REST | [link](https://github.com/service-engineering-final-project/storage_data_service) | [link](http://docs.storagedataservice.apiary.io/) | [link](https://storage-data-service-ar.herokuapp.com/rest/) |
| **Business logic service** | REST | [link](https://github.com/service-engineering-final-project/business_logic_service) | [link](http://docs.businesslogicservice1.apiary.io/) | [link](https://business-logic-service-ar.herokuapp.com/rest/) |
| **Process centric service** | REST | [link](https://github.com/service-engineering-final-project/process_centric_service) | [link](http://docs.processcentricservice1.apiary.io/) | [link](https://process-centric-service-ar.herokuapp.com/rest/) |

The repository for the **telegram bot client** can be found [here](https://github.com/service-engineering-final-project/healthyme_client). Note that the client is for demonstration purpose only, and it represents a sort of prototype of the real possible client.


### How to run it
All the services are already deployed on Heroku, thus it is only needed to go to the desired service Heroku base URL (see the table above) and start making HTTP requests via your preferred HTTP client. If you want to try out also the client prototype, you can follow the steps below:
* **Clone** the repo: `git clone https://github.com/service-engineering-final-project/healthyme_client.git`;
* **Navigate** into the project folder: `cd healthyme_client`;
* **Install** the packages needed via `pip`;
* **Run** the main script: `python client.py`.


### Contributors

* **Alan Ramponi**, 179850 | alan.ramponi@studenti.unitn.it
